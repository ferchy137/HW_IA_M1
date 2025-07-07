import requests
import json
import time
import streamlit as st
import sseclient  # sseclient-py


def backend_call(query: str):
    """
    The `backend_call` function sends a query to a backend service and streams the response using
    Server-Sent Events (SSE).
    
    :param query: The `backend_call` function you provided seems to be making a streaming call to a
    backend service using Server-Sent Events (SSE). The function takes a `query` parameter, which is
    used to construct the URL for the backend call
    :type query: str
    """
    url = f"http://orchestrator/streamingSearch?query={query}"
    stream_response = requests.get(url, stream=True)
    client = sseclient.SSEClient(stream_response)  # type: ignore

    # Loop forever (while connection "open")
    for event in client.events():
        yield event


def display_chat_messages():
    """
    The code defines functions to display chat messages, process user input, handle backend responses,
    and display backend responses with buttons in a chat interface.
    """
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def process_user_input(prompt):
    """
    The function `process_user_input` appends the user input to a list in the session state and displays
    it in a chat message container.
    
    :param prompt: The `process_user_input` function seems to be designed to process user input in a
    chat application. The `prompt` parameter likely represents the user's input message or prompt that
    needs to be processed
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


def process_backend_response(prompt):
    """
    The function `process_backend_response` processes backend responses by displaying them in columns
    with buttons and updating the full response accordingly.
    
    :param prompt: The `process_backend_response` function seems to be processing a response from a
    backend call. It appears to be displaying the response in chunks, potentially with buttons and
    messages. The function also updates the `st.session_state.messages` with the processed response
    """
    full_response = ""
    columns = st.columns(2)
    button_count = 0
    button_placeholders, message_placeholder = [], None
    with st.spinner("Thinking..."):
        for chunk in backend_call(prompt):
            button_count, button_placeholders = display_backend_response(
                chunk, button_count, columns, button_placeholders
            )
            full_response, message_placeholder = process_chunk_event(
                chunk, full_response, message_placeholder
            )

    st.session_state.messages.append({"role": "assistant", "content": full_response})


def display_backend_response(chunk, button_count, columns, button_placeholders):
    """
    The function `display_backend_response` processes search results and creates buttons with shortened
    links.
    
    :param chunk: The `chunk` parameter seems to be an object or data structure that contains
    information related to an event, possibly related to a search operation. The code snippet provided
    is checking if the event in the `chunk` object is a "search" event, and if so, it processes the data
    within the
    :param button_count: The `button_count` parameter in the `display_backend_response` function is used
    to keep track of the number of buttons that have been created so far. It is incremented each time a
    new button is added to the interface
    :param columns: The `columns` parameter in the `display_backend_response` function likely represents
    the number of columns in a grid or layout where buttons will be displayed. It is used to determine
    the layout of the buttons generated in response to a search event
    :param button_placeholders: The `button_placeholders` parameter is a list that stores button
    placeholders. These button placeholders are created and appended to this list within the
    `display_backend_response` function. Each button placeholder is assigned a label and a key based on
    the item data retrieved from the backend response
    :return: The function `display_backend_response` is returning the updated `button_count` and
    `button_placeholders` after processing the `chunk` data in the case where the event is "search".
    """
    if chunk.event == "search":
        for item in json.loads(chunk.data).get("items"):
            button_placeholder = assign_button_placeholder(columns, button_placeholders)
            button_placeholder.button(
                label=item.get("link")[8:42] + "...", key=button_count
            )
            button_count += 1
            button_placeholders.append(button_placeholder)
            time.sleep(0.05)
    return button_count, button_placeholders


    """
    The function `assign_button_placeholder` determines which column to empty based on the parity of the
    number of button placeholders provided.
    
    :param columns: The `columns` parameter is likely a list of two elements, where each element
    represents a column in a user interface or a data structure. The function
    `assign_button_placeholder` seems to be designed to determine which column to empty based on the
    length of the `button_placeholders` list
    :param button_placeholders: Button placeholders are elements in a user interface that indicate where
    a button will be placed. They are typically used to reserve space for buttons that will be
    dynamically added or removed based on user interactions or other conditions
    :return: either `columns[0].empty()` or `columns[1].empty()` based on whether the length of
    `button_placeholders` is even or odd.
    """
def assign_button_placeholder(columns, button_placeholders):
    return (
        columns[0].empty() if len(button_placeholders) % 2 == 0 else columns[1].empty()
    )


def process_chunk_event(chunk, full_response, message_placeholder):
    """
    The function `process_chunk_event` processes a chunk event by updating a full response and
    displaying it with a message placeholder in a markdown format.
    
    :param chunk: The `chunk` parameter seems to represent a piece or part of data being processed. In
    the provided function `process_chunk_event`, it is used to check if the event is a "token" and then
    update the `full_response` and `message_placeholder` accordingly
    :param full_response: The `full_response` parameter seems to be a string that stores the accumulated
    response data from processing chunks. It is updated with the data from the current chunk and
    returned for further processing
    :param message_placeholder: The `message_placeholder` parameter is a placeholder element that can be
    used to display messages or content in a streamlit app. In the `process_chunk_event` function, if
    `message_placeholder` is not provided (i.e., it is `None`), a new empty placeholder element is
    created using
    :return: The function `process_chunk_event` returns two values: `full_response` and
    `message_placeholder`.
    """
    if chunk.event == "token":
        if not message_placeholder:
            message_placeholder = st.empty()
        full_response += chunk.data
        message_placeholder.markdown(full_response + "▌")
    return full_response, message_placeholder


st.title("InternetWhisper")
# Initialize chat history
st.session_state.messages = st.session_state.get("messages", [])

display_chat_messages()

# Accept user input
if prompt := st.chat_input("Ask me a question..."):
    process_user_input(prompt)
    process_backend_response(prompt)
