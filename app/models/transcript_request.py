from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    transcript: str