""" Configure AI settings """
from os import path
from configparser import ConfigParser, NoOptionError, NoSectionError

class Configuration():
    """ Class defining methods to configure and read settings """
    def __init__(self):
        self.scriptpath = (path.dirname(path.realpath(__file__)))
        self.configpath = self.scriptpath + "/config.ini"
        self.config = ConfigParser()
        self.config.read(self.configpath)

    def modelType(self, modelname):
        """ Gets the model name """
        # Checks if you are using Ollama
        try:
            if modelname != "":
                import ollama
                response_object = ollama.list()
                model_list = response_object.models

                models = []

                # Checks if the list is empty or not
                if model_list:
                    for model in model_list:
                        models.append(model.model)
                else:
                    print("No models found, download some models or use Gemini")
                    exit(1)
                if modelname not in models:
                    print("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
                    print(f"Models available: {models}")
                    exit(1)

                self.config.set('Main', 'model', modelname)
                with open(self.configpath, 'w', encoding="utf-8") as configfile:
                    self.config.write(configfile)
                return self.config.get('Main', 'model')

            elif modelname == "":
                return self.config.get('Main', 'model')
        except NoSectionError:
            self.config.add_section('Main')
            self.config.set('Main', 'model', modelname)
            with open(self.configpath, 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)
            return self.config.get('Main', 'model')

    def geminiApiKey(self):
        """ Read the Gemini API key """
        # Get Gemini API key if it doesn't exist
        try:
            if path.isfile(self.configpath) is True:
                return self.config.get('Main', 'api_key')
            elif path.isfile(self.configpath) is False:
                keysave = input("Set a Gemini API key: ")
                self.config.set('Main', 'api_key', keysave)
                with open(self.configpath, 'w', encoding="utf-8") as configfile:
                    self.config.write(configfile)
                return self.config.get('Main', 'api_key')

        except NoOptionError:
            keysave = input("Set a Gemini API key: ")
            self.config.set('Main', 'api_key', keysave)
            with open(self.configpath, 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)
            return self.config.get('Main', 'api_key')
        except NoSectionError:
            keysave = input("Set a Gemini API key: ")
            self.config.add_section('Main')
            self.config.set('Main', 'api_key', keysave)
            with open(self.configpath, 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)
            return self.config.get('Main', 'api_key')

    def systemPrompt(self, systemFlag):
        """ Set the system prompt to use with the AI """
        # System prompt flag
        try:
            if systemFlag is False and path.isfile(self.configpath) is True:
                return self.config.get('Main', 'system_prompt')
            elif systemFlag is True or path.isfile(self.configpath) is False:
                keysave = input("Set a system prompt: ")
                self.config.set('Main', 'system_prompt', keysave)
                with open(self.configpath, 'w', encoding="utf-8") as configfile:
                    self.config.write(configfile)
                return self.config.get('Main', 'system_prompt')
        except NoOptionError:
            keysave = input("Set a system prompt: ")
            self.config.set('Main', 'system_prompt', keysave)
            with open(self.configpath, 'w', encoding="utf-8") as configfile:
                self.config.write(configfile)
            return self.config.get('Main', 'system_prompt')
