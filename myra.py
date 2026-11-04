import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("MYRA: Boss, Gemini API key nahi mili.")
    raise SystemExit

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "system_instruction": (
            "Your name is MYRA. You are a helpful, intelligent female AI assistant. "
            "Always call the user Boss. Reply naturally in Hindi, English or Hinglish "
            "according to the user's language. Be friendly, concise and helpful."
        )
    }
)

print("MYRA: Hello Boss! Main Gemini ke saath taiyar hoon.")
print("MYRA: Aap mujhse Hindi ya English mein baat kar sakte hain.")

while True:
    try:
        text = input("\nBoss: ").strip()

        if text.lower() in ["exit", "band", "bye", "quit"]:
            print("MYRA: Bye Boss! Phir milte hain.")
            break

        if not text:
            continue

        response = chat.send_message(text)
        print("\nMYRA:", response.text or "Boss, mujhe jawab nahi mila.")

    except KeyboardInterrupt:
        print("\nMYRA: Bye Boss!")
        break
    except Exception as e:
        print("\nMYRA: Boss, connection mein problem aayi.")
        print("Error:", str(e))
