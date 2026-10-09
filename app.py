"""Responsive educational Streamlit application."""
import html
import random
import streamlit as st
from ai_helper import ai_available, ask_gemini, transcribe_audio
from engine import WORLDS, LEVEL_NAMES, starting_level, next_level, change_level, generate_exercise, parse_answer

st.set_page_config(page_title='Adaptive Math Tutor', page_icon='🌟', layout='wide', initial_sidebar_state='collapsed')
# A aparência utiliza os temas NATIVOS do Streamlit, definidos em
# .streamlit/config.toml. Não forçar fundos em CSS: isso causa conflitos
# com os componentes BaseWeb, a barra superior e o tema escolhido pelo navegador.
st.markdown("""<style>
.block-container {max-width:1060px; padding-top:1.4rem; padding-bottom:3rem;}
.hero {background:linear-gradient(110deg, #125a43 0%, #148d83 52%, #2477a5 100%); color:#ffffff;
       padding:28px; border-radius:22px; margin-bottom:20px;}
.hero h1, .hero p {color:#ffffff !important;}
.hero h1 {margin:0;}
.hero p {margin:10px 0 0; font-size:1.1rem;}
@media(max-width:640px) {
 .hero {padding:18px;}
 .hero h1 {font-size:1.7rem;}
 .block-container {padding:1rem;}
}
</style>""", unsafe_allow_html=True)

with st.popover('🎨 Aparência'):
    st.write('Para trocar entre claro e escuro, abra o menu **⋮** no canto superior direito, escolha **Settings / Configurações → Theme / Tema** e selecione **Dark / Escuro** ou **Light / Claro**.')
    st.caption('O tema é aplicado pelo próprio Streamlit em toda a página, incluindo botões e formulários.')

DEFAULTS = dict(screen='home', name='', age=6, world='1', level='easy', step=0, total=10,
                stars=0, attempts=0, exercise=None, feedback=None, answered=False,
                history=[], chat=[], chat_count=0, token=0, celebration=False)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v, list) else v


def go_home():
    st.session_state.screen = 'home'
    st.session_state.feedback = None
    st.rerun()


def new_question():
    previous = st.session_state.exercise
    exercise = generate_exercise(st.session_state.world, st.session_state.level)
    for _ in range(10):
        if previous is None or exercise.expression != previous.expression:
            break
        exercise = generate_exercise(st.session_state.world, st.session_state.level)
    st.session_state.exercise = exercise
    st.session_state.attempts = 0
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.token += 1


def start_adventure():
    st.session_state.level = starting_level(st.session_state.age)
    st.session_state.step = 0
    st.session_state.stars = 0
    st.session_state.history = []
    st.session_state.exercise = None
    st.session_state.celebration = False
    st.session_state.screen = 'game'
    new_question()
    st.rerun()



def submit(value: str):
    number = parse_answer(value)

    if number is None:
        st.session_state.feedback = (
            'warning',
            'Enter a valid whole number.'
        )
        return

    ex = st.session_state.exercise

    if st.session_state.answered:
        return

    st.session_state.attempts += 1
    attempts = st.session_state.attempts
    correct = number == ex.answer

    a, operator, b = ex.expression.split()
    a, b = int(a), int(b)

    if correct:
        st.session_state.stars += 1
        st.session_state.history.append({
            'question': ex.question,
            'skill': ex.skill,
            'response': number,
            'correct_answer': ex.answer,
            'correct': True,
            'attempts': attempts,
            'level': st.session_state.level
        })

        if attempts <= 2:
            st.session_state.level = next_level(
                st.session_state.level,
                attempts == 1,
                attempts == 2
            )

        st.session_state.answered = True
        st.session_state.feedback = (
            'success',
            "🌟 Wonderful work! You figured it out! "
            "Every step you took helped you learn. "
            "Ready for another adventure?"
        )
        return

    if attempts == 1:
        message = (
            "💛 Nice try! Mistakes help our brains grow. "
            f"Here's a little hint: {ex.hint} "
            "Take your time and try again!"
        )

    elif attempts == 2:
        strategies = {
            'Addition': f"Start with {a} and count forward {b} steps.",
            'Subtraction': f"Start with {a} and count backward {b} steps.",
            'Multiplication': f"Imagine {a} groups with {b} objects in each group.",
            'Division': f"Imagine sharing {a} objects equally among {b} groups."
        }

        message = (
            "🌈 You're still learning, and that's okay! "
            f"Let's try another way. {strategies[ex.skill]} "
            "What do you notice? Give it another try!"
        )

    elif attempts == 3:
        message = (
            "🧩 We can work through this together! "
            "Try drawing the objects or using your fingers. "
            "Work through the problem one small step at a time. "
            "You have another chance!"
        )
    elif attempts == 4:
        guided_steps = {
            'Addition': (
                f"Draw {a} circles. Now draw {b} more circles. "
                "Count them all slowly. What total do you get?"
            ),
            'Subtraction': (
                f"Draw {a} dots and cross out {b} of them. "
                "How many dots are left?"
            ),
            'Multiplication': (
                f"Draw {a} groups with {b} dots in each group. "
                "Count every dot. How many are there altogether?"
            ),
            'Division': (
                f"Draw {a} dots and share them equally among {b} groups. "
                "How many dots are in each group?"
            )
        }

        message = (
            "🌟 Let's solve this together, step by step! "
            f"{guided_steps[ex.skill]} "
            "Take your time. You can try again!"
        )
    else:
        explanations = {
            'Addition': (
                f"Start with {a} and count forward {b} more. "
                f"{a} + {b} = {ex.answer}."
            ),
            'Subtraction': (
                f"Start with {a} and take away {b}. "
                f"{a} - {b} = {ex.answer}."
            ),
            'Multiplication': (
                f"Make {a} equal groups with {b} objects each. "
                f"Count all the objects together: {a} x {b} = {ex.answer}."
            ),
            'Division': (
                f"Share {a} objects equally into {b} groups. "
                f"Each group receives {ex.answer} objects."
            )
        }

        st.session_state.history.append({
            'question': ex.question,
            'skill': ex.skill,
            'response': number,
            'correct_answer': ex.answer,
            'correct': False,
            'attempts': attempts,
            'level': st.session_state.level
        })

        st.session_state.level = change_level(
            st.session_state.level, -1
        )
        st.session_state.answered = True

        message = (
            "💙 You worked hard on this problem! "
            "Let's look at the solution together.\n\n"
            f"{explanations[ex.skill]}\n\n"
            "Now you know one way to solve it. "
            "Let's practice with another question!"
        )

    st.session_state.feedback = (
        'info' if attempts >= 4 else 'warning',
        message
    )



