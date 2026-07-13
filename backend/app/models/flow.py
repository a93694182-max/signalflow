from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from __future__ import annotations


class Flow(Base):
    __tablename__ = "flows"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_asset: Mapped[str] = mapped_column(String(50), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    nodes: Mapped[list["FlowNode"]] = relationship(
        back_populates="flow",
        cascade="all, delete-orphan",
        order_by="FlowNode.order_index",
    )