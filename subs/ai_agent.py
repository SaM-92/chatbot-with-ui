from autogen_agentchat.agents import AssistantAgent
from typing import Any, Optional  # Import necessary types

def assistant_define(client):
    """Define the assistant agent with the model client and system message."""
    # client = OpenAIChatCompletionClient(
    assistant = AssistantAgent(
        name="assistant",
        model_client=client,
        system_message="""You are a helpful assistant. Be polite and concise., and provide accurate information.""",
        reflect_on_tool_use=True
    )

    return assistant


async def assistant_response_generator(chunk: Any, chunk_text: Optional[str], full_response: str) -> str:
    """Appends assistant message content from a stream chunk to the full response.

    Args:
        chunk: The data chunk from the stream.
        chunk_text: Placeholder for extracted text (re-assigned internally).
        full_response: The accumulated response string so far.

    Returns:
        The updated full_response string with new content appended, if any.
    """
    # Extract text content ONLY if it seems like an assistant response part
    if isinstance(chunk, str):
        chunk_text = chunk
    elif hasattr(chunk, 'content') and isinstance(chunk.content, str):
        # Check if 'source' attribute exists and equals 'assistant'
        if hasattr(chunk, 'source') and chunk.source == 'assistant':
            chunk_text = chunk.content
        else:
            # Reset chunk_text if it's not from the assistant to avoid appending unrelated content
            chunk_text = None

    if chunk_text is not None:
        # Accumulate the extracted text response
        full_response += chunk_text

    return full_response  # Return the updated full_response
