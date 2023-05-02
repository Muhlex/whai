import os
import uuid
import logging

from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
    SpeechRecognitionResult,
)
from fastapi import UploadFile, HTTPException
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

logger = logging.getLogger(__name__)


class Audio:
    config: SpeechConfig

    def __init__(self):
        self.config = SpeechConfig(
            region=os.environ["SPEECH_REGION"], subscription=os.environ["SPEECH_KEY"]
        )

    @staticmethod
    def convert_to_wav(file: UploadFile) -> str:
        """
        Convert an uploaded file to wave format
        :param file: the file you want to convert to wave
        :return: the path/name os the wave file
        """
        name = f"{uuid.uuid4().hex}.wav"
        try:
            audio = AudioSegment.from_file_using_temporary_files(file.file)
            audio.export(name, format="wav")
        except (OSError, CouldntDecodeError):
            os.remove(name)
            raise HTTPException(
                status_code=500,
                detail=f"Couldn't decode {file.filename} to wave format",
            )
        return name

    def recognize_from_wav(self, filename: str, source_language: str | None = None):
        if source_language is not None:
            self.config.speech_recognition_language = source_language
        audio_config = AudioConfig(filename=filename)
        speech_recognizer = SpeechRecognizer(
            speech_config=self.config,
            audio_config=audio_config,
            language=source_language,
        )
        result: SpeechRecognitionResult = speech_recognizer.recognize_once_async().get()
        if result.reason == ResultReason.RecognizedSpeech:
            logger.debug(f"Transcription result: {result.text}")
            return result
        if result.reason == ResultReason.NoMatch:
            logger.error(
                f"Error: no match in audio found file: {filename} lang: {source_language}, reason:"
                f"{result.no_match_details}"
            )
            raise HTTPException(status_code=500, detail="No speech could be recognized")
        elif result.reason == ResultReason.Canceled:
            logger.error(
                f"Error: speech to text canceled file: {filename} lang: {source_language}, reason:"
                f" {result.cancellation_details}"
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")
