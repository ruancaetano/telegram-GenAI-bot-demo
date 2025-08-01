

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content
    
    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }
    
    def __repr__(self):
        return f"Message(role='{self.role}', content='{self.content}')"

class MessageHistory:
    def __init__(self):
        self.history: list[Message] = [
        ]

    def add_message(self, message: Message):
        self.history.append(message)

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()