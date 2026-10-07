#imports
from ai_helper import ask_gemini, transcribe_audio
import streamlit as st
from question_bank import questions, worlds

# SESSION STATE DEFAULTS
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []

if "homework_help_active" not in st.session_state:
    st.session_state.homework_help_active = False

if "started" not in st.session_state:
    st.session_state.started = False

if "age" not in st.session_state:
    st.session_state.age = None


# PAGE SETTINGS
st.set_page_config(
    page_title="Adaptive Math Tutor",
    page_icon="✨",
    layout="centered"
)


# VISUAL STYLE
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #f8f7ff 0%,
            #eef8ff 50%,
            #fff7ec 100%
        );
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 30px;
        border-radius: 28px;
        background: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.07);
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        color: #666;
    }

    .question-card {
        background: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.07);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .world-tag {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 16px;
        height: 3.2rem;
        font-size: 17px;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)
MAX_INTERACTIONS = 20

if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0

# AI HOMEWORK HELP
if st.session_state.get("homework_help_active", False):

    st.title("📚 AI Math Tutor")
    age = st.session_state.get("age", None)


    if age:
        st.markdown(
        f"""
        <div style="
            display: inline-block;
            background: #f1edff;
            padding: 7px 14px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 18px;
        ">
            ✨ Learning for age {age}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Learn through personalized, step-by-step guidance. "
        "Your tutor will help you think through the problem instsead of "
        "simply giving you the answer."
    )

    if st.button("← Back to Home", key="homework_back"):
        st.session_state.homework_help_active = False
        st.session_state.tutor_messages = []
        st.rerun()

    if "homework_help_active" not in st.session_state:
        st.session_state.homework_help_active = False

    if "tutor_messages" not in st.session_state:
        st.session_state.tutor_messages = []

    if "started" not in st.session_state:
        st.session_state.started = False
        st.stop()

    # Create conversation memory
    if "tutor_messages" not in st.session_state:
         st.session_state.tutor_messages = []

# Welcome message shown before the conversation starts
    if not st.session_state.tutor_messages:
         st.markdown(
        """
        ...
        """,
        unsafe_allow_html=True
    )
    if not st.session_state.tutor_messages:
         st.markdown(
            """
            <div style="
            background: white;
            padding: 28px;
            border-radius: 20px;
            border: 1px solid #ececec;
            box-shadow: 0 4px 16px rgba(0,0,0,0.05);
            margin-top: 24px;
            margin-bottom: 24px;
        ">
            <h3 style="margin-top: 0;">Hi! I'm your AI Math Tutor 👋</h3>
            <p style="margin-bottom: 8px;">
                Ask me a math question, and I'll guide you through it step by step.
            </p>
            <p style="margin-bottom: 0;">
                I'll help you think through the problem instead of simply giving you the answer.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show previous conversation
for message in st.session_state.get("tutor_messages",[]):

    if message["role"] == "user":
        avatar = "🧒"
    else:
        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.write(message["content"])

    # Student input
chat_input = st.chat_input(
    "Ask a math question or respond to your tutor...",
    accept_audio=True
)

student_message = None

if chat_input:
        
       
    if st.session_state.interaction_count >= MAX_INTERACTIONS:
       st.warning(
       f"You've reached the {MAX_INTERACTIONS}-message limit for this demo session."
)
       st.stop()

    # If the child typed
    if chat_input.text:
        student_message = chat_input.text

    # If the child recorded audio
    elif chat_input.xaudio:
        with st.spinner("Listening... 🎤"):
            student_message = transcribe_audio(chat_input.audio)

    if student_message:

        st.session_state.interaction_count += 1

        st.session_state.tutor_messages.append(      
            {
                "role": "user",
                "content": student_message
            }
        )

    with st.chat_message("user", avatar="🧒"):
        st.write(student_message)

        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in st.session_state.tutor_messages
        )

        prompt = f"""
You are a friendly, supportive and adaptive AI math tutor.

Your purpose is to help students understand mathematics through
guided thinking rather than simply giving them answers.

Always respond in clear English suitable for an international audience.

Teaching rules:
- Guide the student step by step.
- Ask one meaningful question at a time.
- Adapt your explanation based on the student's responses.
- If the student makes a mistake, explain it kindly and help them try again.
- Do not reveal the final answer immediately.
- Encourage reasoning and mathematical understanding.
- Keep responses concise and age-appropriate.
- If the student already understands a step, move forward instead of
  repeating the explanation.

Conversation so far:

{conversation}

Respond to the student's latest message as their math tutor.
"""

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    tutor_reply = ask_gemini(
                        prompt,
                        st.session_state.age
)
                    st.write(tutor_reply)

                    st.session_state.tutor_messages.append(
                        {
                            "role": "assistant",
                            "content": tutor_reply
                        }
                    )

                except Exception:
                    st.error(
                        "The AI tutor is temporarily unavailable. "
                        "Please try again."
                    )
