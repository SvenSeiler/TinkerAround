import time
from openai import OpenAI
client = OpenAI()
assistant_id="asst_F9zSrohOfFOVeiRm5RUjnfKQ"

# 1) Assistant definieren (einmalig)
#assistant = client.beta.assistants.create(
#    name="Buchhaltungs-GPT",
#    instructions=(
#        "Du bist ein deutscher Buchhaltungsassistent. "
#        "Antworte immer im DATEV-Stil und gib SKR-03-Konten an."
#    ),
#    model="gpt-4o-mini",
#    tools=[{"type": "code_interpreter"}],   # z. B. Python-Sandbox
#    metadata={"version": "2025-04-27"}
#)
#assistant_id = assistant.id           # ---> merken!
#print("Assistant-ID:", assistant_id)

# 2) Für jedes Gespräch einen neuen Thread
thread = client.beta.threads.create()
thread_id = thread.id                 # ---> merken!

# 3) Erste User-Nachricht anhängen
client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="Wie buche ich eine Rechnung über 119 € netto?"
)

# 4) Run starten
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
)

# 5) Auf Abschluss warten
while run.status not in {"completed", "failed", "cancelled", "expired"}:
    time.sleep(0.5)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,          # **immer Keyword-Args!**
        run_id=run.id
    )

# 6) Letzte Antwort aus dem Thread holen
#messages = client.beta.threads.messages.list(thread_id=thread_id)
#print(messages.data[-1].content[0].text.value)


# 7) Ausgabe als Stream

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant_id
) as stream:
    for text in stream.text_deltas:      # nur Textstücke
        print(text, end="", flush=True)

print("\n\n--- fertig ---")

