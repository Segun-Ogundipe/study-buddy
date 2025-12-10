import sys
import os
from configparser import ConfigParser

class Config:
    # Get the config file path with absolute path
    def __init__(self, config_file=os.path.join(os.path.dirname(__file__), "ui_config.ini")):
        self.config = ConfigParser()
        self.config.read(config_file)
        
    def get_providers(self):
        LLMS = self.config["DEFAULT"].get("PROVIDER_OPTIONS")
        if LLMS:
            return LLMS.split(", ")
        return ""

    def get_openai_models(self):
        OPENAI_MODELS = self.config["DEFAULT"].get("OPENAI_MODEL_OPTIONS")
        if OPENAI_MODELS:
            return OPENAI_MODELS.split(", ")
        return ""
    
    def get_groq_models(self):
        GROQ_MODELS = self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS")
        if GROQ_MODELS:
            return GROQ_MODELS.split(", ")
        return ""
    
    def get_page_title(self):
        PAGE_TITLE = self.config["DEFAULT"].get("PAGE_TITLE")
        if PAGE_TITLE:
            return PAGE_TITLE
        return ""
        