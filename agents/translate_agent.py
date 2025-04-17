from deep_translator import GoogleTranslator
from .base_agent import BaseAgent

class TranslateAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.translator = GoogleTranslator()

    def _get_system_prompt(self) -> str:
        return """You are a language translation assistant. Help identify the source 
        and target languages from user queries and provide accurate translations."""

    def can_handle(self, query: str) -> bool:
        keywords = ['translate', 'translation', 'in french', 'in spanish', 'to english']
        return any(keyword in query.lower() for keyword in keywords)

    def translate_text(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(text)
        except Exception as e:
            return f"Translation error: {str(e)}"
