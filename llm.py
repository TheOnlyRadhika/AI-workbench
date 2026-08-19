import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

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
    return response.choices[0].message.content


def ask_llm_with_tools(messages, tools):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    return response.choices[0].message



