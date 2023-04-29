import uuid, os
from typing import List
import translate as ts
import speech
from fastapi import FastAPI, HTTPException, UploadFile
from pydub import AudioSegment

import schemas

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
async def create_upload_file(file: UploadFile):
	name = f"{uuid.uuid4().hex}.wav"
	audio = AudioSegment.from_file_using_temporary_files(file.file)
	audio.export(name, format="wav")

	# extract text
	text = speech.recognize_from_wav(wav_path=name, target_language=english)

	# delete file
	os.remove(name)
	
	# translate text
	lines = text.split(".!?")
	response = translator.translate(schemas.Text(text=lines, language=german))
	result = [schemas.TranslatedText(**x) for x in response.json()]
	return {"filename": file.filename,
	 		"content_type": file.content_type,
			"content": text,
			"translation": result}
