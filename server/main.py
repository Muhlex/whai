import os
import uuid
from pprint import pprint
from typing import List, Annotated

import fastapi
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import translate as ts
import pdfcreator
import speech
import evaluate as ev
from fastapi import FastAPI, HTTPException, UploadFile, Query
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
from starlette.background import BackgroundTasks, BackgroundTask

import schemas
import summarize
import speech

app = FastAPI()

origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

translator = ts.Translator()
english = "en-US"
german = "de-DE"


@app.post("/translate/", response_model=schemas.TranslationResponse)
async def translate(text: schemas.Text, emoji: bool = False):
	print(emoji)
	split_text = text.text[0].split(".!?")
	response = translator.translate(text)
	ai_translate = ev.translate_chat_gpt(". ".join(split_text), text.language, emoji)
	if response is None or response.status_code != 200:
		raise HTTPException(status_code=500, detail="Translation Failed")
	translated_text = " ".join(
		[translation.text for translated_text in [schemas.TranslatedText(**x) for x in response.json()] for translation in
		 translated_text.translations])
	score = ev.evaluate_translation(" ".join(split_text), translation=translated_text)
	try:
		score = int(score)
	except ValueError:
		score = -1
	return {"azure_translation": translated_text,
					"chat_gpt_translation": ai_translate,
					"score": score}


@app.post("/summarize/", response_model=str)
async def summarize_report(report: schemas.SummarizeRequest):
	if len(report.text) < 250:
		raise HTTPException(status_code=400, detail="You need at least 250 characters")
	try:
		summery = summarize.summarize(report)
		return summery.summary
	except Exception as e:
		print(e)
		raise HTTPException(status_code=500, detail="Summarization Failed")


def remove_file(path: str) -> None:
	os.remove(path)


@app.post("/pdf/", response_class=FileResponse)
async def make_pdf(report: schemas.Pdf):
	name = pdfcreator.create_pdf(report.report)
	return FileResponse(name, media_type="application/pdf",background=BackgroundTask(remove_file, name),)


@app.post("/upload-file/", response_model=schemas.TranslationResponse)
async def create_upload_file(file: UploadFile, lang_to: str):
	name = f"{uuid.uuid4().hex}.wav"
	try:
		audio = AudioSegment.from_file_using_temporary_files(file.file)
		audio.export(name, format="wav")
		text_from_audio = speech.recognize_from_wav(wav_path=name, target_language="de-DE")
	except Exception as e:
		print(e)
		raise HTTPException(status_code=500, detail="Transcribe Failed")
	finally:
		os.remove(name)

	if text_from_audio.reason == speechsdk.ResultReason.RecognizedSpeech:
		lines = text_from_audio.text.split(".!?")
		response = translator.translate(schemas.Text(text=lines, language=lang_to))
		print(response.json())
		ai_translate = ev.translate_chat_gpt(text_from_audio.text, lang_to, emoji=False)
		print(ai_translate)
		if response is None or response.status_code != 200:
			raise HTTPException(status_code=500, detail="Translation Failed")
		result = [schemas.TranslatedText(**x) for x in response.json()]
		translated_text = " ".join([t.text for r in result for t in r.translations])
		score = ev.evaluate_translation(text_from_audio.text, translated_text)
		try:
			score = int(score)
		except ValueError:
			score = -1
		return {"azure_translation": translated_text,
						"chat_gpt_translation": ai_translate,
						"score": score}

	# unsuccessful speech to text conversion
	if text_from_audio.reason == speechsdk.ResultReason.NoMatch:
		print("no match in audio found")
		raise HTTPException(status_code=500, detail="No speech could be recognized")

	# failed before speech to text conversion
	elif text_from_audio.reason == speechsdk.ResultReason.Canceled:
		print("speech to text canceled")
		raise HTTPException(status_code=500, detail="Internal Server Error")
