from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import os
import sys
from login import Login, Registro
from PIL import Image
import kivy
img = Image.open('assets/luis.png')
kivy.require('2.1.0')

Window.size = (310, 580)


class Menu(Screen):
    def desconectar(self):
        self.manager.current = "login"
    pass

class HomeScreen(Screen):
	pass

class LoginApp(MDApp):
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        self.manager = ScreenManager(transition=SlideTransition())
        self.manager.add_widget(Builder.load_file("pre-splash.kv"))
        self.manager.add_widget(Login(name='login'))
        self.manager.add_widget(Menu(name='prin'))
        self.manager.add_widget(Registro(name='reg'))
        self.manager.add_widget(HomeScreen(name = 'home'))
        return self.manager

    def on_start(self):
        Clock.schedule_once(self.login, 5)

    def login(self, *args):
        self.manager.current = "home"


if __name__ == '__main__':
    LoginApp().run()
