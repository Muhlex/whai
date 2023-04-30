import os
import openai
from dotenv import load_dotenv


def evaluate_translation(original, translation):
	load_dotenv()

	openai.api_key = os.environ["OPENAI_API_KEY"]

	prompt = f'''Rate the machine translation of:
                 {original}
                 to:
                 {translation}
                 on a scale of 1 to 100. Just the number.'''

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "user", "content": prompt}
		]
	)

	return completion.choices[0].message.content


def translate_chat_gpt(original: str, lang: str):
	load_dotenv()

	openai.api_key = os.environ["OPENAI_API_KEY"]

	prompt = f'''Translate the given text to {lang},
	text: {original}'''

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "user", "content": prompt}
		]
	)

	return completion