# IMPORTANT: outside "if student_message"

    st.stop()

# LEVEL FUNCTIONS
def starting_level(age):
    if age <= 6:
        return "easy"
    elif age <= 8:
        return "medium"
    else:
        return "hard"


level_order = ["easy", "medium", "hard"]

level_names = {
    "easy": "Explorer 🌱",
    "medium": "Adventurer 🚀",
    "hard": "Math Master ⭐"
}


def level_up(level):
    if level == "hard":
        return level

    current = level_order.index(level)
    return level_order[current + 1]


def level_down(level):
    if level == "easy":
        return level

    current = level_order.index(level)
    return level_order[current - 1]


# SESSION STATE
if "started" not in st.session_state:
    st.session_state.started = False

if "challenge" not in st.session_state:
    st.session_state.challenge = 0

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "homework_help_active" not in st.session_state:
    st.session_state.homework_help_active = False

if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []

if "second_try" not in st.session_state:
    st.session_state.second_try = False

if "message" not in st.session_state:
    st.session_state.message = None



# HOME
if st.session_state.get("homework_help_active", False):
    st.stop()
st.markdown(
    """
    <div class="hero">
        <h1>✨ Adaptive Math Tutor</h1>
        # Do not show the Home screen while Homework Help is open.
        <p>Learn, explore and collect stars through your own adventure!</p>
    </div>
    """,
    unsafe_allow_html=True
)


# START SCREEN
if not st.session_state.started:

    name = st.text_input(
        "🌟 What's your name?"
    )

    age = st.number_input(
        "🎂 How old are you?",
        min_value=5,
        max_value=12,
        value=6,
        step=1
    )

    st.write("### What would you like to do today?")

    mode = st.radio(
        "Choose your adventure:",
        [
            "📚 Homework Help",
            "🎮 Practice & Play"
        ],
        horizontal=True
    )


    # PRACTICE MODE
    if mode == "🎮 Practice & Play":

        st.write("### 🌈 Choose your favorite world")
        st.write("Pick a world and begin your math adventure!")

    available_worlds = {
        f"{emoji} {world_name}": key
        for key, (world_name, emoji) in worlds.items()
        if key in questions
    }

    if "selected_world" not in st.session_state:
        st.session_state.selected_world = None

    world_descriptions = {
        "1": "Dive into an ocean of discoveries!",
        "2": "Explore the stars and distant planets!",
        "3": "Travel back to the dinosaur world!",
        "4": "Play, score and become a champion!",
        "5": "Discover magical creatures and treasures!",
        "6": "Race toward your next math challenge!"
    }

    cols = st.columns(3)

    for index, (label, key) in enumerate(available_worlds.items()):

        world_name, emoji = worlds[key]

        with cols[index % 3]:

            with st.container(border=True):

                st.markdown(f"## {emoji}")
                st.markdown(f"**{world_name}**")
                st.caption(world_descriptions.get(key, "Let's explore!"))

                is_selected = (
                    st.session_state.selected_world == label
                )

                button_text = (
                    "✓ Selected"
                    if is_selected
                    else "Explore ✨"
                )

                if st.button(
                    button_text,
                    key=f"world_{key}",
                    use_container_width=True
                ):
                    st.session_state.selected_world = label
                    st.rerun()

    selected_world = st.session_state.selected_world

    if selected_world in available_worlds:
        st.success(f"Your adventure: {selected_world}")

    # START BUTTON
    if st.button(
        "Start my adventure! 🚀",
         use_container_width=True,
         type="primary"
):
         if not name.strip():

            st.warning("Tell me your name first! 😊")

         elif mode == "📚 Homework Help":
            st.session_state.name = name.strip()
            st.session_state.age = int(age)
            st.session_state.homework_help_active = True
            st.session_state.tutor_messages = []
            st.rerun()

         elif selected_world not in available_worlds:

            st.warning("Choose your favorite world first! 🌈")

         else:

            st.session_state.started = True
            st.session_state.name = name.strip()
            st.session_state.age = age
            st.session_state.world_choice = available_worlds[selected_world]

            st.session_state.level = starting_level(age)

            st.session_state.challenge = 0
            st.session_state.stars = 0
            st.session_state.second_try = False
            st.session_state.message = None

            st.rerun()

