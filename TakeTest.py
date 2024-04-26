import requests
import streamlit as st
import os
from twilio.rest import Client

api_key = st.secrets["open_keys"]
endpoint = 'https://api.openai.com/v1/chat/completions'


account_sid = 'ACfeab2ba89e8e8caf1feb0336cdafe342'
auth_token = '9dda3c1d44037cda84aed528c9b4a271'
client = Client(account_sid, auth_token)


def generate_summary(prompt):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
            
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'system', 'content': 'You are a Student scorer.'}, {'role': 'user', 'content': prompt}],
        }
        response = requests.post(endpoint, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']


# Define your questions, options, answers, and categories
questions = [
    {
        "category": "Remembering",
        "content": [
            {
                "question": "What is the force that attracts a body towards the center of the earth, or towards any other physical body having mass?",
                "options": ["Electromagnetic force", "Gravity", "Nuclear force", "Friction"],
                "answer": "Gravity"
            },
            {
                "question": "Which planet in our solar system has the strongest gravitational pull?",
                "options": ["Mercury", "Mars", "Jupiter", "Venus"],
                "answer": "Jupiter"
            }
        ]
    },
    {
        "category": "Understanding",
        "content": [
            {
                "question": "Why do astronauts feel weightless in space?",
                "options": ["There is no gravity in space", "Gravity is only present on Earth", "They are falling freely under gravity", "Space nullifies mass"],
                "answer": "They are falling freely under gravity"
            },
            {
                "question": "What happens to the gravitational force between two objects if the distance between them is doubled?",
                "options": ["It increases by four times", "It decreases by four times", "It doubles", "It halves"],
                "answer": "It decreases by four times"
            }
        ]
    },
    {
        "category": "Applying",
        "content": [
            {
                "question": "If you were to move from sea level up to a mountain, how would gravity affect your weight?",
                "options": ["Weight would increase", "Weight would decrease", "No change in weight", "Weight doubles"],
                "answer": "Weight would decrease"
            },
            {
                "question": "How would the weight of an object change if it were moved from Earth to Mars?",
                "options": ["Increase", "Decrease", "Stay the same", "Become zero"],
                "answer": "Decrease"
            }
        ]
    },
    {
        "category": "Analyzing",
        "content": [
            {
                "question": "Two objects with different masses are dropped from the same height. Which statement is true regarding their motion due to gravity?",
                "options": ["The heavier object hits the ground first", "Both hit the ground at the same time", "The lighter object hits the ground first", "Cannot be determined without additional information"],
                "answer": "Both hit the ground at the same time"
            },
            {
                "question": "Given the equation for gravitational force F = G * (m1*m2) / r^2, what would happen to the force if mass m1 is halved?",
                "options": ["Force is halved", "Force is doubled", "Force remains the same", "Force is quartered"],
                "answer": "Force is halved"
            }
        ]
    },
    {
        "category": "Evaluating",
        "content": [
            {
                "question": "Which would have a greater impact on decreasing the gravitational force between two objects?",
                "options": ["Doubling the distance between them", "Halving the mass of one object", "Doubling the mass of one object", "Reducing the distance by half"],
                "answer": "Doubling the distance between them"
            },
            {
                "question": "Assess the statement: 'Gravitational forces are the weakest forces known in nature.'",
                "options": ["True", "False, electromagnetic forces are weaker", "False, strong nuclear forces are weaker", "False, weak nuclear forces are weaker"],
                "answer": "True"
            }
        ]
    },
    {
        "category": "Creating",
        "content": [
            {
                "question": "Design an experiment to measure the gravitational pull on different planets using only a pendulum.",
                "options": ["Change the length of the pendulum on each planet", "Use the same pendulum and record the time period of swings on each planet", "Use different weights at the end of the pendulum", "Swing the pendulum at different angles"],
                "answer": "Use the same pendulum and record the time period of swings on each planet"
            },
            {
                "question": "Create a plan to demonstrate how gravity would affect the trajectory of a projectile launched from a mountain.",
                "options": ["Launch projectiles at varying angles and measure the distances", "Launch projectiles at the same angle with different velocities", "Launch projectiles with varying weights at the same angle", "All of the above"],
                "answer": "All of the above"
            }
        ]
    }
]

def main():
    st.title("MCQ Assessment on Physics: Gravity")

    total_score = 0
    total_questions = 0

    # Variables to store scores for each category
    remembering_score = 0
    understanding_score = 0
    applying_score = 0
    analyzing_score = 0
    evaluating_score = 0
    creating_score = 0

    for section in questions:
        with st.container():
            score = 0
            answered = 0
            
            for question in section["content"]:
                total_questions += 1
                q = st.radio(question["question"], question["options"], key=f"{section['category']}_{question['question']}")
                if q == question["answer"]:
                    score += 1
                    answered += 1

            # Add the score to the corresponding category variable
            if section['category'] == "Remembering":
                remembering_score += score
            elif section['category'] == "Understanding":
                understanding_score += score
            elif section['category'] == "Applying":
                applying_score += score
            elif section['category'] == "Analyzing":
                analyzing_score += score
            elif section['category'] == "Evaluating":
                evaluating_score += score
            elif section['category'] == "Creating":
                creating_score += score

            total_score += score

    # Show the total score only after the submit button is clicked
    if st.button("Submit"):
        st.write(f"Your total score is {total_score} out of {total_questions}")
        if total_score == total_questions:
            st.balloons()  # Celebrate perfect score

        # Print the scores for each category
        # st.write("Remembering Score:", remembering_score)
        # st.write("Understanding Score:", understanding_score)
        # st.write("Applying Score:", applying_score)
        # st.write("Analyzing Score:", analyzing_score)
        # st.write("Evaluating Score:", evaluating_score)
        # st.write("Creating Score:", creating_score)


        pre_prompt = f"You are an expert teacher. I will be giving you the score of a student which he scored in a Blooms level MCQ test. I will share the score. Your task is to give personalized feedback on the test. The exam is on gravity. The Blooms level scores are:\n\nRemembering Score: {remembering_score}\nUnderstanding Score: {understanding_score}\nApplying Score: {applying_score}\nAnalyzing Score: {analyzing_score}\nEvaluating Score: {evaluating_score}\nCreating Score: {creating_score}\n\ndone. The length of the output should be 100 words only."
        resultgpt=generate_summary(pre_prompt)
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=resultgpt,
        to='whatsapp:+917995664448'
        )


if __name__ == "__main__":
    main()
