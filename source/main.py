from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer


def listen():
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        x = json.loads(rec.Result())
        return x['text']
    else:
        return None


def recognize(sm):
    while True:
        text = listen()
        if text is not None and text != '':
            print(text)
            if text == 'создать форму' and str(sm.current_screen) == "<Screen name='main_screen'>":
                sm.get_screen('main_screen').pressed(None)
            if text == 'назад' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').back_main(None)
            if text == 'имя' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').name_activation(None)
            if text == 'фамилия' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').surname_activation(None)
            if text == 'отчество' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').last_activation(None)
            if text == 'вниз' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').change_curs_down()
            if text == 'вверх' and str(sm.current_screen) == "<Screen name='fill_screen'>":
                sm.get_screen('fill_screen').change_curs_up()
        else:
            pass


class ScreenMain(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btn_init = Button(
            text="Create form",
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self.pressed,
        )

        boxlayout = BoxLayout(orientation="vertical", spacing=5, padding=[100])
        boxlayout.add_widget(self.btn_init)
        self.add_widget(boxlayout)

    def pressed(self, instance):
        self.parent.current = 'fill_screen'


class ScreenFill(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.btn_back = Button(
            text="back",
            background_color=[0, 1.5, 3, 1],
            size_hint=[0.1, 0.03],
            on_press=self.back_main,
        )

        self.first_name_inpt = TextInput(
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.05])
        self.surname_name_inpt = TextInput(
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.05])
        self.last_name_inpt = TextInput(
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.05])

        boxlayout = BoxLayout(orientation="vertical", spacing=20, padding=[100])
        first_label = Label(size_hint=[1, 0.05], text='Имя')
        surname_label = Label(size_hint=[1, 0.05], text='Фамилия')
        last_label = Label(size_hint=[1, 0.05], text='Отчество')
        boxlayout.add_widget(first_label)
        boxlayout.add_widget(self.first_name_inpt)
        boxlayout.add_widget(surname_label)
        boxlayout.add_widget(self.surname_name_inpt)
        boxlayout.add_widget(last_label)
        boxlayout.add_widget(self.last_name_inpt)
        boxlayout.add_widget(self.btn_back)
        self.add_widget(boxlayout)

    def back_main(self, instance):
        self.parent.current = 'main_screen'

    def name_activation(self, instance):
        self.first_name_inpt.background_color = [3, 1.5, 3, 1]
        self.surname_name_inpt.background_color = [0, 1.5, 3, 1]
        self.last_name_inpt.background_color = [0, 1.5, 3, 1]
        # print('What?')

    def surname_activation(self, instance):
        self.surname_name_inpt.background_color = [3, 1.5, 3, 1]
        self.first_name_inpt.background_color = [0, 1.5, 3, 1]
        self.last_name_inpt.background_color = [0, 1.5, 3, 1]

    def last_activation(self, instance):
        self.last_name_inpt.background_color = [3, 1.5, 3, 1]
        self.surname_name_inpt.background_color = [0, 1.5, 3, 1]
        self.first_name_inpt.background_color = [0, 1.5, 3, 1]

    def change_curs_down(self):
        if self.first_name_inpt.background_color == [3, 1.5, 3, 1]:
            self.first_name_inpt.background_color = [0, 1.5, 3, 1]
            self.surname_name_inpt.background_color = [3, 1.5, 3, 1]
        elif self.surname_name_inpt.background_color == [3, 1.5, 3, 1]:
            self.surname_name_inpt.background_color = [0, 1.5, 3, 1]
            self.last_name_inpt.background_color = [3, 1.5, 3, 1]
        else:
            pass

    def change_curs_up(self):
        if self.first_name_inpt.background_color == [3, 1.5, 3, 1]:
            pass
        elif self.surname_name_inpt.background_color == [3, 1.5, 3, 1]:
            self.surname_name_inpt.background_color = [0, 1.5, 3, 1]
            self.first_name_inpt.background_color = [3, 1.5, 3, 1]
        elif self.last_name_inpt.background_color == [3, 1.5, 3, 1]:
            self.surname_name_inpt.background_color = [3, 1.5, 3, 1]
            self.last_name_inpt.background_color = [0, 1.5, 3, 1]


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.add_widget(ScreenMain(name='main_screen'))
        self.sm.add_widget(ScreenFill(name='fill_screen'))

    def build(self):
        return self.sm

    def on_start(self):
        t = Thread(target=recognize, args=[self.sm])
        # self.parent.current = 'fill_screen'
        t.daemon = True
        t.start()


if __name__ == '__main__':

    if not os.path.exists("model"):
        print(
            "Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack "
            "as "
            "'model' in the current folder.")
        exit(1)

    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    app = MyApp()
    app.run()
