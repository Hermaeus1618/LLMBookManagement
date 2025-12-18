import ollama

from app.core.config import settings

llm_client=ollama.Client(settings.LLM_BASE_URL)

prompt_system="""
You are a highly intelligent assistant that specializes in summarizing long texts, especially books.
Your task is to provide a concise and coherent summary of the provided text while maintaining its core ideas and key themes.
Aim for brevity, but make sure to include important plot points, character developments, and any significant information.
Your summary should be easy to read, engaging, and informative.
Make sure to provide summary in points.
"""

prompt_user="""
Please summarize the following text from a book.
Provide a brief yet comprehensive overview, capturing the most important details, including the plot, characters, and any other key themes or messages. 

*Book*
{text}
"""

class LLMService:
    """
    Service to generate summaries using Llama3/OpenRouter or other LLM backends.
    """

    def __init__(self):
        self.model_name = settings.LLM_MODEL_NAME

    async def generate_summary(self, text: str) -> str:
        """
        Generates a summary for the given text.
        """
        if not text:
            return "No content to summarize."
        
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user.format(text=text)}
        ]
        result = llm_client.chat(self.model_name, messages)
        
        return result.message.content