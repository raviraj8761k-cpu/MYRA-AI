import os
import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL_NAME = "gemini-2.5-flash"

class MyraUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Conversation history for memory
        self.history = []

        # Scrollable chat display
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll.add_widget(self.chat_layout)
        self.add_widget(self.scroll)

        # Input and send layout
        input_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.text_input = TextInput(
            hint_text="Ask Myra or give coding task, Boss...",
            size_hint=(0.8, 1),
            multiline=False
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(text="Send", size_hint=(0.2, 1))
        send_btn.bind(on_press=self.send_message)

        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        self.add_widget(input_layout)

        # Initial Greeting
        self.add_chat("MYRA: Hello Boss! Main Gemini ke saath taiyar hoon. Mujhe sab yaad rahega.")

    def add_chat(self, text):
        lbl = Label(
            text=text,
            size_hint_y=None,
            height=60,
            text_size=(self.width - 20, None),
            halign='left',
            valign='middle'
        )
        lbl.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        self.chat_layout.add_widget(lbl)

    def send_message(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            return

        self.add_chat(f"Boss: {user_text}")
        self.text_input.text = ""

        # Append user message to history
        self.history.append({"role": "user", "parts": [{"text": user_text}]})

        # Run API call in background thread to avoid freezing UI
        threading.Thread(target=self.fetch_gemini_response, daemon=True).start()

    def fetch_gemini_response(self):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "system_instruction": {
                "parts": [{"text": "Your name is MYRA. You are a helpful, intelligent female AI assistant. Always call the user Boss. Reply naturally in Hindi, English or Hinglish. Remember everything discussed in the chat session."}]
            },
            "contents": self.history
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=45)
            response.raise_for_status()
            data = response.json()
            answer = data['candidates'][0]['content']['parts'][0]['text']
            
            # Append model response to history for persistent memory
            self.history.append({"role": "model", "parts": [{"text": answer}]})
        except Exception as error:
            answer = f"Boss, connection mein dikkat aayi: {str(error)}"

        Clock.schedule_once(lambda dt: self.add_chat(f"MYRA: {answer}"))

class MyraApp(App):
    def build(self):
        return MyraUI()

if __name__ == '__main__':
    MyraApp().run()
