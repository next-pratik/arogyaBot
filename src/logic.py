from io import BytesIO
from gtts import gTTS
from googletrans import Translator
from src.text_utils import remove_emojis
from src.main import run_query

def process_user_prompt(prompt: str):
    translator = Translator()

    try:
        lang = translator.detect(prompt).lang
        translated_prompt = translator.translate(prompt, dest="en").text if lang != "en" else prompt

        # RAG pipeline call
        reply_en = run_query(translated_prompt)

        # Back-translate
        reply_local = translator.translate(reply_en, dest=lang).text if lang != "en" else reply_en

        # TTS with emoji cleaned
        clean_text = remove_emojis(reply_local)
        tts = gTTS(text=clean_text, lang=lang)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        return reply_local, audio_fp

    except Exception as e:
        return f"❌ Sorry, something went wrong.\n\n{str(e)}", None
