# Adaptive Math Tutor

An AI-powered math tutor designed to help children solve math problems through guided, step-by-step reasoning rather than simply providing the answer.

## Live Demo

[Try the Adaptive Math Tutor](https://adaptive-math-tutor.streamlit.app)

Experience the tutor directly in your browser — no installation required.

## About the Project
Adaptive Math Tutor is an educational AI project that combines generative artificial intelligence woth guided learning. Instead of immediately giving students the final answer, the tutor encourages them to reason through math problems step by step by asking questions, responding to their ideas, and maintaining the context of the conversation.

Students can interact with the tutor by typing or using voice input, making the experience more natural and accessible for young learners.

## Features

- AI-powered math tutoring using Google Gemini
- Guided, step-by-step problem solving instead of immediately revealing answers
- Text-based interaction with the tutor
- Voice input with automatic speech transcription
- Conversation memory that allows the tutor to follow the student's reasoning across multiple messages
- Playful, child-friendly learning experience designed to make math feel more engaging and approachable

## How It Works

1. The student asks a math question by typing or speaking.
2. If voice input is used, the audio is transcribed into text.
3. The AI analyzes the student's question and the context of the conversation.
4. Instead of immediately providing the final answer, the tutor guides the student through the problem with questions, hints, and age-friendly explanations.
5. The student responds and the tutor continues the conversation based on their reasoning, creating an interactive and playful learning experience.

## Educational Approach

The Adaptive Math Tutor was designed around the idea that children learn more meaningfully when they are actively involved in the problem-solving process.

Rather than simply giving the correct answer, the tutor uses guided questions, hints, encouragement, and conversational feedback to help students work toward the solution themselves.

The experience is intentionally playful and child-friendly, with the goal of making mathematics feel less intimidating and more engaging while still encouraging independent thinking.

## Technologies Used

- **Python** – Core programming language used to build the tutor's logic and AI integration
- **Streamlit** – Used to create the interactive web interface
- **Google Gemini API** – Powers the AI tutoring responses and audio transcription
- **Google Gen AI Python SDK** – Connects the application to Gemini models
- **python-dotenv** – Manages the API key securely through environment variables

## Project Structure

```text
Adaptive-math-tutor/
│
├── app.py
├── ai_helper.py
├── question_bank.py
├── tutor.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

- **app.py** – Runs the Streamlit web application and manages the user interface and learning experience.
- **ai_helper.py** – Handles communication with Google Gemini, including AI tutoring responses and voice transcription.
- **question_bank.py** – Stores the themed math questions used in Practice & Play.
- **tutor.py** – Contains the initial command-line prototype of the math tutor.
- **requirements.txt** – Lists the Python dependencies required to run the project.
- **.gitignore** – Prevents sensitive and unnecessary files from being uploaded to the repository.

## Getting Started

### 1. Install the dependencies

After downloading the project, open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 2. Set up the Gemini API key

Create a `.env` file in the project folder and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never share or commit your real API key to a public repository.

### 3. Run the application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser, where you can interact with the AI Math Tutor using text or voice input.

## Future Improvements

- Add spoken responses so students can listen to the tutor's explanations
- Develop more adaptive learning experiences based on student performance
- Add progress tracking to help students visualize their learning over time
- Expand the question bank to include more math topics and difficulty levels
- Create richer learner profiles to personalize tutoring interactions
- Conduct usability testing with learners to improve the educational experience

## Project Motivation

This project was developed as an independent exploration of the intersection between artificial intelligence, learning, and child-centered educational design.

Drawing on my background in education and my growing experience with programming and AI, I wanted to explore how generative AI could support children during the problem-solving process without simply replacing their own thinking.

The project also represents my broader interest in designing and studying AI-powered learning technologies that are engaging, accessible, and educationally meaningful.

