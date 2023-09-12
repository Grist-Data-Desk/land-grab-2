from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Parcel:
    normalized_number: Optional[str] = None
    original_number: Optional[str] = None
    county: Optional[str] = None
    alt_county_parcel: Optional[str] = None

    def to_dict(self):
        return asdict(self)
