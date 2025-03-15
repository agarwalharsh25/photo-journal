from pydantic import BaseModel

class PhotoDescription(BaseModel):
    description: str
    time_and_weather: str
    mood: str
    landmarks: list[str]
    activities: list[str]
    style: str

class PhotoDescriptionList(BaseModel):
    photo_descriptions: list[PhotoDescription]