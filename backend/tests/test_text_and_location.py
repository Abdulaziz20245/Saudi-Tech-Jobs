import pytest

from collector.location import is_saudi
from collector.models import RawPosting
from collector.text import content_hash, detect_language, html_to_text


def posting(location="", country=None):
    return RawPosting(
        source="lever",
        source_job_id="1",
        title="t",
        apply_url="u",
        location_raw=location,
        country_code=country,
    )


@pytest.mark.parametrize(
    "location",
    [
        "Riyadh",
        "Al Khobar, Eastern Province",
        "Jeddah | Remote",
        "KSA",
        "الرياض، السعودية",
        "NEOM",
        "Dhahran, Saudi Arabia",
    ],
)
def test_saudi_locations(location):
    assert is_saudi(posting(location))


@pytest.mark.parametrize("location", ["Dubai, UAE", "Cairo", "Remote", "Hailey, Idaho", ""])
def test_non_saudi_locations(location):
    assert not is_saudi(posting(location))


def test_country_code_wins():
    assert is_saudi(posting("Remote", country="sa"))


def test_html_to_text_keeps_structure():
    text = html_to_text("<p>Hello&nbsp;there</p><ul><li>Python</li><li>SQL</li></ul>")
    assert text == "Hello there\n\n- Python\n\n- SQL"


def test_html_to_text_unescapes_greenhouse_content():
    assert html_to_text("&lt;p&gt;Go &amp;amp; Rust&lt;/p&gt;") == "Go & Rust"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Senior Python Developer", "en"),
        ("مهندس برمجيات أول", "ar"),
        ("مهندس برمجيات Python Django React", "mixed"),
        ("", "en"),
    ],
)
def test_detect_language(text, expected):
    assert detect_language(text) == expected


def test_content_hash_changes_with_content():
    assert content_hash("a", "b", "c") == content_hash("a", "b", "c")
    assert content_hash("a", "b", "c") != content_hash("a", "b2", "c")
