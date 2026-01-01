"""Configure AI settings"""

from configparser import ConfigParser, NoOptionError, NoSectionError
from ollama import list, ListResponse


class Configuration:
    def __init__(self, current_directory):
        self.configpath = current_directory + "/config.ini"
        self.config = ConfigParser()
        self.config.read(self.configpath)

    def setKey(self, key: str, value: str):
        self.config.set("Main", key, value)

        try:
            with open(self.configpath, "w", encoding="utf-8") as configfile:
                self.config.write(configfile)
        except NoSectionError:
            self.config.add_section("Main")
            with open(self.configpath, "w", encoding="utf-8") as configfile:
                self.config.write(configfile)

        return

    def getKey(self, key) -> str:
        try: 
            value = self.config.get("Main", key)
        except NoOptionError:
            value = None

        return value

    def setOllamaModel(self, selectedModel: str) -> None:
        ollama_models = list()
        model_list = []

        for model in ollama_models.models:
            model_list.append(model.model)

        if not model_list:
            print("No models found, download some models or use Gemini")
            exit(1)

        if selectedModel not in model_list:
            print(
                "The model was not found. Make sure it is spelled right and if you've also typed its tag."
            )
            print(f"Models available: {model_list}")
            exit(1)

        self.setKey(key='model', value=selectedModel)

        return

    def setGeminiKey(self, api_key):
        self.setKey(key='api_key', value=api_key)