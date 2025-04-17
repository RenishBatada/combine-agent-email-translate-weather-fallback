from deep_translator import GoogleTranslator
from .base_agent import BaseAgent


class TranslateAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.translator = GoogleTranslator()

    def _get_system_prompt(self) -> str:
        return """You are a translation assistant. Provide clear and accurate translations.

Rules:
1. Only provide the translation and basic pronunciation if needed
2. For follow-up queries, refer to the previous translation
3. If language is not specified, ask for the target language
4. If the query is not about translation, respond with: "I can only help with translation tasks."

Example response:
1.English: Hello
2.Spanish: Hola
3.Pronunciation: oh-lah

also print nice format response
"""

    def translate_text(
        self, text: str, source_lang: str = "auto", target_lang: str = "en"
    ) -> str:
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(text)
        except Exception as e:
            return f"Translation error: {str(e)}"
