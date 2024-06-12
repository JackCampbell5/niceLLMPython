from openai import OpenAI

client = OpenAI()
OPENAI_API_KEY = "73a6564fb1a34743a99cf28f080f3f5a"

completion = client.chat.completions.create(
    model="gpt35turbo0613",
    messages=[
        {"role": "system",
         "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print(completion.choices[0].message)