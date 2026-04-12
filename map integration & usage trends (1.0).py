from dataclasses import dataclass, field
from typing import List

class Address:
    def __init__(self, city, suburb, street, number, state, postcode, coordinates):
        self.city = city
        self.suburb = suburb
        self.street = street
        self.number = number
        self.state = state
        self.postcode = postcode
        self.coordinates = coordinates

@dataclass
class YearlyUsageTrend:
    monthly_usage: List[float] = field(default_factory=lambda: [0.0] * 12)

@dataclass
class MonthlyUsageTrend:
    weekly_usage: List[float] = field(default_factory=lambda: [0.0] * 4)

@dataclass
class WeeklyUsageTrend:
    daily_usage: List[float] = field(default_factory=lambda: [0.0] * 7)

@dataclass
class HourlyUsageTrend:
    hourly_usage: List[float] = field(default_factory=lambda: [0.0] * 24)