# GAME SCREEN
if st.session_state.get("started", False):
    choice = st.session_state.world_choice

    world_name = worlds[choice][0]
    world_emoji = worlds[choice][1]
    name = st.session_state.name
    level = st.session_state.level


    # PLAYER INFORMATION
    st.write(
        f"## {world_emoji} {world_name}"
    )

    st.write(
        f"Welcome, **{name}**! Let's collect some stars. ✨"
    )


    # STATS
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⭐ Stars",
        f"{st.session_state.stars}/3"
    )

    col2.metric(
        "🎯 Challenge",
        f"{min(st.session_state.challenge + 1, 3)}/3"
    )

    col3.metric(
        "🌱 Level",
        level_names[level]
    )


    # MESSAGE FROM PREVIOUS ANSWER
    if st.session_state.message:

        message_type, message_text = st.session_state.message

        if message_type == "success":
            st.success(message_text)

        elif message_type == "warning":
            st.warning(message_text)

        else:
            st.info(message_text)

        st.session_state.message = None


    # ADVENTURE COMPLETE
    if st.session_state.challenge >= 3:

        st.progress(1.0)

        st.write(
            f"## 🏆 {world_name} Complete!"
        )

        stars = st.session_state.stars

        st.write(
            f"You collected **{stars} out of 3 stars!** ⭐"
        )

        if stars == 3:

            st.balloons()

            st.success(
                "🌟 Perfect adventure! "
                "You're a Math Explorer!"
            )

        elif stars == 2:

            st.success(
                "🎉 Great adventure! "
                "You did an awesome job!"
            )

        else:

            st.info(
                "🌱 Nice work! Every challenge "
                "makes your math skills stronger!"
            )


        if st.button(
            "🌈 Play another adventure",
            use_container_width=True
        ):

            st.session_state.started = False
            st.session_state.challenge = 0
            st.session_state.stars = 0
            st.session_state.second_try = False
            st.session_state.message = None

            st.rerun()


    # QUESTION SCREEN
    else:

        challenge = st.session_state.challenge
        level = st.session_state.level

        st.progress(
            (challenge + 1) / 3
        )


        question, correct_answer, hint = (
            questions[choice][level][challenge]
        )


        st.markdown(
            f"""<div class="question-card">
        <div class="world-tag">
        🏁 Challenge {challenge + 1}
        </div>
        <h3>{question}</h3>
        </div>""",
             unsafe_allow_html=True
)



        # SHOW HINT ON SECOND TRY
        if st.session_state.second_try:

            st.info(hint)


        # ANSWER FORM
        with st.form(
            key=f"answer_form_{challenge}_{level}_{st.session_state.second_try}"
        ):

            answer = st.text_input(
                "✏️ Your answer"
            )

            submitted = st.form_submit_button(
                "Check my answer ✨",
                use_container_width=True,
                 type="primary")


            if submitted:

                 answer = answer.strip()


            if not answer:

                st.warning(
                    "Type an answer first 😊"
                )


            # CORRECT
            elif answer == str(correct_answer):

                st.session_state.stars += 1


                # CORRECT AFTER HINT
                if st.session_state.second_try:

                    st.session_state.message = (
                        "success",
                        "🎉 You got it! Great thinking! "
                        "You earned a star! ⭐"
                    )

                    st.session_state.second_try = False


                # CORRECT FIRST TRY
                else:

                    st.session_state.message = (
                        "success",
                        "🌟 Amazing job! "
                        "You earned a star!"
                    )

                    new_level = level_up(
                        st.session_state.level
                    )

                    if new_level != st.session_state.level:

                        st.session_state.message = (
                            "success",
                            "🌟 Amazing job! You earned a star! "
                            "🚀 Your next challenge is leveling up!"
                        )

                        st.session_state.level = new_level


                st.session_state.challenge += 1

                st.rerun()


            # WRONG
            else:

                # FIRST WRONG ANSWER
                if not st.session_state.second_try:

                    st.session_state.second_try = True

                    st.session_state.message = (
                        "warning",
                        "💡 Almost! Here's a little hint."
                    )

                    st.rerun()


                # SECOND WRONG ANSWER
                else:

                    st.session_state.message = (
                        "info",
                        f"🌱 Nice try! The answer was "
                        f"{correct_answer}. "
                        "Let's keep learning together!"
                    )

                    st.session_state.level = level_down(
                        st.session_state.level
                    )

                    st.session_state.second_try = False
                    st.session_state.challenge += 1

                    st.rerun()