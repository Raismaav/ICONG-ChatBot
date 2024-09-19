from dotenv import load_dotenv
from openai import OpenAI
import os

class Assistant:
    def __init__(self, system_message: str, default_model: str, functions: list = None):
        load_dotenv()

        self.client = OpenAI(api_key=os.getenv('openai_key'))
        self.system_message = [{"role": "system", "content": system_message}]
        self.model = default_model
        self.tools = functions

    def respose_to(self, messages: list, model: str = None):
        if not model:
            model = self.model
        completion = self.client.chat.completions.create(
            model=model,
            messages=self.system_message + messages,
            tools=self.tools,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return completion.choices[0].message