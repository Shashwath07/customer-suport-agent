"""
Customer memory service.

This module provides the simple interface that the Backend will use.

The Backend does NOT need to know Hindsight's internal API.

It only needs functions such as:

    get_customer_memories(customer_id, query)
    save_customer_memory(customer_id, memory)

This keeps the architecture clean and makes it easier to replace
or modify the memory implementation later.
"""

from typing import Any, List, Optional

from memory.hindsight_client import (
    ensure_customer_bank,
    get_hindsight_client,
)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_RECALL_LIMIT = 5


# ============================================================
# MEMORY RETRIEVAL
# ============================================================

def get_customer_memories(
    customer_id: str,
    query: str,
    limit: int = DEFAULT_RECALL_LIMIT
) -> List[str]:
    """
    Retrieve memories relevant to the customer's current query.

    Parameters:
        customer_id:
            Unique customer identifier.

        query:
            Current customer message/question.

        limit:
            Maximum number of memories returned.

    Returns:
        A list of relevant memory strings.
    """

    if not isinstance(customer_id, str):
        raise TypeError(
            "customer_id must be a string."
        )

    if not customer_id.strip():
        raise ValueError(
            "customer_id cannot be empty."
        )

    if not isinstance(query, str):
        raise TypeError(
            "query must be a string."
        )

    if not query.strip():
        raise ValueError(
            "query cannot be empty."
        )

    if not isinstance(limit, int) or limit <= 0:
        raise ValueError(
            "limit must be a positive integer."
        )


    # Make sure this customer's isolated memory bank exists.
    bank_id = ensure_customer_bank(
        customer_id
    )

    client = get_hindsight_client()


    try:

        result = client.recall(
            bank_id=bank_id,
            query=query.strip(),
            types=[
                "world",
                "experience",
                "observation"
            ],
            max_tokens=3000,
            budget="mid"
        )


        memories = []


        # Hindsight returns recalled memories in result.results.
        for memory in getattr(
            result,
            "results",
            []
        ):

            memory_text = getattr(
                memory,
                "text",
                None
            )

            if memory_text:
                memories.append(
                    memory_text.strip()
                )


            if len(memories) >= limit:
                break


        return memories


    except Exception as error:

        raise RuntimeError(
            f"Failed to retrieve memories "
            f"for customer {customer_id}: {error}"
        ) from error


# ============================================================
# SAVE MEMORY
# ============================================================

def save_customer_memory(
    customer_id: str,
    memory: str,
    context: Optional[str] = None
) -> bool:
    """
    Store a useful customer-specific memory in Hindsight.

    Parameters:
        customer_id:
            Unique customer identifier.

        memory:
            Information that should be remembered.

        context:
            Optional context describing where the information came from.

    Returns:
        True when the memory has been submitted successfully.
    """

    if not isinstance(customer_id, str):
        raise TypeError(
            "customer_id must be a string."
        )

    if not customer_id.strip():
        raise ValueError(
            "customer_id cannot be empty."
        )

    if not isinstance(memory, str):
        raise TypeError(
            "memory must be a string."
        )

    memory = memory.strip()

    if not memory:
        raise ValueError(
            "memory cannot be empty."
        )


    # Ensure the customer has an isolated memory bank.
    bank_id = ensure_customer_bank(
        customer_id
    )

    client = get_hindsight_client()


    try:

        retain_kwargs = {
            "bank_id": bank_id,
            "content": memory,
        }


        # Hindsight supports context to help shape the
        # extraction and interpretation of memories.
        if context and context.strip():

            retain_kwargs["context"] = (
                context.strip()
            )


        client.retain(
            **retain_kwargs
        )


        return True


    except Exception as error:

        raise RuntimeError(
            f"Failed to save memory "
            f"for customer {customer_id}: {error}"
        ) from error


# ============================================================
# SAVE CONVERSATION
# ============================================================

def save_customer_conversation(
    customer_id: str,
    customer_message: str,
    assistant_response: str
) -> bool:
    """
    Store a conversation turn as customer memory.

    This is useful for the 'getting smarter' demonstration.

    Hindsight can process a whole conversation as one memory item,
    allowing it to extract useful facts, experiences, and observations.
    """

    if not customer_message.strip():
        raise ValueError(
            "customer_message cannot be empty."
        )

    if not assistant_response.strip():
        raise ValueError(
            "assistant_response cannot be empty."
        )


    conversation = (
        f"Customer: {customer_message.strip()}\n"
        f"Support Agent: {assistant_response.strip()}"
    )


    return save_customer_memory(
        customer_id=customer_id,
        memory=conversation,
        context="Customer support conversation"
    )


# ============================================================
# SAVE CUSTOMER PROFILE
# ============================================================

def save_customer_profile(
    customer_id: str,
    profile: dict
) -> bool:
    """
    Store structured customer information as a readable
    memory statement.

    Example:

        {
            "plan": "Premium",
            "communication_preference": "Email"
        }

    becomes a natural-language memory that Hindsight can process.
    """

    if not isinstance(profile, dict):
        raise TypeError(
            "profile must be a dictionary."
        )

    if not profile:
        raise ValueError(
            "profile cannot be empty."
        )


    profile_lines = []


    for key, value in profile.items():

        if value is None:
            continue

        readable_key = (
            str(key)
            .replace("_", " ")
            .strip()
        )

        profile_lines.append(
            f"{readable_key}: {value}"
        )


    if not profile_lines:
        raise ValueError(
            "profile does not contain usable information."
        )


    memory_text = (
        "Customer profile information:\n"
        + "\n".join(
            f"- {line}"
            for line in profile_lines
        )
    )


    return save_customer_memory(
        customer_id=customer_id,
        memory=memory_text,
        context="Customer profile"
    )
