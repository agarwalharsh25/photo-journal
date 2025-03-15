from typing import Dict


class PromptTemplates:
    
    @staticmethod
    def analyse_image(image_metadata: list[Dict[str, str]]) -> str:
        return f"""
        You are an expert image annotator. Analyze each image in detail and provide a list of descriptions with:

        1. A detailed description of the scene, including location, people, objects, and activities.
        2. The apparent time of day and weather conditions based on visual cues (e.g., lighting, shadows). Include exact date and time from metadata if available, but prioritize the image itself.
        3. The mood or emotional tone conveyed by the image (e.g., happy, serene, chaotic).
        4. Any notable landmarks or distinctive features. Use visual cues (e.g., signs, architecture) to pinpoint the location.
        5. Any activities happening in the image.
        6. The visual style or aesthetic of the image (e.g., vintage, modern, minimalist).

        Format your response as JSON with a key 'descriptions' containing a list of objects, each with keys:
        'description', 'time_and_weather', 'mood', 'landmarks', 'activities', 'style'.

        Be detailed and specific for each image. This will be used to generate a personal journal entry.

        Here is the datetime and location metadata from the image's EXIF data:
        {image_metadata}
        Use this as a reference, but note that the images may have been taken at a different time or location. This does not mean you ignore it. If you think it is related and could be accurate, make sure to include information from the metadata in your response.
        """
