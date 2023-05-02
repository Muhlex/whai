import functools
import os
from typing import Callable

import openai
from . import schemas


def retry(n: int) -> Callable:
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, count=0, *args, **kwargs) -> Callable:
            retries = count
            try:
                return func(self, *args, **kwargs)
            except openai.error.Timeout as e:
                if retries > n:
                    raise e
                retries += 1
                return wrapper(self, retries, *args, **kwargs)

        return wrapper

    return decorator


class OpenAiWrapper:
    timeout: int

    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.setup()

    def setup(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

    @retry(n=3)
    def evaluate_translation(self, original, translation) -> schemas.OpenAIResponse:
        prompt = f"""Rate the machine translation of: {original} to: {translation} on a scale of 1 to 100. Just the number."""
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            request_timeout=self.timeout,
        )
        ai_translate = schemas.OpenAIResponse(**completion)
        return ai_translate

    @retry(n=3)
    def translate_chat_gpt(
            self, text: schemas.Text, emoji: bool
    ) -> schemas.OpenAIResponse:
        prompt = f"""
        I want you to act as an {text.language} translator, spelling corrector and improver.
        I will speak to you in any language and you will detect the language, translate it and answer in the corrected
        and improved version of my text, in {text.language}. I want you to replace my simplified A0-level words and sentences with
        more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary.
        I want you to only reply the correction, the improvements and nothing else, do not write explanations.
        My first sentence is '{text.text}'
        """

        if emoji:
            prompt = f"""
        I want you to translate the sentences I wrote into emojis. I will write the sentence, and you will express it with
        emojis. I just want you to express it with emojis. I don't want you to reply with anything but emoji. When I need
        to tell you something in English, I will do it by wrapping it in curly brackets like {{like this}}. {text.text}"
        """
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            request_timeout=self.timeout,
        )
        ai_translate = schemas.OpenAIResponse(**completion)
        return ai_translate

    @retry(n=3)
    def transcribe_audio(self, filename: str) -> str:
        with open(filename, "rb") as file:
            transcript = openai.Audio.transcribe(model="whisper-1", filename=file, request_timeout=self.timeout)
        return transcript["text"]
