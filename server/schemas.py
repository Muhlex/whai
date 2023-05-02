from enum import Enum
from typing import List

from pydantic import BaseModel


class Pdf(BaseModel):
    report: str


class TranslationResponse(BaseModel):
    chat_gpt_translation: str
    azure_translation: str
    score: int


class Text(BaseModel):
    text: List[str]
    language: str


class SummarizeLength(Enum):
    AUTO = "auto"
    SHORT = "short"
    MEDIUM = "medium"
    LARGE = "long"


class SummarizeRequest(BaseModel):
    text: str
    length: SummarizeLength


class DetectedLanguage(BaseModel):
    language: str
    score: float


class Translation(BaseModel):
    text: str
    to: str


class TranslatedText(BaseModel):
    detectedLanguage: DetectedLanguage
    translations: List[Translation]


class Parameters(BaseModel):
    modelVersion: str


class Document(BaseModel):
    id: str
    text: str


class AnalysisInput(BaseModel):
    documents: List[Document]


class DetectBody(BaseModel):
    kind: str
    parameters: Parameters
    analysisInput: AnalysisInput
