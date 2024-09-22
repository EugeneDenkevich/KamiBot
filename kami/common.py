from pathlib import Path


def get_work_dir() -> Path:
    """Get project work dir"""

    return Path(__file__).parent


def get_prompt(prompt_file: str) -> str:
    """
    Get prompt by file name.

    :param prompt_file: File with prompt.
    """

    promt_path = get_work_dir() / "prompts" / prompt_file
    with open(promt_path, encoding="utf-8") as f:
        return f.read()
