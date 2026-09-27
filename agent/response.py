"""
Response generation layer.

This module acts as the interface between the Backend and
the LLM module.

The Backend should call this module instead of directly
calling the Groq API.
"""

from agent.llm import generate_llm_response


def generate_response(
    customer_query: str,
    customer_memories: list
) -> str:
    """
    Generate the final customer-support response.

    Parameters:
        customer_query:
            Current customer message.

        customer_memories:
            Relevant memories retrieved for the customer.

    Returns:
        Final AI-generated response.
    """

    if not isinstance(
        customer_query,
        str
    ):
        raise TypeError(
            "customer_query must be a string."
        )


    if not customer_query.strip():
        raise ValueError(
            "customer_query cannot be empty."
        )


    if customer_memories is None:
        customer_memories = []


    if not isinstance(
        customer_memories,
        list
    ):
        raise TypeError(
            "customer_memories must be a list."
        )


    try:

        response = generate_llm_response(
            customer_query=customer_query.strip(),
            customer_memories=customer_memories
        )


        return response


    except Exception as error:

        raise RuntimeError(
            f"Unable to generate customer-support response: "
            f"{str(error)}"
        ) from error
