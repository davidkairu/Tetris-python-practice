import pygame
pygame.mixer.init()

# Load and play a sound
place_sound = pygame.mixer.Sound("gameover.wav")
place_sound.play()

# Add a delay so the program doesn't exit immediately
pygame.time.delay(1000)