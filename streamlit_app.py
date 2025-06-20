import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 영어 회화 학습을 위한 Chatbot")
st.write(
    "영어회화 학습을 위한 챗봇입니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    level = st.selectbox(
    "👉 먼저 본인의 영어 실력을 선택해주세요:",
    ["Beginner", "Intermediate", "Advanced"]
)

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        if level == "Beginner":
        sys_prompt = (
            "You are a kind English tutor. Speak slowly and use simple vocabulary. "
            "Correct the user's grammar and explain why. Use very simple sentences."
        )
        elif level == "Intermediate":
        sys_prompt = (
            "You are a supportive English tutor. Speak naturally and give suggestions for more fluent expressions. "
            "Correct minor grammar mistakes and explain in simple English."
        )
        else:  # Advanced
        sys_prompt = (
            "You are a native-level English tutor. Speak fluently and naturally like a native speaker. "
            "Use idioms and complex sentence structures. Correct subtle mistakes and suggest native-like alternatives."
        )
        st.session_state.messages = [
            {
            "role": "system",
            "content": (
                "You are a friendly English conversation tutor. "
                "You help the user practice speaking naturally. "
                "Correct the user's grammar gently if needed, and give one suggestion for a more natural expression when appropriate. "
                "Always keep the tone supportive and encouraging."
                "기본적으로 영어로 응답을 생성하나, 사용자가 한국어로 설명해줄것을 요청할 경우, 한국어로 응답을 생성해."
                "fluency를 더할 수 있는 표현이 있다면 추천해줘."
            )
        }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("영어로 대화를 시작해보세요~"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=0.7,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
