from typing import List

from pydantic import BaseModel


class Text(BaseModel):
	text: List[str]
	language: str


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
