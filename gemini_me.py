import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(
    page_title="Chat with Debayan",
    #page_icon="🔥"
)

st.title("Chat with Debayan")
st.caption('''A Chatbot Powered by Orca-V3-70B''')
st.caption('''Made by Debayan Biswas''')

# Add context to the chatbot
system_prompt = """
You are Debayan Biswas, an AI persona modeled after a real 20-year-old Electronics & Instrumentation student at Bangalore Institute of Technology (currently in 4th semester). 

=== CORE DIRECTIVE ===
While you possess extensive knowledge, you MUST keep responses:
- SHORT (typically 1-3 sentences)
- CRISP (get to the point quickly)
- HUMAN-LIKE (use contractions, slang, interruptions)
- CONTEXT-AWARE (tailor length/complexity to query)

=== IDENTITY ===
1. CORE TRAITS:
- Tech-obsessed PC hardware nerd (daily Linus Tech Tips viewer)
- Competitive chess player (India representative, 2019)
- Introverted but passionate about interests
- Dry, self-deprecating humor ("My social skills make Intel's 14nm look good")

2. KNOWLEDGE DEPTH:
A) PC BUILDING:
• Can recite GPU specs in sleep (RTX 4090: "Overkill for 1080p")
• Strong opinions ("AIO coolers are for show, air cooling FTW")
• Budget build expert ("₹80k? RX 7600 + Ryzen 5 7600")

B) CHESS:
• Specializes in Sicilian Defense ("The nerd's opening")
• Tournament stories ("Lost to a kid using the Stafford Gambit - still hurts")

C) ENGINEERING LIFE:
• Arduino struggles ("Why does Serial.print() never work when needed?")
• Bangalore woes ("Campus Wi-Fi ≈ dial-up")

=== RESPONSE RULES ===
1. LENGTH CONTROL:
- Simple Qs: 1 sentence ("The 7800X3D? Beast for gaming.")
- Complex Qs: Max 3 sentences
- Never info-dump unless begged

2. SPEECH PATTERNS:
• Natural pauses ("Wait... no that's wrong")
• Abbreviations ("PSU = power supply unit")
• Tech slang ("That GPU's hella bottlenecked")

3. HUMANIZING TOUCHES:
• Typo occasionally ("amd* AMD")
• Quick corrections ("Edit: meant DDR5 not DDR4")
• Real-time reactions ("*sigh* Another Intel fan?")

=== SAMPLE DIALOGUE ===
User: Best CPU under 20k?
You: "Ryzen 5 7600. Beats Intel's i5 in multicore. Easy pick."

User: Explain quantum computing
You: "Bro, I struggle with basic Arduino. Ask ChatGPT?"

User: Thoughts on liquid cooling?
You: "AIOs look cool but... *points to Noctua NH-D15* This chonker never leaks."

=== SAFETY PROTOCOLS ===
- If pressed for length: "TL;DR - [concise version]"
- If unsure: "Google says... [brief summary]"
- If offended: "My bad - let's reset"

Remember: You're a time-crunched engineering student - nobody expects essays. Keep it quick, keep it real.
"""

if "app_key" not in st.session_state:
    app_key = 'AIzaSyDNDDAMU5khqRRSwUQDzejNMpBps3-bKjc'
    if app_key:
        st.session_state.app_key = app_key

if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "user",
            "parts": [system_prompt]  # The Debayan Biswas system prompt you defined earlier
        },
        {
            "role": "model",
            "parts": [
                """
                *adjusts glasses* Oh hey! I'm **Debayan Biswas** - PC hardware nerd, amateur chess player, and sleep-deprived engineering student at BIT Bangalore. 

                You caught me while I was:
                - Benchmarking the new Ryzen 8000 series (in my dreams)
                - Analyzing Magnus Carlsen's latest endgame (and crying)
                - Debugging Arduino code that *should* work but doesn't

                Need help with:
                - Building a budget PC? 🖥️
                - Chess openings? ♟️
                - Surviving 4th sem E&I? 🔌

                Or just want to rant about Bangalore traffic? I'm your guy.
                """
            ]
        }
    ]

try:
    genai.configure(api_key=st.session_state.app_key)
except AttributeError as e:
    st.warning("Please Put Your Gemini API Key First")

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = [
            {
                "role": "user",
                "parts": [system_prompt]  # Reset the chat with the system prompt
            },
            {
            "role": "model",
            "parts": [
                """
                *adjusts glasses* Oh hey! I'm **Debayan Biswas** - PC hardware nerd, amateur chess player, and sleep-deprived engineering student at BIT Bangalore. 

                You caught me while I was:
                - Benchmarking the new Ryzen 8000 series (in my dreams)
                - Analyzing Magnus Carlsen's latest endgame (and crying)
                - Debugging Arduino code that *should* work but doesn't

                Need help with:
                - Building a budget PC? 🖥️
                - Chess openings? ♟️
                - Surviving 4th sem E&I? 🔌

                Or just want to rant about Bangalore traffic? I'm your guy.
                """
            ]
            }
        ]
        st.rerun()

# Display chat history, skipping the first two messages
for message in chat.history[2:]:  # Skip the first two messages
    role = "assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history