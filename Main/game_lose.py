import pygame
from pygame import mixer

def game_lose(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1, fade_ms= 5000)

def win_music(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1, fade_ms= 5000)