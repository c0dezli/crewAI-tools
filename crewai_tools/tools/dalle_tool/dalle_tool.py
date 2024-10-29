import json
from typing import Type

from openai import OpenAI
from pydantic import BaseModel

from crewai.tools.base_tool import BaseTool


class ImagePromptSchema(BaseModel):
    """Input for Dall-E Tool."""

    image_description: str = "Description of the image to be generated by Dall-E."


class DallETool(BaseTool):
    name: str = "Dall-E Tool"
    description: str = "Generates images using OpenAI's Dall-E model."
    args_schema: Type[BaseModel] = ImagePromptSchema

    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "standard"
    n: int = 1

    def _run(self, **kwargs) -> str:
        client = OpenAI()

        image_description = kwargs.get("image_description")

        if not image_description:
            return "Image description is required."

        response = client.images.generate(
            model=self.model,
            prompt=image_description,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )

        image_data = json.dumps(
            {
                "image_url": response.data[0].url,
                "image_description": response.data[0].revised_prompt,
            }
        )

        return image_data
