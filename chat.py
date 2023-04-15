import openai

def generate_response(prompt, messages):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    reply = response.choices[0].message.content.strip()
    return reply
