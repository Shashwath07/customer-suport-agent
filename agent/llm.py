"""
Groq LLM integration.

This module is responsible only for communicating with the
Groq API and generating an AI response.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from agent.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt
)


# Load variables from .env
load_dotenv()


# Read configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


# Create Groq client only when an API key exists.
# This allows the rest of the project to be imported
# before the API key is configured.
client = None

if GROQ_API_KEY:
    client = Groq(
        api_key=GROQ_API_KEY
    )


def generate_llm_response(
    customer_query: str,
    customer_memories: list
) -> str:
    """
    Generate a customer-support response using Groq.

    Parameters:
        customer_query:
            The customer's current message.

        customer_memories:
            Relevant memories retrieved for this customer.

    Returns:
        The generated AI response as a string.
    """

    if not customer_query:
        raise ValueError(
            "Customer query cannot be empty."
        )


    if client is None:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add your Groq API key to the .env file."
        )


    # Build the prompt
    user_prompt = build_user_prompt(
        customer_query=customer_query,
        customer_memories=customer_memories
    )


    try:

        completion = client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.3,

            max_tokens=500
        )


        # Extract the generated response
        response = (
            completion
            .choices[0]
            .message
            .content
        )


        if not response:
            raise RuntimeError(
                "The LLM returned an empty response."
            )


        return response.strip()


    except Exception as error:

        raise RuntimeError(
            f"LLM generation failed: {str(error)}"
        ) from error
