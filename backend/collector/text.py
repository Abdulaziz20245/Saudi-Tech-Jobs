"""Text helpers: HTML to plain text, language detection, content hashing."""

import hashlib
import html
import re
from html.parser import HTMLParser

_BLOCK_TAGS = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}
_ARABIC = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
_LATIN = re.compile(r"[A-Za-z]")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "li":
            self.parts.append("\n- ")
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_text(raw: str | None) -> str:
    """Convert (possibly entity-escaped) HTML to readable plain text."""
    if not raw:
        return ""
    # Greenhouse returns HTML that is itself entity-escaped (&lt;p&gt;...).
    if "&lt;" in raw and "<" not in raw:
        raw = html.unescape(raw)
    parser = _TextExtractor()
    parser.feed(raw)
    text = "".join(parser.parts).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def detect_language(text: str) -> str:
    """Return 'ar', 'en' or 'mixed' based on the share of Arabic vs Latin letters."""
    arabic = len(_ARABIC.findall(text))
    latin = len(_LATIN.findall(text))
    total = arabic + latin
    if total == 0:
        return "en"
    share = arabic / total
    if share >= 0.8:
        return "ar"
    if share <= 0.1:
        return "en"
    return "mixed"


def content_hash(title: str, description_text: str, location_raw: str) -> str:
    payload = "\x1f".join((title.strip(), description_text.strip(), location_raw.strip()))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
