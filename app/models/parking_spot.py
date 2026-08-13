from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.enums.parking_spot_type import ParkingSpotType

class ParkingSpot(Base):
    __tablename__ = "parking_spot"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    spot_name: Mapped[str] = mapped_column(String(4), nullable=False, unique=True)
    type: Mapped[ParkingSpotType] = mapped_column(SQLEnum(ParkingSpotType), default=ParkingSpotType.STANDARD, nullable=False)