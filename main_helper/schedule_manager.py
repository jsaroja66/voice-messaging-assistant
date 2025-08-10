import openai

from datetime import datetime

# Initialize OpenAI client with your API key
client = openai.OpenAI()

def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

def scheduler_function(user_prompt):
    # Read the schedule from the file
    with open("schedule.txt") as f:
        contents = f.readlines()

    # If the schedule is empty, prompt the user to write something
    if not contents:
        return "Please write a prompt in the box above"
    else:
        # Format the input prompt
        today_date = get_today_date()
        formatted_prompt = f"q: today is {today_date}, {user_prompt}\nr: \n"

        # Append the formatted prompt to the schedule content
        contents.append(formatted_prompt)

        # Join the contents to create the prompt for the AI
        combined_prompts = "".join(contents)

        # Get the AI completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant, really great at helping manage schedules. Follow the given pattern given by the user. Respond then update schedule as done before."},
                {"role": "user", "content": combined_prompts}
            ]
        )

        # Extract the AI response
        txt_response = completion.choices[0].message.content.strip()

        # Prepare the final formatted output to append to the file
        final_output = f"q: {user_prompt}\nr: {txt_response}\n"

        # Append the AI response and the final formatted output to the schedule file
        with open("schedule.txt", "a") as f:
            f.write(final_output + '\n')

        # Read the file again and print only the latest response, stopping if it encounters "date,description"
        with open("schedule.txt") as f:
            lines = f.readlines()
            # Iterate from the end to find the last "r: " response
            for line in reversed(lines):
                if line.startswith("r: "):
                    return line.strip()[3:]  # Return everything after "r: "