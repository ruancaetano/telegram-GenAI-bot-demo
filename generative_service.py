from openai import OpenAI
from message_history import MessageHistory, Message
import json
import logging


class GenerativeService:
    model = "gpt-5"
    whisper_model = "whisper-1"
    tts_model = "tts-1-hd"
    tts_voice = "nova"

    history: MessageHistory = MessageHistory()

    system_message = (
        "You are a helpful assistant integrated into a Telegram bot that CAN send audio replies via TTS. "
        "Decide between 'voice' and 'text' for each reply. "
        "Always respond in the same language as the user's message. "
        "If the user requests an audio/voice reply (e.g., 'áudio', 'voz', 'mensagem de áudio', 'voice note', 'send audio'), "
        "you MUST set answer_type to 'voice' and do not refuse. The application will synthesize and send the audio. "
        "When answer_type is 'voice', return clean, speakable text without markdown or emojis."
    )

    functions = [
        {
            "name": "create_answer_and_decide_response_type",
            "description": "After analyzing the user's message, create an answer and decide if the answer must be by voice or text. If the user mentions audio/voz/voice note, choose 'voice'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The answer to the user's message based on the history of the conversation",
                    },
                    "answer_type": {
                        "type": "string",
                        "enum": ["voice", "text"],
                        "description": "Use 'voice' when the user asks for audio/voz/voice note; otherwise choose 'text'.",
                    },
                },
            },
        }
    ]

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        # Ensure the system message is present at startup
        self.init_history()

    def init_history(self):
        logging.info("Initializing history")
        self.history.add_message(Message(role="system", content=self.system_message))

    def clear_history(self):
        logging.info("Clearing history")
        self.history.clear()
        self.init_history()

    def get_messages(self) -> list[Message]:
        return self.history.get_history()

    def get_audio_transcription(self, audio_file: bytes) -> str:
        logging.info(f"Getting audio transcription for: {audio_file}")
        transcription = self.client.audio.transcriptions.create(
            model=self.whisper_model, file=audio_file, response_format="text"
        )
        return (
            transcription
            if isinstance(transcription, str)
            else getattr(transcription, "text", "")
        )

    def generate_audio_response(self, prompt: str) -> bytes:
        logging.info(f"Generating audio response for: {prompt}")
        response = self.client.audio.speech.create(
            model=self.tts_model, voice=self.tts_voice, input=prompt
        )
        return response.content

    def generate_response(self, prompt: str) -> tuple[str, str]:
        try:
            logging.info(f"Generating response for: {prompt}")
            # Add the current user message to the history first
            self.history.add_message(Message(role="user", content=prompt))
            # Convert Message objects to dictionaries for OpenAI API
            messages = [msg.to_dict() for msg in self.get_messages()]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=self.functions,
                function_call={"name": "create_answer_and_decide_response_type"},
            )

            answer = json.loads(response.choices[0].message.function_call.arguments)
            answer_type = answer["answer_type"]
            answer = answer["answer"]

            self.history.add_message(Message(role="assistant", content=answer))

            return answer, answer_type

        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response", "text"
