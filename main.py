from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
import io
from generative_service import GenerativeService
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

help_text = """🤖 **Telegram GenAI Bot Commands**
                        **Available Commands:**
                        • `/start` - Welcome message and bot introduction
                        • `/help` - Show this help message
                        • `/clear_history` - Clear conversation history

                        **How to use:**
                        Simply send me any message and I'll generate an AI response for you! The bot remembers our conversation context until you clear it.

                        **Note:** Use `/clear_history` if you want to start a fresh conversation.
        """


async def main():
    generative_service = GenerativeService(OPENAI_API_KEY)
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    logging.info("Bot started")

    async def get_voice_transcription(message: types.Message) -> str:
        if message.voice is None:
            return ""

        prefix = "Audio message transcript:\n"
        tg_file = await bot.get_file(message.voice.file_id)
        audio_buffer = io.BytesIO()

        logging.info("Downloading voice file...")
        await bot.download_file(tg_file.file_path, audio_buffer)

        audio_buffer.name = "voice.ogg"
        audio_buffer.seek(0)

        logging.info("Getting audio transcript...")
        transcript = generative_service.get_audio_transcription(audio_buffer)

        return f"{prefix}{transcript}"

    async def get_user_message(message: types.Message) -> str:
        if message.text:
            return message.text
        elif message.voice:
            return await get_voice_transcription(message)
        else:
            return ""

    async def send_response_message(
        message: types.Message, answer: str, answer_type: str
    ):
        logging.info(f"Sending response message: {answer_type} \n Answer: {answer}")
        if answer_type == "text":
            await message.answer(answer)
        elif answer_type == "voice":
            audio_response = generative_service.generate_audio_response(answer)
            audio_file = types.BufferedInputFile(
                audio_response, filename="response.mp3"
            )
            await message.answer_voice(audio_file)

    @dp.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer("Hello, world!")

    @dp.message(Command("help"))
    async def help_handler(message: types.Message):
        await message.answer(help_text, parse_mode="Markdown")

    @dp.message(Command("clear_history"))
    async def clear_handler(message: types.Message):
        generative_service.clear_history()
        await message.answer("History cleared")

    @dp.message()
    async def generate_response_handler(message: types.Message):
        await bot.send_chat_action(message.chat.id, "typing")
        try:
            user_message = await get_user_message(message)

            answer, answer_type = generative_service.generate_response(user_message)
            logging.info(f"Answer type: {answer_type} \n Answer: {answer}")

            await send_response_message(message, answer, answer_type)

        except Exception as e:
            await message.answer(f"Failed to generate response: {str(e)}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())
