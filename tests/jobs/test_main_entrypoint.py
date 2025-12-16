import pytest
from main import main

def test_main_unknown_job_exits(mocker):
    mocker.patch("sys.argv", ["main.py", "--job", "unknown"])
    mocker.patch("job_registry.JOB_REGISTRY", {})

    with pytest.raises(SystemExit):
        main()
