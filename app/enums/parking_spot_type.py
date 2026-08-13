from enum import Enum

class ParkingSpotType(str, Enum):
    STANDARD = "Standard"
    ELECTRIC = "Electric"
    ACCESSIBLE = "Accessible"
    DEDICATED = "Dedicated"