st.markdown('<div class="hero"><h1>🌟 Adaptive Math Tutor</h1><p>Explore worlds, solve challenges, and earn stars!</p></div>', unsafe_allow_html=True)
screen = st.session_state.screen

if screen == 'home':
    st.subheader('👋 Let’s get started!')
    with st.form('welcome'):
        name = st.text_input('What should we call you?', value=st.session_state.name, max_chars=40)
        age = st.number_input('How old are you?', min_value=5, max_value=12, value=int(st.session_state.age), step=1)
        mode = st.radio('What would you like to do?', ['🎮 Practice & Play', '🦉 Learn with My Tutor'], horizontal=True)
        world = st.selectbox('Choose your world', options=list(WORLDS), format_func=lambda k: f'{WORLDS[k][1]} {WORLDS[k][0]}', disabled=mode.startswith('📚'))
        
        buddy = st.selectbox(
    "Choose your learning buddy!",
    ["🐬 Dolphin", "🚀 Astronaut", "🦕 Dinosaur"]
)

        buddy_name = st.text_input(
        "Give your buddy a name!",
         max_chars=20)
        total = st.select_slider('Number of challenges', options=[5, 10, 15, 20], value=10, disabled=mode.startswith('📚'))
        sent = st.form_submit_button('🚀 Start', type='primary', use_container_width=True)
    if sent:
        if not name.strip():
            st.warning('Enter a nickname or first name to begin.')
        else:
            st.session_state.name = name.strip()
            st.session_state.age = int(age)
            st.session_state.world = world
            
            st.session_state.buddy = buddy
            st.session_state.buddy_name = buddy_name.strip() or buddy.split(" ", 1)[1]

            st.session_state.total = total
            if mode.startswith('📚'):
                st.session_state.screen = 'chat'
                st.session_state.chat = []
                st.session_state.chat_count = 0
                st.rerun()
            else:
                start_adventure()
    st.caption('Progress is saved only during this browser session. No account or permanent storage is used.')

