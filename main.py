import os
import threading
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 12
    spacing: 10

    Label:
        text: '[b]MYRA AI[/b]'
        markup: True
        font_size: '28sp'
        size_hint_y: None
        height: '50dp'

    TextInput:
        id: api_key
        hint_text: 'Gemini API key yahan enter karein'
        password: True
        multiline: False
        size_hint_y: None
        height: '48dp'

    ScrollView:
        Label:
            id: chat
            text: 'MYRA: Namaste Boss! Main taiyaar hoon.\\n'
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
            valign: 'top'

    TextInput:
        id: message
        hint_text: 'Boss, kuch bhi poochhiye...'
        multiline: False
        size_hint_y: None
        height: '48dp'
        on_text_validate: app.send_message()

    Button:
        text: 'SEND'
        size_hint_y: None
        height: '48dp'
        on_release: app.send_message()
'''

class MyraApp(App):
    def build(self):
        self.chat_session = []
        return Builder.load_string(KV)

    def add_chat(self, text):
        self.root.ids.chat.text += text + '\\n'
        self.root.ids.chat.texture_update()

    def send_message(self):
        message = self.root.ids.message.text.strip()
        key = self.root.ids.api_key.text.strip()

        if not key:
            self.add_chat('MYRA: Boss, pehle Gemini API key enter karein.')
            return

        if not message:
            return

        self.root.ids.message.text = ''
        self.add_chat('Boss: ' + message)
        self.add_chat('MYRA: Soch rahi hoon...')

        threading.Thread(
            target=self.ask_gemini,
            args=(message, key),
            daemon=True
        ).start()

    def ask_gemini(self, message, key):
        try:
            url = (
                'https://generativelanguage.googleapis.com/v1beta/'
                'models/gemini-2.5-flash:generateContent'
            )
            response = requests.post(
                url,
                params={'key': key},
                json={
                    'systemInstruction': {
                        'parts': [{'text': 'You are MYRA, a helpful AI assistant. Address the user as Boss. Reply naturally in the language the user uses.'}]
                    },
                    'contents': [{'parts': [{'text': message}]}]
                },
                timeout=45
            )
            response.raise_for_status()
            data = response.json()
            answer = data['candidates'][0]['content']['parts'][0]['text']
        except Exception as error:
            answer = 'Boss, connection mein dikkat aayi: ' + str(error)

        Clock.schedule_once(lambda dt: self.add_chat('MYRA: ' + answer))

MyraApp().run()
