import json
import logging
from openai import OpenAI
from tqdm import tqdm
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model="/nfs/turbo/coe-chaijy-unreplicated/pre-trained-weights/Qwen2.5-0.5B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful agent."},
        {"role": "user", "content": "Help me to make a salad"},
    ],
    max_tokens=300,
    temperature=1.0,
    top_p=1.0
)
print(chat_response.choices[0].message.content)