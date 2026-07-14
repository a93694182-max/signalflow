from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidences"

    id: Mapped[int] = mapped_column(primary_key=True)
    flow_node_id: Mapped[int] = mapped_column(
        ForeignKey("flow_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    relation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    impact_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    reliability_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    node: Mapped["FlowNode"] = relationship(back_populates="evidences")