from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FlowLink(Base):
    __tablename__ = "flow_links"

    __table_args__ = (
        UniqueConstraint(
            "source_flow_id",
            "target_flow_id",
            "relation_type",
            name="uq_flow_link_relation",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    source_flow_id: Mapped[int] = mapped_column(
        ForeignKey(
            "flows.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    target_flow_id: Mapped[int] = mapped_column(
        ForeignKey(
            "flows.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    relation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    source_flow: Mapped["Flow"] = relationship(
        foreign_keys=[source_flow_id],
        back_populates="outgoing_links",
    )

    target_flow: Mapped["Flow"] = relationship(
        foreign_keys=[target_flow_id],
        back_populates="incoming_links",
    )