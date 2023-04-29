import os
import openai
from dotenv import load_dotenv

def evaluate_translation(original, translation):
    load_dotenv()

    openai.api_key = os.environ("OPENAI_API_KEY")

    prompt = "Rate the translation of " + original + " to " + translation + " on a scale of 1 to 100."

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )

    return completion.choices[0].message.content