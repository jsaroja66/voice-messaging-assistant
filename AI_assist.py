# Function to collect user name and AI assistant name
def collect_user_info():
    user_name = input("Enter your name: ")
    ai_name = input("Enter the name of the AI assistant: ")
    return user_name, ai_name

# Function to display voice options and let the user choose one
def choose_voice():
    voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
    print("Choose a voice from the following options:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice}")

    voice_choice = int(input("Enter the number corresponding to your choice: ")) - 1
    return voices[voice_choice]

import json

# Function to store user preferences in a file
def store_preferences(user_name, ai_name, chosen_voice):
    preferences = {
        'user_name': user_name,
        'ai_name': ai_name,
        'voice': chosen_voice
    }
    with open('preferences.json', 'w') as file:
        json.dump(preferences, file)

from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client with your API key
client = OpenAI()

# Function to generate spoken audio using OpenAI API
def generate_spoken_audio(text, voice, file_name='speech.mp3'):
    # Path to save the audio file
    speech_file_path = Path(__file__).parent / file_name
    
    # Generate the spoken audio
    response = client.audio.speech.create(
        model='tts-1',
        voice=voice,
        input=text
    )
    
    # Save the audio file
    with open(speech_file_path, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    
    print(f"Audio saved to {speech_file_path}")
    return speech_file_path

# Function to play the generated voice message and confirm if the user is satisfied with the voice
def play_and_confirm_voice(user_name, ai_name, chosen_voice):
    welcome_message = f"Hey, {user_name}, I'm {ai_name}, and I will be your messaging assistant."
    audio_path = generate_spoken_audio(welcome_message, chosen_voice)
    
    # Code to play audio from audio_path (implementation depends on the environment)
    # For example, you can use the playsound library: playsound(str(audio_path))
    
    satisfied = input("Is this voice good? (yes/no): ").strip().lower()
    return satisfied == 'yes'

# Function to run the setup process
def setup():
    try:
        with open('preferences.json', 'r') as file:
            preferences = json.load(file)
            return preferences
    except FileNotFoundError:
        user_name, ai_name = collect_user_info()
        chosen_voice = choose_voice()
        
        while not play_and_confirm_voice(user_name, ai_name, chosen_voice):
            chosen_voice = choose_voice()
        
        store_preferences(user_name, ai_name, chosen_voice)
        print("Setup complete.")
        
        return {
            'user_name': user_name,
            'ai_name': ai_name,
            'voice': chosen_voice
        }

# CALL setup
user_preferences = setup()

import random
from main_helper.greetings import get_greetings
from main_helper.date_utils import format_date

# Function to generate a random greeting and convert it to speech
def generate_greeting_audio(user_name, ai_name):
    greetings = get_greetings(user_name, ai_name)
    greeting = random.choice(greetings)
    
    # Generate the spoken audio for the greeting
    audio_path = generate_spoken_audio(greeting, user_preferences['voice'], file_name='greeting.mp3')
    
    # Code to play audio from audio_path (implementation depends on the environment)
    # For example, you can use the playsound library: playsound(str(audio_path))
    
    print(f"Greeting played: {greeting}")

# Generate greeting audio
generate_greeting_audio(user_preferences['user_name'], user_preferences['ai_name'])

from main_helper.greetings import get_random_follow_up, get_random_goodbye
from main_helper.classify_query import classify_query
from main_helper.schedule_manager import scheduler_function
from main_helper.gpt_response import get_gpt_response

# Continuous interaction loop
def interaction_loop(user_preferences):
    user_name = user_preferences['user_name']
    ai_name = user_preferences['ai_name']
    chosen_voice = user_preferences['voice']
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() == "bye":
            goodbye_message = get_random_goodbye() + user_name
            print(f"{ai_name}: {goodbye_message}")
            generate_spoken_audio(goodbye_message, chosen_voice, file_name='goodbye.mp3')
            break

        schedule_flag = classify_query(user_input)
        print(schedule_flag)
        
        # Initialize ai_response with a default value
        ai_response = ""
        if schedule_flag == "general":
            ai_response = get_gpt_response(user_input, user_name, ai_name)
        elif schedule_flag == "schedule":
            ai_response = scheduler_function(user_input)
        else:
            ai_response = "I'm not sure how to handle that request. Could you please rephrase?"

        follow_up_question = get_random_follow_up()
        full_response = f"{ai_response} {follow_up_question}"
        
        generate_spoken_audio(full_response, chosen_voice, file_name='response.mp3')
        
        print(f"{ai_name}: {full_response}")


# Start the interaction loop
interaction_loop(user_preferences)