# test_openai.py
from openai import OpenAI

client = OpenAI()          # liest OPENAI_API_KEY automatisch

## Modelle ausgeben
#models = client.models.list()
#for m in models.data:
#    print(m.id)
#*/

reply = client.chat.completions.create(
    model="gpt-4.1-nano",   # oder "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
        {"role": "user",   "content": "Sag bitte 'Hallo Welt'!"}
    ],
    temperature=0.7
)

print(reply.choices[0].message.content)