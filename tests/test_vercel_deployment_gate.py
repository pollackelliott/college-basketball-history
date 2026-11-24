from tools.vercel_deployment_gate import should_skip


def test_main_always_deploys():
    assert should_skip(ref="main", parent_available=True, site_diff_returncode=0) is False


def test_data_publication_branch_always_deploys():
    assert should_skip(
        ref="data/kentucky-onboarding",
        parent_available=False,
        site_diff_returncode=2,
    ) is False


def test_maintenance_publication_branch_always_deploys():
    assert should_skip(
        ref="maintenance/shared-reference-publication",
        parent_available=False,
        site_diff_returncode=2,
    ) is False


def test_non_publication_branches_always_skip():
    for ref in (
        "control/remote-implementation",
        "tooling/stage2-repair",
        "research/hawai-i-stage7",
        "control-center/maintenance",
        "transport/freeze",
        "hardening/tooling",
        "docs/update",
        "feature/site-change",
    ):
        assert should_skip(
            ref=ref,
            parent_available=True,
            site_diff_returncode=1,
        ) is True
