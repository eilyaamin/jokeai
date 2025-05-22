import os
import time
import random
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Memory for recent jokes to prevent duplicates
recent_jokes = set()
MAX_RECENT_JOKES = 100

prompt_variations = [
    "Tell me a random short joke.",
    "Make up a silly short joke.",
    "Invent a unique joke I've never heard.",
    "Give me a creative, original short joke.",
    "Tell me a weird but funny short joke about planets."
]

def is_duplicate(joke: str) -> bool:
    return joke in recent_jokes

def remember_joke(joke: str):
    recent_jokes.add(joke)
    if len(recent_jokes) > MAX_RECENT_JOKES:
        recent_jokes.pop()

async def generate_joke(logger):
    try:
        loop = asyncio.get_running_loop()

        for attempt in range(3):
            prompt = random.choice(prompt_variations)

            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="gemini-2.0-flash",
                    temperature=0.9,
                    top_p=0.95,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            )

            joke = response.choices[0].message.content.strip()

            if not is_duplicate(joke):
                remember_joke(joke)
                logger.info(f"Generated joke: {joke}")
                return joke
            else:
                logger.info("Duplicate joke detected. Retrying...")

        logger.warning("Too many duplicate jokes. Returning fallback.")
        return "Oops! Couldn't fetch a fresh joke right now."

    except Exception as e:
        logger.error(f"Failed to generate joke: {e}")
        return "Oops! Couldn't fetch a joke right now."
