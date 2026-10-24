"""Read-only runtime tracing for one Stage 2 reconciliation target.

The tracer observes the existing onboarding_plan reconciliation code without
reimplementing or altering its basketball decisions. It is intended only for
disposable diagnostics after a permanent proposal rehearsal has blocked.
"""

from __future__ import annotations

import sys
from copy import deepcopy
from types import FrameType
from typing import Any


def _location_status(city: Any, state: Any) -> str:
    city_value = str(city or "").strip()
    state_value = str(state or "").strip()
    if city_value and state_value:
        return "complete"
    if not city_value and not state_value:
        return "blank"
    return "partial"


class ReconciliationTrace:
    """Capture one canonical game's actual reconciliation mutation path."""

    def __init__(self, canonical_game_id: str):
        canonical_game_id = canonical_game_id.strip()
        if not canonical_game_id:
            raise ValueError("canonical_game_id is required")
        self.canonical_game_id = canonical_game_id
        self.document: dict[str, Any] = {
            "schema_version": 1,
            "kind": "IMPLEMENTATION_RECONCILIATION_TRACE",
            "canonical_game_id": canonical_game_id,
            "decision_order": [],
            "mutations": [],
            "site_sync_events": [],
        }
        self._old_trace = None
        self._last_canonical: dict[str, Any] | None = None
        self._last_sources: dict[str, dict[str, Any]] = {}
        self._last_assertions: dict[str, dict[str, Any]] = {}
        self._current_decision: dict[str, Any] | None = None
        self._seen_decisions: set[str] = set()
        self._sync_initial: dict[int, dict[str, Any]] = {}

    def __enter__(self) -> "ReconciliationTrace":
        self._old_trace = sys.gettrace()
        sys.settrace(self._trace)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        sys.settrace(self._old_trace)
        self._old_trace = None
        if exc is not None and "error" not in self.document:
            self.document["error"] = str(exc)
        self._finalize_classification()

    def _trace(self, frame: FrameType, event: str, arg: Any):
        if frame.f_globals.get("__name__") != "onboarding_plan":
            return self._trace
        name = frame.f_code.co_name
        if name == "apply_reconciliation_decisions":
            self._trace_reconciliation(frame, event, arg)
        elif name == "_sync_site_metadata_from_source":
            self._trace_site_sync(frame, event, arg)
        return self._trace

    def _initialize_from_locals(self, local: dict[str, Any]) -> None:
        if "canonical_before" in self.document:
            return
        canonical_by_id = local.get("canonical_by_id")
        if not isinstance(canonical_by_id, dict):
            return
        canonical = canonical_by_id.get(self.canonical_game_id)
        if not isinstance(canonical, dict):
            return
        self.document["canonical_before"] = deepcopy(canonical)
        self._last_canonical = deepcopy(canonical)

        assertion_rows = local.get("assertion_rows")
        if isinstance(assertion_rows, list):
            linked = [
                deepcopy(row)
                for row in assertion_rows
                if isinstance(row, dict)
                and row.get("canonical_game_id") == self.canonical_game_id
            ]
            self.document["linked_assertions_before"] = linked
            self._last_assertions = {
                str(row.get("assertion_id") or f"assertion-{index}"): deepcopy(row)
                for index, row in enumerate(linked)
            }

        source_rows = local.get("source_rows")
        school_key = str(local.get("school_key") or "")
        source_ids = {
            str(row.get("source_game_id") or "")
            for row in self.document.get("linked_assertions_before", [])
            if row.get("source_program_key") == school_key
        }
        if isinstance(source_rows, list):
            sources = [
                deepcopy(row)
                for row in source_rows
                if isinstance(row, dict)
                and str(row.get("source_game_id") or "") in source_ids
            ]
            self.document["target_source_rows_before"] = sources
            self._last_sources = {
                str(row.get("source_game_id") or f"source-{index}"): deepcopy(row)
                for index, row in enumerate(sources)
            }

        approved = local.get("approved")
        if isinstance(approved, dict):
            self.document["approved_decisions_touching_game"] = [
                deepcopy(item)
                for item in approved.get("decisions", [])
                if isinstance(item, dict)
                and item.get("canonical_game_id") == self.canonical_game_id
            ]

    def _decision_context(self, local: dict[str, Any]) -> dict[str, Any] | None:
        item = local.get("item")
        if not isinstance(item, dict):
            return None
        game_id = str(
            local.get("actual_game_id")
            or item.get("canonical_game_id")
            or local.get("game_id")
            or ""
        )
        if game_id != self.canonical_game_id:
            return None
        decision_id = str(item.get("decision_id") or "")
        if not decision_id:
            return None
        return {
            "decision_id": decision_id,
            "category": str(item.get("category") or ""),
            "field_name": str(item.get("field_name") or ""),
            "decision": str(item.get("decision") or ""),
            "source_game_id": str(item.get("source_game_id") or ""),
        }

    @staticmethod
    def _diff(before: dict[str, Any], after: dict[str, Any]) -> dict[str, dict[str, Any]]:
        keys = sorted(set(before) | set(after))
        return {
            key: {"before": before.get(key, ""), "after": after.get(key, "")}
            for key in keys
            if before.get(key, "") != after.get(key, "")
        }

    def _record_row_changes(self, frame: FrameType) -> None:
        local = frame.f_locals
        canonical = local.get("canonical")
        if isinstance(canonical, dict) and canonical.get("canonical_game_id") == self.canonical_game_id:
            current = deepcopy(canonical)
            if self._last_canonical is None:
                self._last_canonical = current
            else:
                changes = self._diff(self._last_canonical, current)
                if changes:
                    self.document["mutations"].append(
                        {
                            "row_kind": "canonical",
                            "row_id": self.canonical_game_id,
                            "decision": deepcopy(self._current_decision),
                            "function": frame.f_code.co_name,
                            "line": frame.f_lineno,
                            "changes": changes,
                        }
                    )
                    self._last_canonical = current
            self.document["canonical_last_observed"] = current

        source = local.get("source")
        if isinstance(source, dict):
            source_id = str(source.get("source_game_id") or "")
            known_ids = {
                str(row.get("source_game_id") or "")
                for row in self.document.get("target_source_rows_before", [])
            }
            if source_id and source_id in known_ids:
                current = deepcopy(source)
                previous = self._last_sources.get(source_id)
                if previous is None:
                    self._last_sources[source_id] = current
                else:
                    changes = self._diff(previous, current)
                    if changes:
                        self.document["mutations"].append(
                            {
                                "row_kind": "source",
                                "row_id": source_id,
                                "decision": deepcopy(self._current_decision),
                                "function": frame.f_code.co_name,
                                "line": frame.f_lineno,
                                "changes": changes,
                            }
                        )
                        self._last_sources[source_id] = current

        assertion = local.get("assertion")
        if isinstance(assertion, dict) and assertion.get("canonical_game_id") == self.canonical_game_id:
            assertion_id = str(assertion.get("assertion_id") or "")
            current = deepcopy(assertion)
            previous = self._last_assertions.get(assertion_id)
            if previous is None:
                self._last_assertions[assertion_id] = current
            else:
                changes = self._diff(previous, current)
                if changes:
                    self.document["mutations"].append(
                        {
                            "row_kind": "assertion",
                            "row_id": assertion_id,
                            "decision": deepcopy(self._current_decision),
                            "function": frame.f_code.co_name,
                            "line": frame.f_lineno,
                            "changes": changes,
                        }
                    )
                    self._last_assertions[assertion_id] = current

    def _trace_reconciliation(self, frame: FrameType, event: str, arg: Any) -> None:
        local = frame.f_locals
        self._initialize_from_locals(local)

        context = self._decision_context(local)
        if context is not None:
            self._current_decision = context
            decision_id = context["decision_id"]
            if decision_id not in self._seen_decisions:
                self._seen_decisions.add(decision_id)
                self.document["decision_order"].append(deepcopy(context))
        elif isinstance(local.get("item"), dict):
            self._current_decision = None

        if event in {"line", "return", "exception"}:
            self._record_row_changes(frame)

        canonical_by_id = local.get("canonical_by_id")
        if isinstance(canonical_by_id, dict):
            canonical = canonical_by_id.get(self.canonical_game_id)
            if isinstance(canonical, dict):
                final = deepcopy(canonical)
                self.document["canonical_last_observed"] = final
                self.document["final_location_status"] = _location_status(
                    final.get("site_city"), final.get("site_state")
                )

        if event == "exception":
            exc = arg[1] if isinstance(arg, tuple) and len(arg) > 1 else None
            if exc is not None:
                self.document["error"] = str(exc)
                if (
                    self.canonical_game_id in str(exc)
                    and "partial canonical city/state" in str(exc)
                ):
                    self.document["integrity"] = {
                        "status": "FAIL",
                        "check": "canonical_city_state_atomicity",
                        "error": str(exc),
                        "canonical": deepcopy(
                            self.document.get("canonical_last_observed", {})
                        ),
                    }
        elif event == "return" and "integrity" not in self.document:
            final_status = self.document.get("final_location_status")
            if final_status:
                self.document["integrity"] = {
                    "status": "PASS" if final_status != "partial" else "FAIL",
                    "check": "canonical_city_state_atomicity",
                    "canonical": deepcopy(
                        self.document.get("canonical_last_observed", {})
                    ),
                }

    def _trace_site_sync(self, frame: FrameType, event: str, arg: Any) -> None:
        local = frame.f_locals
        canonical = local.get("canonical")
        if not isinstance(canonical, dict):
            return
        if canonical.get("canonical_game_id") != self.canonical_game_id:
            return

        key = id(frame)
        if event == "call":
            self._sync_initial[key] = {
                "source": deepcopy(local.get("source", {})),
                "canonical_before": deepcopy(canonical),
            }
            return

        if event not in {"return", "exception"}:
            return

        initial = self._sync_initial.pop(key, {})
        source = local.get("source", {})
        venue = local.get("venue", {})
        source_status = local.get("source_location_status")
        registry_status = local.get("registry_location_status")
        site = str(initial.get("canonical_before", {}).get("site_type") or "")

        if site == "UNKNOWN":
            branch = "UNKNOWN_CLEAR"
        elif (
            canonical.get("venue_key")
            and canonical.get("venue_id")
            and registry_status == "complete"
        ):
            branch = "REGISTRY_LOCATION"
        elif source_status == "complete":
            branch = "SOURCE_LOCATION"
        else:
            branch = "CLEAR_INCOMPLETE_LOCATION"

        event_doc = {
            "decision": deepcopy(self._current_decision),
            "source_game_id": str(source.get("source_game_id") or ""),
            "source_location_status": source_status,
            "registry_location_status": registry_status,
            "resolved_venue": deepcopy(venue) if isinstance(venue, dict) else {},
            "branch": branch,
            "canonical_before": initial.get("canonical_before", {}),
            "canonical_after": deepcopy(canonical),
        }
        if event == "exception":
            exc = arg[1] if isinstance(arg, tuple) and len(arg) > 1 else None
            event_doc["error"] = str(exc) if exc is not None else "sync failed"
        self.document["site_sync_events"].append(event_doc)

    def _finalize_classification(self) -> None:
        before = self.document.get("canonical_before", {})
        after = self.document.get("canonical_last_observed", {})
        before_status = _location_status(
            before.get("site_city"), before.get("site_state")
        ) if before else ""
        after_status = _location_status(
            after.get("site_city"), after.get("site_state")
        ) if after else ""
        self.document["initial_location_status"] = before_status
        self.document["final_location_status"] = after_status

        location_mutated = any(
            event.get("row_kind") == "canonical"
            and bool({"site_city", "site_state"} & set(event.get("changes", {})))
            for event in self.document.get("mutations", [])
        )
        if after_status != "partial":
            classification = "FINAL_LOCATION_NOT_PARTIAL"
        elif before_status != "partial":
            classification = "INTRODUCED_DURING_RECONCILIATION"
        elif location_mutated:
            classification = "PREEXISTING_MUTATED_STILL_PARTIAL"
        else:
            classification = "PREEXISTING_PERSISTED"
        self.document["partial_location_classification"] = classification

        if self._last_sources:
            self.document["target_source_rows_last_observed"] = [
                deepcopy(self._last_sources[key]) for key in sorted(self._last_sources)
            ]
        if self._last_assertions:
            self.document["linked_assertions_last_observed"] = [
                deepcopy(self._last_assertions[key]) for key in sorted(self._last_assertions)
            ]
