import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(context):
    """Generate a response from the given context using OpenAI API."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Choose the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context}
        ]
    )
    return response['choices'][0]['message']['content']
