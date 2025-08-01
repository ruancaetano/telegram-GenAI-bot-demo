from openai import OpenAI
from message_history import MessageHistory, Message

class GenerativeService:
    model = "gpt-4o-mini"
    history: MessageHistory = MessageHistory()
    system_message = "You are a helpful assistant."
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)


    def init_history(self):
        self.history.add_message(Message(role="system", content=self.system_message))

    def clear_history(self):
        self.history.clear()
        self.init_history()

    def get_messages(self) -> list[Message]:
        return self.history.get_history()

    def generate_response(self, prompt: str) -> str:
        try:
            # Convert Message objects to dictionaries for OpenAI API
            messages = [msg.to_dict() for msg in self.get_messages()]
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            self.history.add_message(Message(role="assistant", content=response.choices[0].message.content))
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response"