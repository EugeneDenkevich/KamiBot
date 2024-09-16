from pathlib import Path


def get_work_dir() -> Path:
    return Path(__file__).parent
