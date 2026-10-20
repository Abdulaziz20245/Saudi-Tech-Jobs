"""Decide whether a posting is located in Saudi Arabia."""

import re

from collector.models import RawPosting

_SAUDI_TERMS = [
    "saudi",
    "ksa",
    "riyadh",
    "jeddah",
    "jiddah",
    "dammam",
    "khobar",
    "dhahran",
    "makkah",
    "mecca",
    "madinah",
    "medina",
    "neom",
    "jubail",
    "yanbu",
    "tabuk",
    "abha",
    "taif",
    "qassim",
    "buraydah",
    "hail",
    "al ula",
    "alula",
    "kafd",
    "السعودية",
    "الرياض",
    "جدة",
    "الدمام",
    "الخبر",
    "الظهران",
    "مكة",
    "المدينة",
    "نيوم",
]
_PATTERN = re.compile(
    "|".join(rf"(?<![a-z]){re.escape(t)}(?![a-z])" for t in _SAUDI_TERMS), re.IGNORECASE
)


def is_saudi(posting: RawPosting) -> bool:
    if posting.country_code and posting.country_code.upper() == "SA":
        return True
    return bool(_PATTERN.search(posting.location_raw))
