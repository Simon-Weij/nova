from dotenv.main import logger
from src.router.settings_store import load_settings_or_404


def wakeword():
    data = load_settings_or_404()

    wake_words = data.get("wakeWords", [])

    for word in wake_words:
        logger.info(f"ID: {word['id']}, Value: {word['value']}")
