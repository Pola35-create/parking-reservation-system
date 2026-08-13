from datetime import datetime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.enums.reservation_status import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=False)
    parking_spot_id: Mapped[int] = mapped_column(ForeignKey("parking_spot.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(SQLEnum(ReservationStatus), default=ReservationStatus.RESERVED, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    parking_spot = relationship("ParkingSpot", back_populates="reservations")
    person = relationship("Person", back_populates="reservations")