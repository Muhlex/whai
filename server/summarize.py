import cohere


def summarize(text: str):
	co = cohere.Client('V7K5ms3A0i22LChge8R0sAotQSG4SbPHYpL6MJEa')  # This is your trial API key
	response = co.summarize(
		text=text,
		length='auto',
		format='bullets',
		model='summarize-xlarge',
		additional_command='stay with the industry specific words',
		temperature=0.7,
	)
	return response
