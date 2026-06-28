from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Expression(Base):
    __tablename__ = 'expressions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    expression: Mapped[String] = mapped_column(String, nullable=True)
    expression_type: Mapped[Optional[String]] = mapped_column(String)
    derivatives: Mapped[String] = mapped_column(String)
    roots: Mapped[String] = mapped_column(String)
    domain: Mapped[String] = mapped_column(String)
    range: Mapped[String] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 default=lambda: datetime.now(timezone.utc)
                                                 ) 