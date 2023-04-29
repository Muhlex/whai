import os
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv


def recognize_from_wav(wav_path, target_language):
	load_dotenv()

	# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
	key = os.environ['SPEECH_KEY']
	region = os.environ['SPEECH_REGION']
	speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
	speech_config.speech_recognition_language = target_language  # default: "en-US"

	audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
	speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

	speech_recognition_result = speech_recognizer.recognize_once_async().get()

	return speech_recognition_result
