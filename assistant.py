from functions_to_call import call_function, tools
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

class Assistant:
    def __init__(self, system_message:str, default_model: str, temperature:float = 1, max_tokens:int = 256, have_tools:bool = False):
        load_dotenv()

        self.client = OpenAI(api_key=os.getenv('openai_key'))
        self.system_message = [{"role": "system", "content": system_message}]
        self.model = default_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tools = tools if have_tools else None

    def __call_function(self, tool_calls, messages):
        calls = []
        tools_called = []

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            result = call_function(name, arguments)

            tools_called.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": f"{arguments}"
                }})

            calls.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id,
            })

        messege_call = [{
                "role": "assistant",
                "content": "",
                "tool_calls": tools_called
        }] + calls

        response = self.__response_to(messages + messege_call)

        if response.content:
            return response
        else:
            return self.__call_function(response.tool_calls, messages + messege_call)

    def __response_to(self, messages: list, model: str = None):
        model = model or self.model
        completion = self.client.chat.completions.create(
            model=model,
            messages=self.system_message + messages,
            tools=self.tools,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response = completion.choices[0].message

        if response.tool_calls:
            return self.__call_function(response.tool_calls, messages)
        else:
            return response

    def response_to(self, messages: list, model: str = None):
        response = self.__response_to(messages, model)
        return {"role": response.role, "content": response.content}