from pip._internal import main
from sys import platform



_all_ = [
    "pyautogui>=0.9.52"
]

def install(packages):
    for package in packages:
        main(['install', package])


if __name__ == '__main__':
    _windows_ = [
        "docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew",
        "kivy.deps.gstreamer",
        "kivy.deps.angle"
    ]
    install(_all_)
    if platform == "windows":
        install(_windows_)
    install(['kivy>=1.11.1'])
