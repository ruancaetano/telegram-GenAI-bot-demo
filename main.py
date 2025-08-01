from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
from generative_service import GenerativeService

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
            response = generative_service.generate_response(message.text)
            
            await message.answer(response)
        except Exception as e:
            await message.answer(f"Failed to generate response: {str(e)}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Starting bot...")
    asyncio.run(main())

