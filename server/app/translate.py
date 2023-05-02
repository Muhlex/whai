from typing import List

import httpx
import os
from fastapi import HTTPException

from . import schemas
from .evaluate import OpenAiWrapper


class Translator:
    client: httpx.Client
    openai_wrapper: OpenAiWrapper

    def __init__(self):
        self.setup()
        self.openai_wrapper = OpenAiWrapper()

    def setup(self):
        self.client = httpx.Client(
            headers={
                "Ocp-Apim-Subscription-Key": os.environ["KEY"],
                "Ocp-Apim-Subscription-Region": os.environ["LOCATION"],
                "Content-type": "application/json",
            },
            base_url=os.environ["ENDPOINT"],
        )

    def _azure_translate(self, text: schemas.Text) -> schemas.AzureTranslationResponse:
        path = "/translate?api-version=3.0"
        target_language_parameter = "&to=" + text.language
        constructed_url = path + target_language_parameter
        body = [{"text": t} for t in text.texts]
        response = self.client.post(constructed_url, json=body)
        if response.status_code != 200:
            # todo logging
            raise HTTPException(status_code=500, detail="Azure Translation Failed")
        return schemas.AzureTranslationResponse(**response.json()[0])

    def detect(self, texts: List[str]):
        analysis_input = schemas.AnalysisInput(
            documents=list(
                [
                    schemas.Document(id=index, text=text)
                    for index, text in enumerate(texts)
                ]
            )
        )

        body = schemas.DetectBody(
            kind="LanguageDetection",
            parameters=schemas.Parameters(modelVersion="latest"),
            analysisInput=analysis_input,
        )
        print(body.json())
        url = "language/:analyze-text?api-version=2022-05-01"
        print(url)
        return self.client.post(url=url, data=body.json())

    def translate(self, text: schemas.Text, emoji: bool) -> schemas.TranslationResponse:
        azure_response = self._azure_translate(text=text)
        openai_response = self.openai_wrapper.translate_chat_gpt(text=text, emoji=emoji)
        score = self.openai_wrapper.evaluate_translation(
            original=text.text, translation=azure_response.text
        )
        try:
            score = int(score.text)
        except ValueError:
            score = -1
        return schemas.TranslationResponse(
            **{
                "original_text": text.text,
                "azure_translation": azure_response.text,
                "chat_gpt_translation": openai_response.text,
                "score": score,
            }
        )
