from google. genai import types
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega a chave guardada no arquivo .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no arquivo .env")

# Conecta ao Gemini
client = genai.Client(api_key=api_key)


def ask_gemini(prompt, age=None):
    age_context = ""

    if age is not None:
        age_context = f"""
The student is {age} years old.

Adapt your explanation to this age.
Use short, clear, child-friendly language.
Explain only one small step at a time.
Ask only one question at a time.
Be encouraging and playful.
Do not give the final answer immediately.
Help the student discover the answer.
"""

    full_prompt = f"""
{age_context}

{prompt}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=full_prompt
    )
    return response.text

def transcribe_audio(audio_file):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[
            "Transcribe the speech in this audio. Return only the transcription.",
            types.Part.from_bytes(
                data=audio_file.getvalue(),
                mime_type="audio/wav"
            )
        ]
    )
    return response.text.strip()