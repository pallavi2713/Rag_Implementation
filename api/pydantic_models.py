from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    GEMINI_2_FLASH = "gemini-2.0-flash"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GEMINI_2_FLASH)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int