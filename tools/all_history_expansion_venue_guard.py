#!/usr/bin/env python3
"""Generic physical-venue identity pre-registration guard for expansion.

Use only the newly introduced school venue supports; inherited venue
relationships are immutable accepted authority. A current-global exact key
may be reused only when geography is consistent. A name or historical alias
of a *different* registered key is a conflict/reconciliation question even
when locality agrees: similarity is not historical physical-identity consent.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from stage_research_portfolio import normalize_name, normalize_jurisdiction


class ExpansionVenueConflict(ValueError):
    """Unsettled shared physical-venue identity; registration forbidden."""


def _locality(row: dict[str,str]) -> tuple[str,str]:
    return (
        (row.get("city") or "").strip().casefold(),
        normalize_jurisdiction(row.get("state") or ""),
    )


def _names(row: dict[str,str]) -> set[str]:
    labels=[row.get("canonical_name","")]
    labels.extend(x.strip() for x in (row.get("aliases") or "").split(";"))
    return {n for x in labels if (n:=normalize_name(x))}


def census(
    new_school_venues: list[dict[str,str]],
    global_venues: list[dict[str,str]],
    global_venue_names: list[dict[str,str]],
) -> dict[str,Any]:
    """Return every duplicate/alias/geography conflict, no exception hides rows.

    A precise disagreement is recorded, not arbitrated. A guard with any
    blocker is unsuitable for a live transaction, even if the ordinary
    name/geography auto-rebaser would suggest a new registry ID.
    """
    by_id: dict[str,list[dict[str,str]]] = defaultdict(list)
    by_key: dict[str,list[dict[str,str]]] = defaultdict(list)
    alias_by_name: dict[str,set[str]] = defaultdict(set)
    alias_rows: dict[tuple[str,str],list[dict[str,str]]] = defaultdict(list)
    for row in global_venues:
        vid=row.get("venue_id","").strip()
        key=row.get("venue_key","").strip()
        if vid:
            by_id[vid].append(row)
            alias_by_name[normalize_name(row.get("display_name",""))].add(vid)
        if key:
            by_key[key].append(row)
    for row in global_venue_names:
        label=normalize_name(row.get("venue_name","") or row.get("normalized_name",""))
        vid=row.get("venue_id","").strip()
        if label and vid:
            alias_by_name[label].add(vid)
            alias_rows[(vid,label)].append(row)
    conflicts: list[dict[str,Any]] = []
    classification: list[dict[str,Any]] = []
    seen_keys:set[str]=set()
    for local in new_school_venues:
        key=local.get("venue_key","").strip()
        labels=_names(local)
        if not key or not labels:
            conflicts.append({"class":"VENUE_NEW_SUPPORT_IDENTITY_INCOMPLETE",
                              "venue_key":key})
            continue
        if key in seen_keys:
            conflicts.append({"class":"VENUE_NEW_SUPPORT_DUPLICATE_KEY",
                              "venue_key":key})
        seen_keys.add(key)
        expected_key_rows=by_key.get(key,[])
        if len(expected_key_rows)>1:
            conflicts.append({"class":"VENUE_GLOBAL_DUPLICATE_KEY",
                              "venue_key":key,
                              "global_ids":sorted({x.get("venue_id","") for x in expected_key_rows})})
        same_key_id=expected_key_rows[0].get("venue_id","") if len(expected_key_rows)==1 else ""
        if same_key_id:
            registered=expected_key_rows[0]
            if _locality(registered)!=_locality(local):
                conflicts.append({
                    "class":"VENUE_EXACT_KEY_LOCALITY_CONFLICT",
                    "venue_key":key,
                    "local_city":local.get("city",""),
                    "local_state":local.get("state",""),
                    "global_venue_id":same_key_id,
                    "registered_city":registered.get("city",""),
                    "registered_state":registered.get("state",""),
                })
        matches=set()
        for name in labels:
            matches.update(alias_by_name.get(name,set()))
        for vid in sorted(matches):
            registered=by_id.get(vid,[])
            if len(registered)!=1:
                conflicts.append({"class":"VENUE_GLOBAL_IDENTITY_AMBIGUOUS",
                                  "venue_key":key,"global_venue_id":vid})
                continue
            row=registered[0]
            if row.get("venue_key","") == key:
                continue
            matching_labels=sorted(n for n in labels
                                   if vid in alias_by_name.get(n,set()))
            historical=sorted({x.get("name_type","") for n in matching_labels
                         for x in alias_rows.get((vid,n),[])})
            conflicts.append({
                "class":"VENUE_POTENTIAL_EXISTING_PHYSICAL_IDENTITY",
                "venue_key":key,
                "proposed_name":local.get("canonical_name",""),
                "local_city":local.get("city",""),
                "local_state":local.get("state",""),
                "global_venue_id":vid,
                "registered_key":row.get("venue_key",""),
                "registered_name":row.get("display_name",""),
                "registered_city":row.get("city",""),
                "registered_state":row.get("state",""),
                "matching_normalized_names":matching_labels,
                "registered_alias_types":historical,
                "locality_agrees":_locality(local)==_locality(row),
            })
        classification.append({
            "venue_key":key,
            "existing_key_reuse_id":same_key_id,
            "possible_existing_global_ids":sorted(matches),
            "registration_safe":not any(x.get("venue_key")==key for x in conflicts),
        })
    return {"schema_version":1,
            "status":"BLOCKED_VENUE_IDENTITY_RECONCILIATION" if conflicts else "PASS",
            "new_support_count":len(new_school_venues),
            "blocker_count":len(conflicts),
            "blockers":conflicts,
            "rows":classification}


def require_clean(census_result: dict[str,Any]) -> dict[str,Any]:
    if census_result.get("status")!="PASS" or census_result.get("blocker_count")!=0:
        raise ExpansionVenueConflict(
            "VENUE_IDENTITY_RECONCILIATION_REQUIRED:"
            + ",".join(sorted({r["venue_key"] for r in census_result["blockers"]}))
        )
    return census_result
