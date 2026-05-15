from uuid import uuid4
from datetime import datetime

from sqlmodel import Field, SQLModel


class PublicSubmissions(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    # Changed: UUID -> str, uuid4 -> lambda: str(uuid4())
    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid4()), nullable=False
    )
    submitted_by: str = Field(max_length=128, nullable=True)
    name: str = Field(max_length=128, nullable=True, default=None)
    face_mesh: str = Field(nullable=False)  # JSON string of face mesh landmarks
    location: str = Field(max_length=128, nullable=True)
    city: str = Field(max_length=64, nullable=True, default=None)
    state: str = Field(max_length=64, nullable=True, default=None)
    mobile: str = Field(max_length=10, nullable=False)
    email: str = Field(max_length=64, nullable=True)
    status: str = Field(max_length=16, nullable=False)
    birth_marks: str = Field(max_length=512, nullable=True)
    # Use datetime.now for local time instead of UTC
    submitted_on: datetime = Field(default_factory=datetime.now, nullable=False)


class RegisteredCases(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    # Changed: UUID -> str, uuid4 -> lambda: str(uuid4())
    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid4()), nullable=False
    )
    submitted_by: str = Field(max_length=64, nullable=False)
    name: str = Field(max_length=128, nullable=False)
    father_name: str = Field(max_length=128, nullable=True)
    age: str = Field(max_length=8, nullable=True)
    complainant_name: str = Field(max_length=128)
    complainant_mobile: str = Field(max_length=10, nullable=True)
    complainant_email: str = Field(max_length=128, nullable=True, default=None)
    adhaar_card: str = Field(max_length=12)
    last_seen: str = Field(max_length=64)
    address: str = Field(max_length=512)
    state: str = Field(max_length=64, nullable=True, default=None)
    city: str = Field(max_length=64, nullable=True, default=None)
    description: str = Field(max_length=1024, nullable=True, default=None)
    face_mesh: str = Field(nullable=False)  # JSON string of face mesh landmarks
    # Use datetime.now for local time instead of UTC
    submitted_on: datetime = Field(default_factory=datetime.now, nullable=False)
    status: str = Field(max_length=16, nullable=False)
    birth_marks: str = Field(max_length=512)
    matched_with: str = Field(nullable=True)
