from workbench import run_workbench


def test_run_workbench_coordinates_pipeline(monkeypatch, tmp_path):
    calls = {}

    def fake_initialize():
        calls["initialized"] = True

    def fake_register_task(**kwargs):
        calls["task_details"] = kwargs
        return "fake_task"

    def fake_clone_repo(repo_url, workspace):
        calls["clone"] = (repo_url, workspace)
        return str(tmp_path / "repo")

    def fake_execute_task(task, repo_root):
        calls["execute"] = (task, repo_root)
        return "fake_result"

    monkeypatch.setattr("workbench.initialize_workbench", fake_initialize)
    monkeypatch.setattr(
        "workbench.create_and_register_task",
        fake_register_task,
    )
    monkeypatch.setattr("workbench.clone_repo", fake_clone_repo)
    monkeypatch.setattr("workbench.execute_task", fake_execute_task)

    result = run_workbench(
        repo_url="https://github.com/example/repo.git",
        workspace=str(tmp_path / "workspace" / "repo"),
        task_id="task-1",
        description="Add input validation",
        allowed_files=["app.py"],
        acceptance=["Invalid input is rejected"],
        forbidden_files=["secrets.env"],
    )

    assert result == "fake_result"
    assert calls["initialized"] is True
    assert calls["task_details"]["task_id"] == "task-1"
    assert calls["task_details"]["allowed_files"] == ["app.py"]
    assert calls["task_details"]["forbidden_files"] == ["secrets.env"]
    assert calls["clone"][0] == "https://github.com/example/repo.git"
    assert calls["execute"] == ("fake_task", str(tmp_path / "repo"))