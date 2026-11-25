import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

client = Groq(api_key=api_key)

def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned an empty response.")
    return content


def ask_llm_with_tools(messages, tools):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned an empty response.")
    return content



