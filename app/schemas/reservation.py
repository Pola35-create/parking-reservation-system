from datetime import datetime
from pydantic import BaseModel
from app.enums.reservation_status import ReservationStatus

class ReservationCreate(BaseModel):
    person_id: int
    parking_spot_id: int
    start_time: datetime
    end_time: datetime

class ReservationResponse(BaseModel):
    id: int
    person_id: int
    parking_spot_id: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }