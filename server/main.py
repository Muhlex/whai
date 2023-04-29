from typing import List
import translate as ts
from fastapi import FastAPI, HTTPException, UploadFile

import schemas

app = FastAPI()
translator = ts.Translator()


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
	return {"filename": file.filename}
