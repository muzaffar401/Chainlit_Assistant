# Import the Chainlit library and alias it as 'cl' for easier reference
import chainlit as cl

# Use the @cl.on_message decorator to specify that the following function 
# should be executed whenever a new message is received
@cl.on_message
# Define an asynchronous function named 'main' that will handle incoming messages.
# The function takes a single parameter 'message', which is an instance of cl.Message
async def main(message: cl.Message):

    # Extract the content of the incoming message and create a response string.
    # The response simply echoes back what the user said, prefixed with "You said:"
    response = f"You said: {message.content}"

    # Create a new message object with the response content and send it back to the user.
    # The 'await' keyword ensures that this operation completes asynchronously.
    await cl.Message(content=response).send()