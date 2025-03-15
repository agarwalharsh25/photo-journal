from openai import OpenAI
import os
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ["GEMINI_API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

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
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            response_format=response_format_class,
        )

        return response.choices[0].message.parsed
