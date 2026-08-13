from pydantic import BaseModel
from app.enums.parking_spot_type import ParkingSpotType

class ParkingSpotCreate(BaseModel):
    spot_name: str
    type: ParkingSpotType

class ParkingSpotResponse(BaseModel):
    id: int
    spot_name: str
    type: ParkingSpotType

    model_config = {
        "from_attributes": True
    }