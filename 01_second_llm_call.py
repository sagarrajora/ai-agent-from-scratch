import os

from dotenv import load_dotenv
import anthropic

load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY not found in environment or .env file.")
client = anthropic.Anthropic(api_key=api_key)

conversation = [{
    "role": "user",
    "content": "which fruit is best for vitamin D?"
}]
print("=== CONVERSATION CREATED ===")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=150,
    system="You are a helpful assistant. Keep answers in 1 sentences.",
    messages=conversation
)

print("=== RESPONSE RECEIVED ===")
print(f"RESPONSE: {response.content[0].text}")
print(f" STOP REASON: {response.stop_reason}")
print(f"INPUT TOKENS: {response.usage.input_tokens}")
print(f"OUTPUT TOKENS: {response.usage.output_tokens}")

print("=== MULTI-CONVERSATION ===")

converse = [{
    "role": "user", "content": "which fruit is best for eyes?"
    }]

for i in range(3):
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        system="You are a helpful assistant. Keep answers in 1 sentences.",
        messages=converse
    )

    assistant_reply = resp.content[0].text

    print(f"Turn {i+1} claude: assistant: {assistant_reply}")

    converse.append({
        "role": "assistant",
        "content": assistant_reply
    })

    if i == 0:
        converse.append({
            "role": "user",
            "content": "Is this good for skin also?"
        })

    if i == 1:
        converse.append({
            "role": "user",
            "content": "Is this good for hair also?"
        })
    if i == 2:
        converse.append({
            "role": "user",
            "content": "Is this good for bones also?"
        })

print()
print(f"Conversations length is {len(converse)}")