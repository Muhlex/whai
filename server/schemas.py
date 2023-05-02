from enum import Enum
from typing import List

from pydantic import BaseModel


class Pdf(BaseModel):
    report: str


class TranslationResponse(BaseModel):
    original_text: str
    chat_gpt_translation: str
    azure_translation: str
    score: int


class Text(BaseModel):
    text: str
    language: str

    @property
    def texts(self) -> List[str]:
        return self.text.split(".!?")


class SummarizeLength(Enum):
    AUTO = "auto"
    SHORT = "short"
    MEDIUM = "medium"
    LARGE = "long"


class SummarizeRequest(BaseModel):
    text: str
    length: SummarizeLength


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


class Message(BaseModel):
    content: str
    role: str


class Choice(BaseModel):
    finish_reason: str
    index: int
    message: Message


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class OpenAIResponse(BaseModel):
    choices: List[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage

    @property
    def text(self) -> str:
        return [x.message.content for x in self.choices][0]


class AzureDetectedLanguage(BaseModel):
    language: str
    score: float


class AzureTranslation(BaseModel):
    text: str
    to: str


class AzureTranslationResponse(BaseModel):
    detectedLanguage: AzureDetectedLanguage
    translations: List[AzureTranslation]

    @property
    def text(self) -> str:
        return " ".join(map(lambda t: t.text, self.translations))


class AzureTranslationResponseList(BaseModel):
    __root__: List[AzureTranslationResponse]