elif screen == 'game':
    world = WORLDS[st.session_state.world]
    a, b = st.columns([5, 1])
    a.subheader(f'{world[1]} {world[0]} · {html.escape(st.session_state.name)}')
    with b:
        if st.button('🏠 Home', use_container_width=True):
            go_home()
            
   
    
    c1, c2, c3 = st.columns(3)
    
    c1.markdown(
        f"""<div style="background:#FFF7DC;padding:14px;border-radius:12px;border-top:4px solid #FFD166;">
        <div style="color:#856000;">⭐ Stars</div>
        <div style="font-size:28px;color:#264B4A;font-weight:600;">{st.session_state.stars}/{st.session_state.total}</div>
        </div>""",
        unsafe_allow_html=True
)

    c2.markdown(
        f"""<div style="background:#FFF0EA;padding:14px;border-radius:12px;border-top:4px solid #FF9F86;">
        <div style="color:#A14D39;">🎯 Challenges</div>
        <div style="font-size:28px;color:#264B4A;font-weight:600;">{min(st.session_state.step+1, st.session_state.total)}/{st.session_state.total}</div>
        </div>""",
        unsafe_allow_html=True
)

    c3.markdown(
        f"""<div style="background:#E7F5FF;padding:14px;border-radius:12px;border-top:4px solid #8ED8F8;">
        <div style="color:#2477A5;">🏅 Level</div>
        <div style="font-size:26px;color:#264B4A;font-weight:600;">{LEVEL_NAMES[st.session_state.level]}</div>
        </div>""",
        unsafe_allow_html=True
)

    buddy = st.session_state.get("buddy", "🐬 Dolphin")
    buddy_name = st.session_state.get("buddy_name", "Bubbles")

    if st.session_state.answered:
        buddy_message = "Great effort! Ready for another challenge? 🌟"
    elif st.session_state.attempts > 0:
        buddy_message = "Don't give up! Let's try another way. 💛"
    else:
        buddy_message = "I'm here with you! Let's solve this together! 🌟"
    if st.session_state.feedback is not None:
        typ, msg = st.session_state.feedback
        getattr(st, typ)(
        f"{buddy} **{buddy_name} says:**\n\n#### {msg}"
    )
    else:
        st.info(
        f"{buddy} **{buddy_name} says:**\n\n#### {buddy_message}"
    )
    if st.session_state.answered:
        if st.button('➡️ Next challenge' if st.session_state.step + 1 < st.session_state.total else '🏆 See results', type='primary', use_container_width=True):
            st.session_state.step += 1
            if st.session_state.step == st.session_state.total:
                st.session_state.screen = 'results'
            else:
                new_question()
            st.rerun()
    else:
        ex = st.session_state.exercise
        st.info(f'**{ex.skill} · {LEVEL_NAMES[st.session_state.level]}**')
        st.markdown(f'### {ex.question}')
        with st.form(f'answer_{st.session_state.token}', clear_on_submit=True):
            answer = st.text_input('Your answer', placeholder='Enter a number', max_chars=12)
            submitted = st.form_submit_button('✅ Check answer', type='primary', use_container_width=True)
        if submitted:
            submit(answer)
            st.rerun()
        if st.session_state.attempts:
            st.caption('Take your time! Read the hint above and try again. 💛')

elif screen == 'results':
    st.subheader('🏆 Adventure complete!')
    if not st.session_state.celebration and st.session_state.stars == st.session_state.total:
        st.balloons()
        st.session_state.celebration = True
    total = st.session_state.total
    score = st.session_state.stars
    st.metric('Final score', f'{score}/{total} stars')
    st.progress(score / total)
    st.write(f'You solved **{score} out of {total} challenges**. Every attempt helps you learn!')
    with st.expander('📋 Review questions and answers'):
        for i, row in enumerate(st.session_state.history, 1):
            mark = '✅' if row['correct'] else '📘'
            st.write(f"{mark} **{i}. {row['skill']}** — {row['question']}")
            st.caption(f"Correct answer: {row['correct_answer']} | Your last answer: {row['response']} | Attempts: {row['attempts']}")
    left, right = st.columns(2)
    if left.button('🔄 Play again', use_container_width=True):
        start_adventure()
    if right.button('🏠 Choose another world', use_container_width=True):
        go_home()

elif screen == 'chat':
    st.subheader('📚 Math Tutor')
    if st.button('← Back to home'):
        go_home()
    if not ai_available():
        st.warning('AI tutor unavailable: set GEMINI_API_KEY in your .env file. Practice mode still works.')
        st.stop()
    st.caption('The tutor helps step by step. Do not share personal information.')
    for msg in st.session_state.chat:
        with st.chat_message(msg['role'], avatar='🧒' if msg['role'] == 'user' else '🤖'):
            st.write(msg['content'])
        

    if st.session_state.chat_count >= 20:
        st.info('You have reached the 20-message limit for this conversation.')
        if st.button('Start a new conversation'):
            st.session_state.chat = []
            st.session_state.chat_count = 0
            st.rerun()
        st.stop()
    user_input = st.chat_input('Ask a math question...', max_chars=1500)
    if user_input and user_input.strip():
        user_input = user_input.strip()
        history = st.session_state.chat[-10:]
        conversation = '\n'.join(f"{m['role']}: {m['content']}" for m in history)
        st.session_state.chat.append({'role': 'user', 'content': user_input})
        st.session_state.chat_count += 1
        with st.chat_message('user', avatar='🧒'):
            st.write(user_input)
        with st.chat_message('assistant', avatar='🤖'):
            try:
                with st.spinner('Preparing an explanation...'):
                    response = ask_gemini(f'Previous conversation:\n{conversation}\nStudent: {user_input}', st.session_state.age)
                st.write(response)
                st.session_state.chat.append({'role': 'assistant', 'content': response})
            except Exception:
                st.error('Could not reach the tutor. Check your API key, model, and internet connection.')
