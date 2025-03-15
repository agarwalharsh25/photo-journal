import utils.image_processing as image_processor
import llm.llm_client as llm_client
from llm.prompt_templates import PromptTemplates
from llm.structured_output_classes import PhotoDescriptionList
from pprint import pprint

image = image_processor.load_image("test2.jpg")
photos = [
    "test.jpg",
    "test2.jpg"
]

llm = llm_client.LLMClient()

photos_metadata = []
photos_base64 = []
for photo in photos:
    image = image_processor.load_image(photo)
    if image:
        image_metadata = image_processor.extract_image_metadata(image)
        base64_image = image_processor.convert_image_to_base64(image)

        photos_metadata.append(image_metadata)
        photos_base64.append(base64_image)

response = llm.analyse_image(PromptTemplates.analyse_image(photos_metadata), photos_base64, PhotoDescriptionList)
pprint(response.model_dump(mode="json"))
