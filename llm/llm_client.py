from openai import OpenAI
import os
from typing import Type, TypeVar, Any, Dict, List
from openai.resources.beta.threads import messages
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self, system_prompt: str=""):
        self.client = OpenAI(
            api_key=os.environ["GEMINI_API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        self.system_message = self.get_system_message(system_prompt)

    def get_system_message(self, system_prompt: str):
        if system_prompt and system_prompt.strip() != "":
            return {
                "role": "developer",
                "content": [{
                    "type": "text",
                    "text": system_prompt.strip()
                }]
            }
        return None

    def get_chat_messages(self, content: List[Dict[str, Any]]):
        chat_messages = []
        
        if self.system_message:
            chat_messages.append(self.system_message)
            
        chat_messages.append({
            "role": "user",
            "content": content
        })

        return chat_messages

    def analyse_image(self, prompt: str, base64_images: list[str], response_format_class: Type[T]) -> T:
        content = []
        content.append({"type": "text", "text": f"{prompt}"})
        for base64_image in base64_images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        
        response = self.client.beta.chat.completions.parse(
            model="gemini-2.0-flash",
            messages=self.get_chat_messages(content),
            response_format=response_format_class,
        )

        return response.choices[0].message.parsed

    def generate_text(self, prompt: str) -> str:
        content = []
        content.append({"type": "text", "text": f"{prompt}"})

        response = self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=self.get_chat_messages(content)
        )

        return str(response.choices[0].message.content)
