from typing import Optional

from sqlalchemy import Column, Enum
from sqlmodel import Field, JSON, TEXT

from app.libs.types import Timestamp
from app.models.base_model import BaseModel, TimeStampMixin, PrimaryKeyMixin


class Run(BaseModel, PrimaryKeyMixin, TimeStampMixin, table=True):
    instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))
    model: str = Field(default=None)
    status: str = Field(
        default="queued",
        sa_column=Column(
            Enum(
                "cancelled",
                "cancelling",
                "completed",
                "expired",
                "failed",
                "in_progress",
                "queued",
                "requires_action",
            ),
            default="queued",
            nullable=True,
        ),
    )
    assistant_id: str = Field(nullable=False)
    thread_id: str = Field(default=None, nullable=False)
    object: str = Field(nullable=False, default="thread.run")
    file_ids: Optional[list] = Field(default=[], sa_column=Column(JSON))
    metadata_: Optional[dict] = Field(default={}, sa_column=Column("metadata", JSON))
    last_error: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    required_action: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tools: Optional[list] = Field(default=[], sa_column=Column(JSON))
    started_at: Optional[Timestamp] = Field(default=None)
    completed_at: Optional[Timestamp] = Field(default=None)
    cancelled_at: Optional[Timestamp] = Field(default=None)
    expires_at: Optional[Timestamp] = Field(default=None)
    failed_at: Optional[Timestamp] = Field(default=None)
    additional_instructions: Optional[str] = Field(default=None, max_length=32768, sa_column=Column(TEXT))


class RunRead(Run):
    pass


class RunCreate(BaseModel):
    assistant_id: str
    status: str = "queued"
    instructions: str = None
    additional_instructions: str = None
    model: str = None
    file_ids: Optional[list] = []
    metadata_: Optional[dict] = Field(default={}, alias="metadata")
    tools: Optional[list] = []


class RunUpdate(BaseModel):
    tools: Optional[list] = []
    metadata_: Optional[dict] = Field(alias="metadata")
