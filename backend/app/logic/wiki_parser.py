import re
from typing import List

WIKI_LINK_REGEX = re.compile(r"\[\[(.*?)\]\]")
BRACKET_TAG_REGEX = re.compile(r"\[#([a-zA-Z0-9_\-]+)\]|\[\[#([a-zA-Z0-9_\-]+)\]\]|\[\[tag:([a-zA-Z0-9_\-]+)\]\]|\[tag:([a-zA-Z0-9_\-]+)\]")
HASHTAG_REGEX = re.compile(r"(?:^|\s)#([a-zA-Z0-9_\-]{2,})")

def extract_wiki_links(content: str) -> List[str]:
    """
    Extracts all bracketed note titles from markdown content, e.g. [[Note B]].
    Returns list of cleaned, non-empty title strings.
    """
    if not content:
        return []
    matches = WIKI_LINK_REGEX.findall(content)
    cleaned = []
    for match in matches:
        title = match.strip()
        # If it starts with '#' or 'tag:', it's an inline tag, not a note link
        if title.startswith("#") or title.lower().startswith("tag:"):
            continue
        if title and title not in cleaned:
            cleaned.append(title)
    return cleaned

def extract_inline_tags(text: str) -> List[str]:
    """
    Extracts tags written directly in brackets or hashtags in text:
    Examples: [[#ai]], [#productivity], [[tag:ml]], #machine-learning
    """
    if not text:
        return []
    tags = []

    # 1. Bracket tags [#tag], [[#tag]], [[tag:xyz]], [tag:xyz]
    bracket_matches = BRACKET_TAG_REGEX.findall(text)
    for group in bracket_matches:
        for item in group:
            if item:
                tag = item.strip().lower()
                if tag and tag not in tags:
                    tags.append(tag)

    # 2. Inline hashtags #tag
    hash_matches = HASHTAG_REGEX.findall(text)
    for h in hash_matches:
        tag = h.strip().lower()
        if tag and tag not in tags:
            tags.append(tag)

    return tags
