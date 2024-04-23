import pygame
from pygame import mixer

# This function plays a voice file once without looping and without a fade-in effect.
def Voice(file_path):
    # Ensure the mixer is initialized (it's okay if this is called multiple times, but it's
    # more efficient to do it once at the start of your program)
    if not mixer.get_init():
        mixer.init()
    
    # Load the voice file
    mixer.music.load(file_path)
    
    # Set a reasonable volume; adjust as needed
    mixer.music.set_volume(0.2)
    
    # Play the audio once; remove the fade_ms parameter if no fade-in is desired
    mixer.music.play()
