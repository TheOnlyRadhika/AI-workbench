from unittest.mock import patch
import pytest
from github import clone_repo


def test_invalid_url():
    with pytest.raises(ValueError):
        clone_repo(
            "https://example.com/test.git",
            "workdir/test"
        )

def test_clone_failure():
    fake_result = type(
        "Result",
        (),
        {
            "returncode": 1,
            "stdout": "",
            "stderr": "Repository not found"
        }
    )()
    with patch(
        "github.subprocess.run",
        return_value=fake_result
    ):
        with pytest.raises(RuntimeError):
            clone_repo(
                "https://github.com/user/test.git",
                "workdir/test"
            )

def test_successful_clone():
    fake_result = type(
        "Result",
        (),
        {
            "returncode": 0,
            "stdout": "Cloning into 'test'...",
            "stderr": ""
        }
    )()
    with patch(
        "github.subprocess.run",
        return_value=fake_result
    ):
        with patch(
            "github.Path.exists",
            return_value=False
        ):
            result = clone_repo(
                "https://github.com/user/test.git",
                "workdir/test"
            )
    assert result == "workdir/test"