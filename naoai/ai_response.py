from re import sub
from requests import post
from ollama import chat, ChatResponse


class AiResponse:
    """Class defining methods for different AI model responses"""

    def gemini(self, prompt, api_key, sysprompt) -> str:
        """Module for communicating with Gemini and getting responses. Needs an API key."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"

        data = {
            "system_instruction": {"parts": {"text": sysprompt}},
            "contents": [{"parts": [{"text": prompt}]}],
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
        x = response.json()
        content = x["candidates"][0]["content"]["parts"][0]["text"]
        print(sub("[*]", " ", content))
        return content

    def ollama(self, prompt, model, sysprompt) -> str:
        """Module for interfacing with local Ollama and getting responses."""
        response: ChatResponse = chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": sysprompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        response = response["message"]["content"]
        print(sub("[*]", " ", response))
        return sub("[*]", " ", response)
