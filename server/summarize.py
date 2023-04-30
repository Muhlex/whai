import os
import schemas
import cohere
from dotenv import load_dotenv


def summarize(report: schemas.SummarizeRequest):
	load_dotenv()
	key = os.environ['COHERE_KEY']
	co = cohere.Client(key)
	response = co.summarize(
		text=report.text,
		length=str(report.length.value),
		format='bullets',
		model='summarize-xlarge',
		additional_command='stay with the industry specific words',
		temperature=0.7,
	)
	return response
