from tools.vercel_deployment_gate import should_skip


def test_main_always_deploys():
    assert should_skip(ref="main", parent_available=True, site_diff_returncode=0) is False


def test_control_branch_always_skips():
    assert should_skip(
        ref="control/remote-implementation",
        parent_available=False,
        site_diff_returncode=2,
    ) is True


def test_data_publication_branch_deploys_exact_head_without_last_commit_site_delta():
    assert should_skip(
        ref="data/kentucky-onboarding",
        parent_available=True,
        site_diff_returncode=0,
    ) is False


def test_maintenance_publication_branch_deploys_exact_head_without_last_commit_site_delta():
    assert should_skip(
        ref="maintenance/shared-reference-publication",
        parent_available=True,
        site_diff_returncode=0,
    ) is False


def test_other_branch_still_skips_when_last_commit_has_no_site_delta():
    assert should_skip(
        ref="feature/non-site-change",
        parent_available=True,
        site_diff_returncode=0,
    ) is True


def test_other_branch_deploys_when_last_commit_changes_site():
    assert should_skip(
        ref="feature/site-change",
        parent_available=True,
        site_diff_returncode=1,
    ) is False


def test_uncertain_diff_fails_open():
    assert should_skip(
        ref="feature/uncertain",
        parent_available=True,
        site_diff_returncode=2,
    ) is False
