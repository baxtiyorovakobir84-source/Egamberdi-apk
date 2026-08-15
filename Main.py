from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from groq import Groq

Window.clearcolor = (0.95, 0.95, 0.95, 1)

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)


class EgamberdiApp(App):

    def build(self):
        main_layout = BoxLayout(
            orientation="vertical", padding=[10, 10, 10, 10], spacing=10
        )

        self.scroll = ScrollView(size_hint=(1, 0.92), do_scroll_x=False)
        self.chat_history = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=10
        )
        self.chat_history.bind(
            minimum_height=self.chat_history.setter("height")
        )

        self.scroll.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll)

        input_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.08), spacing=8
        )
        self.text_input = TextInput(
            hint_text="Egamberdiga yozing...",
            multiline=False,
            size_hint=(0.75, 1),
            font_size="15sp",
        )

        send_btn = Button(
            text="Yuborish",
            size_hint=(0.25, 1),
            background_color=(0.2, 0.5, 0.8, 1),
            font_size="13sp",
            bold=True,
        )
        send_btn.bind(on_press=self.send_message)

        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)

        Clock.schedule_once(
            lambda dt: self.add_message(
                "Salom! Men Egamberdi. Savolingiz bormi?", False
            ),
            0.5,
        )
        return main_layout

    def add_message(self, text, is_user):
        screen_w = Window.width if Window.width > 0 else 400
        msg_w = screen_w * 0.75

        lbl = Label(
            text=text,
            size_hint=(None, None),
            color=(0.1, 0.1, 0.1, 1),
            text_size=(msg_w - 20, None),
            font_size="15sp",
            halign="left",
            valign="top",
        )

        lbl.bind(
            texture_size=lambda instance, val: setattr(
                instance, "size", (msg_w, val[1] + 20)
            )
        )

        bubble = BoxLayout(
            size_hint=(1, None), padding=[5, 5], spacing=5
        )

        if is_user:
            bubble.add_widget(BoxLayout(size_hint_x=0.25))
            lbl.color = (0, 0.3, 0.8, 1)
            bubble.add_widget(lbl)
        else:
            lbl.color = (0.1, 0.6, 0.2, 1)
            bubble.add_widget(lbl)
            bubble.add_widget(BoxLayout(size_hint_x=0.25))

        lbl.bind(
            size=lambda instance, val: setattr(
                bubble, "height", instance.height + 10
            )
        )

        self.chat_history.add_widget(bubble)
        Clock.schedule_once(
            lambda dt: setattr(self.scroll, "scroll_y", 0), 0.1
        )

    def send_message(self, instance):
        text = self.text_input.text.strip()
        if text:
            self.add_message(text, True)
            self.text_input.text = ""
            Clock.schedule_once(lambda dt: self.get_ai_response(text), 0.2)

    def get_ai_response(self, text):
        try:
            chat = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": text}],
            )
            self.add_message(chat.choices[0].message.content, False)
        except Exception as e:
            self.add_message("Xatolik yuz berdi :(", False)


if __name__ == "__main__":
    EgamberdiApp().run()
