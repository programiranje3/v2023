"""
LAB 6, enums
"""

from enum import Enum

"""
The FlightService enumeration defines various kinds of services that can be offered to passengers, 
plus an item for cases when services are not specified.
"""

class FlightService(Enum):
    SNACK = 'snack'
    REFRESHMENTS = 'refreshments'
    MEAL = 'meal'
    PRIORITY_BOARDING = 'priority boarding'
    ONBOARD_WIFI = 'onboard wifi'
    ONBOARD_MEDIA = 'onboard media'
    UNSPECIFIED = 'unspecified'

    @staticmethod
    def valid_service_str(str_value):
        return any([str_value in [s.value, s.name] for s in FlightService])

    @staticmethod
    def get_service_from_str(str_value):
        for s in FlightService:
            if str_value in [s.name, s.value]:
                return s
        return None
