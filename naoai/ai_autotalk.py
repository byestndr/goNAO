from re import sub
from base64 import b64encode
from requests import post
from ollama import chat



class AutoResponse:

    def ollamaImage(self, path):
        """Module for sending images to Ollama and getting responses."""
        with open(path, "rb") as image_file:
            image = b64encode(image_file.read()).decode("utf-8")

        response = chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Your role is a robotic assistant whose job is to sarcastically in a hilarious matter describe what is happening in this image in one sentence.",
                    "images": [image],
                }
            ],
        )

        reply = response["message"]["content"]
        return reply

    def geminiImage(path, api_key):
        """Module for sending images to Gemini and getting a response. An API key is needed."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"
        with open(path, "rb") as image_file:
            image = b64encode(image_file.read()).decode("utf-8")

        data = {
            "contents": [
                {
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": image}},
                        {
                            "text": "Your role is a robotic assistant whose job is to sarcastically in a hilarious matter describe what is happening in this image in one sentence."
                        },
                    ]
                }
            ],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        }

        response = post(url, headers={"Content-Type": "application/json"}, json=data)
        # This prints the result from Gemini
        # It converts the json into actual text and then regex's all the * out
        x = response.json()
        content = x["candidates"][0]["content"]["parts"][0]["text"]
        print(sub("[*]", " ", content))
        return content
