import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import pyautogui
import os


class ScreenShot(FloatLayout):
    images = []
    count = 0
    sm = ScreenManager()
    screens = []
    ctr = 0
    imgs = 5

    def __init__(self):
        super(ScreenShot, self).__init__()
        self.scr = Screen(name="Main")
        self.sm.add_widget(self.scr)
        self.image = Image(source="main.jpg")
        self.scr.add_widget(self.image)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def take_screen(self):
        Clock.schedule_interval(self.burst_shot, 1)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == 'q':
            exit(0)
        elif text == 's':
            self.take_screen()
        elif len(self.screens) != 0 and keycode[1] == 'left':
            self.sm.transition.direction = 'right'
            if self.ctr == 0:
                self.ctr = self.imgs - 1
            else:
                self.ctr -= 1
            self.sm.current = f'Screen{self.ctr}'
        elif len(self.screens) != 0 and keycode[1] == 'right':
            self.sm.transition.direction = 'left'
            if self.ctr == self.imgs - 1:
                self.ctr = 0
            else:
                self.ctr += 1
            self.sm.current = f'Screen{self.ctr}'
        elif keycode[1] == 'enter':
            self.images[self.ctr].save('my_image.png')
            for i in range(self.imgs):
                os.system(f"rm tmp{i}.png")
            exit(0)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def burst_shot(self, obj):
        if self.count == self.imgs:
            self.count = 0
            print("Exiting loop")
            return False
        if len(self.screens) == self.imgs:
            tmp = self.screens
            self.screens.clear()
            for i in tmp:
                self.sm.remove_widget(i)

        scr = Screen(name=f"Screen{self.count}")
        self.images.append(pyautogui.screenshot(f'tmp{self.count}.png'))
        scr.add_widget(Image(source=f"tmp{self.count}.png"))
        self.screens.append(scr)
        self.sm.add_widget(scr)
        self.count += 1


class Preview(App):

    def build(self):
        Window.size = (250, 150)
        Window.borderless = True
        Window.position = 'custom'
        Window.top = 0
        Window.left = 0
        Window.resizable = False
        return ScreenShot().sm


if __name__ == "__main__":
    print("Running Application...")
    Preview().run()
