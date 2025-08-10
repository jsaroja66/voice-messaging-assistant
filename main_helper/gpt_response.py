# Function to interact with GPT-4 and get a response
def get_gpt_response(user_input, user_name, ai_name):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant to {user_name}. Name {ai_name}. You like to keep your messages short but friendly."},
            {"role": "user", "content": user_input},
        ]
    )
    return response.choices[0].message['content']