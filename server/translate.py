from typing import List

import httpx
import os
from dotenv import load_dotenv

import schemas


class Translator:
    client: httpx.Client
    key: str
    endpoint: str
    location: str

    def __init__(self):
        self.setup()

    def setup(self):
        load_dotenv()
        key = os.environ["KEY"]
        self.endpoint = os.environ["ENDPOINT"]
        location = os.environ["LOCATION"]
        self.client = httpx.Client(
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Ocp-Apim-Subscription-Region": location,
                "Content-type": "application/json",
            },
            base_url=self.endpoint,
        )

    def translate(self, text: schemas.Text):
        path = "/translate?api-version=3.0"
        target_language_parameter = "&to=" + text.language
        constructed_url = path + target_language_parameter
        body = [{"text": t} for t in text.text]
        translator_request = self.client.post(constructed_url, json=body)
        return translator_request

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
