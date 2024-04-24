import pygame
from pygame import mixer

current_volume =0.5

def set_volume(volume):
    global current_volume
    current_volume = volume
    print("Setting volume to:", volume) 
    mixer.music.set_volume(volume)

def soundtrack(file_path):  # Default volume is 0.5
    mixer.init()
    mixer.music.load(file_path)
    set_volume(current_volume)
    mixer.music.play(-1, fade_ms=5000)