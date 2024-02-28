import streamlit as st

st.image("valorizeHeader.png")

footer_html = """
    <hr style="border: none; border-top: 1px solid #555; margin-top: 2em; margin-bottom: 0;" />
    <p style="font-size: 0.8em; color: #777; text-align: center;">Powered by: Valorize</p>
    """
with st.sidebar:
    st.image("lock.png",width=20)
    
    st.caption("Autonomous Agent")
    st.caption("Expertvetted Consultant")
    
    st.image("step.png",width=300)
    # openai_api_key = st.secrets["openai_api_key"]
    openai_api_key = "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"
    
    st.markdown(footer_html, unsafe_allow_html=True)



st.image("UI.png")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

    # client = OpenAI(api_key=openai_api_key)
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)

# st.sidebar.image("step.png",width = 200)
# st.sidebar.caption("Powered by: Valorize")

