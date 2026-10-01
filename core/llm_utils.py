import os
import time

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI


load_dotenv(override=True)

_last_request_time = 0


def get_llm(temperature=0.3):
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise RuntimeError(
            "MISTRAL_API_KEY was not configured."
        )

    return ChatMistralAI(
        model="ministral-3b-2512",
        mistral_api_key=api_key,
        temperature=temperature,
    )


def safe_invoke(chain, input_data, retries=3):
    global _last_request_time

    for attempt in range(retries):
        elapsed = time.time() - _last_request_time

        if elapsed < 1.2:
            time.sleep(1.2 - elapsed)

        try:
            result = chain.invoke(input_data)
            _last_request_time = time.time()
            return result

        except Exception as e:
            error_message = str(e)

            if (
                "429" in error_message
                or "rate_limit" in error_message.lower()
            ):
                wait_time = 3 * (attempt + 1)

                print(
                    f"Mistral rate limit reached. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise RuntimeError(
        "Mistral API rate limit persisted after multiple retries."
    )