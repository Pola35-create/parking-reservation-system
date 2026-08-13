from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    can_use_electric: Mapped[bool] = mapped_column(default=False, nullable=False)
    can_use_accessible: Mapped[bool] = mapped_column(default=False, nullable=False)
    can_use_dedicated: Mapped[bool] = mapped_column(default=False, nullable=False)