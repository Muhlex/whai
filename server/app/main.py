import os
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from. import translate as ts
from. import pdfcreator
from. import evaluate as ev
from fastapi import FastAPI, HTTPException, UploadFile
import logging
from starlette.background import BackgroundTask
from dotenv import load_dotenv

from. import schemas
from. import summarize
from. import audio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()

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
audio = audio.Audio()
openai_wrapper = ev.OpenAiWrapper()


@app.post("/translate/", response_model=schemas.TranslationResponse)
async def translate(text: schemas.Text, emoji: bool = False):
    return translator.translate(text, emoji)


@app.post("/summarize/", response_model=str)
async def summarize_report(report: schemas.SummarizeRequest):
    if len(report.text) < 250:
        raise HTTPException(status_code=400, detail="You need at least 250 characters")
    try:
        summery = summarize.summarize(report)
        return summery.summary
    except Exception as e:
        logger.error(f"Summarization Failed: {e}")
        raise HTTPException(status_code=500, detail="Summarization Failed")


def remove_file(path: str) -> None:
    os.remove(path)


@app.post("/pdf/", response_class=FileResponse)
async def make_pdf(report: schemas.Pdf):
    name = pdfcreator.create_pdf(report.report)
    return FileResponse(
        name,
        media_type="application/pdf",
        background=BackgroundTask(remove_file, name),
    )


@app.post("/transcribe-file/", response_model=schemas.TranscriptionResult)
async def transcribe_audio_file(file: UploadFile):
    name = audio.convert_to_wav(file)
    result = openai_wrapper.transcribe_audio(filename=name)
    logger.debug(f"openai transcript result: {result}")
    os.remove(name)
    return {"transcription": result}
