"""
PHASE 1 — Exercise 1: Your First LLM Call
==========================================
No frameworks. Just the raw Anthropic SDK.
Goal: understand what a "call" to an LLM actually is.

Run: python 01_first_llm_call.py
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── 1. CREATE A CLIENT ────────────────────────────────────────────────────────
# The client reads your ANTHROPIC_API_KEY from the environment.
# You can also pass it explicitly: anthropic.Anthropic(api_key="sk-ant-...")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# ── 2. THE CORE CALL ──────────────────────────────────────────────────────────
# Every LLM call has three main knobs:
#   model      → which version of Claude to use
#   max_tokens → hard cap on response length (1 token ≈ 0.75 words)
#   messages   → the conversation so far, as a list of role/content pairs

response = client.messages.create(
    model="claude-haiku-4-5-20251001",   # cheapest/fastest Claude model
    max_tokens=256,
    system="You are a helpful assistant. Keep answers under 3 sentences.",
    messages=[
        {"role": "user", "content": "What is an AI agent in one sentence?"}
    ]
)


# ── 3. INSPECT THE RESPONSE ───────────────────────────────────────────────────
print("=== RAW RESPONSE OBJECT ===")
print(f"Model used     : {response.model}")
print(f"Stop reason    : {response.stop_reason}")   # 'end_turn' = finished naturally
print(f"Input tokens   : {response.usage.input_tokens}")
print(f"Output tokens  : {response.usage.output_tokens}")
print()

print("=== THE ACTUAL REPLY ===")
# response.content is a list — usually one TextBlock
text = response.content[0].text
print(text)
print()


# ── 4. MULTI-TURN CONVERSATION ────────────────────────────────────────────────
# There's no magic "memory" — you literally re-send the full history each time.
# This is the key insight: the model is stateless. YOU maintain the conversation.

conversation = [
    {"role": "user", "content": "Name one popular AI agent framework."}
]

print("=== MULTI-TURN CONVERSATION ===")

for i in range(2):
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        messages=conversation
    )

    assistant_reply = resp.content[0].text
    print(f"[Turn {i+1}] Claude: {assistant_reply}")

    # Append the assistant's reply to history, then add the next user message
    conversation.append({"role": "assistant", "content": assistant_reply})

    if i == 0:
        conversation.append({"role": "user", "content": "What language is it written in?"})

print()
print(f"Full conversation has {len(conversation)} messages total.")
print("Notice: every API call above sent the ENTIRE history — no server-side memory.")
