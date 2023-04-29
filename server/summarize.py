import os

import cohere
from dotenv import load_dotenv


def summarize(text: str):
	load_dotenv()
	key = os.environ['COHERE_KEY']
	co = cohere.Client(key)  # This is your trial API key
	response = co.summarize(
		text=text,
		length='auto',
		format='bullets',
		model='summarize-xlarge',
		additional_command='stay with the industry specific words',
		temperature=0.7,
	)
	return response
