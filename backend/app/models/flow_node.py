from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class FlowNode(Base):
    __tablename__ = "flow_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    flow_id: Mapped[int] = mapped_column(
        ForeignKey("flows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    evidence_level: Mapped[str] = mapped_column(
        String(20),
        default="moderate",
        nullable=False,
    )

    flow: Mapped["Flow"] = relationship(back_populates="nodes")
    evidences: Mapped[list["Evidence"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan",
    )