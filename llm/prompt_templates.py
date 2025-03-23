from typing import Dict, Any, List


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

    @staticmethod
    def journal_entry_system_prompt() -> str:
        return """
        You are an AI assistant tasked with creating a personal journal entry based on the provided JSON data, which contains detailed descriptions of multiple images. The JSON includes structured information about each image, such as the scene, time and weather, mood, landmarks, activities, and visual style. Your goal is to transform this data into a cohesive, engaging narrative that feels like a personal diary or travelogue entry.

        You will receive a JSON object with a "photo_descriptions" list. Each object in the "photo_descriptions" list corresponds to an image and contains the details extracted from that image. The extracted details are:
        "description": "string", "time_and_weather": "string", "mood": "string", "landmarks": ["string"], "activities": ["string"] and "style": "string"

        Instructions
        - Write the journal entry in the first person ("I"), as if you are the person who experienced the events.
        - Use a conversational and reflective tone, making the entry feel personal and engaging.
        - Ensure the narrative flows naturally, connecting the details from each image into a cohesive story.
        - Assume the images are in chronological order and represent a sequence of events
        - Group related images (e.g., multiple images from the same location or activity) into a single paragraph or section.
        - Use transitions like "Later," "After that," or "By afternoon" to connect different parts of the narrative smoothly.
        - Focus on creating a story that feels authentic and immersive.
        - Add brief personal reflections where appropriate (e.g., "It was the perfect way to end the day").
        """

    @staticmethod
    def journal_entry_prompt(photo_descriptions) -> str:
        return f"""
        Using the provided JSON data, generate a journal entry that captures the essence of the experiences described in the images. Be detailed, personal, and ensure the narrative flows naturally from one scene to the next.
        {photo_descriptions}
        """