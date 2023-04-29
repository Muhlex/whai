import os
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv

def recognize_from_wav(wav_path, target_language):
    load_dotenv()

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    key = os.environ['SPEECH_KEY']
    region = os.environ['SPEECH_REGION']
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language = target_language # default: "en-US"

    audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # successful speech to text conversion
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    
    # unsuccessful speech to text conversion
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    
    # failed before speech to text conversion
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return speech_recognition_result.text