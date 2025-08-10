import openai

# Initialize OpenAI client with your API key
client = openai.OpenAI()

def classify_query(user_prompt):
    # Send the user prompt to the AI for classification
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Simply say 'schedule' if related to schedule and say 'general' if the question is a general question. Be brief."},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Extract the classification from the AI's response
    classification = completion.choices[0].message.content.strip().lower()
    return classification