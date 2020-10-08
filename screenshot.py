import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import pyautogui
import os


if "temp_files" not in os.listdir("."):
    os.mkdir("temp_files")

class ScreenShot(FloatLayout):
    fullscreen = False
    images = []
    count = 0
    sm = ScreenManager()
    screens = []
    ctr = 0
    imgs = 3

    def __init__(self):
        super(ScreenShot, self).__init__()
        self.scr = Screen(name="Main")
        self.sm.add_widget(self.scr)
        self.image = Image(source="main.jpg")
        self.scr.add_widget(self.image)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def take_screen(self):
        Window.hide()
        Clock.schedule_interval(self.burst_shot, 1)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == 'q':
            App.stop(App.get_running_app())
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
        elif keycode[1] == 'enter' and len(self.images) != 0:
            self.images[self.ctr].save('my_image.png')
            App.stop(App.get_running_app())
        elif text == 'f':
            if self.fullscreen is False:
                Window.size = (pyautogui.getInfo()[4].width - 100, pyautogui.getInfo()[4].height - 300)
                self.fullscreen = True
            else:
                Window.size = (250, 150)
                self.fullscreen = False

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def burst_shot(self, obj):
        if self.count == self.imgs:
            self.count = 0
            print("Exiting loop")
            Window.show()
            return False
        if len(self.screens) == self.imgs:
            tmp = self.screens
            self.screens.clear()
            for i in tmp:
                self.sm.remove_widget(i)

        scr = Screen(name=f"Screen{self.count}")
        self.images.append(pyautogui.screenshot(f'temp_files/tmp{self.count}.png'))
        scr.add_widget(Image(source=f"temp_files/tmp{self.count}.png"))
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
    for i in os.listdir("temp_files"):
        os.remove(f"temp_files/{i}")
        print("Removing", i)
