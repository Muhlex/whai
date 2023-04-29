import os
import uuid
from typing import List
import translate as ts
import speech
import evaluate as ev
from fastapi import FastAPI, HTTPException, UploadFile
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

import schemas
import summarize
import speech

app = FastAPI()
translator = ts.Translator()
english = "en-US"
german = "de-DE"


@app.post("/translate/", response_model=List[schemas.TranslatedText])
async def translate(text: schemas.Text):
	print(text)
	response = translator.translate(text)
	print(response)
	if response is None or response.status_code != 200:
		raise HTTPException(status_code=400, detail="Bad Request")
	result = [schemas.TranslatedText(**x) for x in response.json()]
	print(" ".join(y.text for x in result for y in x.translations))
	return [schemas.TranslatedText(**x) for x in response.json()]


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile, lang: str):
	name = f"{uuid.uuid4().hex}.wav"
	try:
		audio = AudioSegment.from_file_using_temporary_files(file.file)
		audio.export(name, format="wav")

		# extract text
		text_from_audio = speech.recognize_from_wav(wav_path=name, target_language=lang)
	# delete file
	except Exception as e:
		raise HTTPException(status_code=500, detail="Transcribe Failed")
	finally:
		os.remove(name)

	if text_from_audio.reason == speechsdk.ResultReason.RecognizedSpeech:
		lines = text_from_audio.text.split(".!?")
		response = translator.translate(schemas.Text(text=lines, language="en-US"))
		if response is None or response.status_code != 200:
			raise HTTPException(status_code=500, detail="Translation Failed")
		result = [schemas.TranslatedText(**x) for x in response.json()]
		try:
			summery = summarize.summarize(". ".join([t.text for r in result for t in r.translations]))
		except Exception as e:
			raise HTTPException(status_code=500, detail="Summarization Failed")
		content = ev.evaluate_translation(text_from_audio.text, translation=". ".join([t.text for r in result for t in r.translations]))
		print(content)
		return {"filename": file.filename,
						"content_type": file.content_type,
						"content": text_from_audio.text,
						"translation": result,
						"summery": summery}

	# unsuccessful speech to text conversion
	if text_from_audio.reason == speechsdk.ResultReason.NoMatch:
		raise HTTPException(status_code=500, detail="No speech could be recognized")

	# failed before speech to text conversion
	elif text_from_audio.reason == speechsdk.ResultReason.Canceled:
		raise HTTPException(status_code=500, detail="Internal Server Error")
