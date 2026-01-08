from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import ConfigDict, field_validator
import uuid
from datetime import datetime
from sqlmodel import Relationship


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationships to related models
    tasks: list["Task"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")
    messages: list["Message"] = Relationship(back_populates="user")


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user and messages
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="messages")
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


# Request models for API
class UserCreate(SQLModel):
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserResponse(SQLModel):
    id: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        extra='ignore',
        validate_assignment=True,
        str_strip_whitespace=True
    )

    @field_validator('title', mode='before')
    @classmethod
    def validate_title(cls, v):
        if v is None or v == "":
            return None
        return str(v)

    @field_validator('completed', mode='before')
    @classmethod
    def validate_completed(cls, v):
        if v is None:
            return None
        return bool(v)


class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class ConversationCreate(SQLModel):
    pass  # Empty for now, as conversation_id is optional in chat endpoint


class ConversationResponse(SQLModel):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(SQLModel):
    conversation_id: int
    role: str
    content: str


class MessageResponse(SQLModel):
    id: int
    user_id: str
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(SQLModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(SQLModel):
    conversation_id: int
    response: str
    tool_calls: Optional[list] = []

    model_config = ConfigDict(from_attributes=True)


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    user_id: str
    email: str