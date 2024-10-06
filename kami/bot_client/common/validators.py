import re
from typing import Match


def clean_tags(text: str) -> str:
    """
    Remove tags that not supported by Telegram.

    :param text: Text with tags.
    :return: Text without invalid tags.
    """

    tag_pattern = re.compile(r"</?([a-zA-Z0-9]+)(?:\s[^>]*)?>")

    def replace_tags(match: Match[str]) -> str:
        """
        Replace invalid tags or remove attributes from valid tags.

        :param match: A regex match object that represents a tag.
        :return: The original tag if valid and without attributes, or an empty string.
        """

        tag_name = match.group(1).lower()

        if tag_name in {"b", "i", "u", "s", "a", "code", "pre"}:
            if match.group(0).startswith("</"):
                return f"</{tag_name}>"
            return f"<{tag_name}>"
        return ""

    return re.sub(tag_pattern, replace_tags, text)
