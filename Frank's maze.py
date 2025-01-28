import pygame
from pygame.locals import *
pygame.init()


Hlavni_screen_X = 1980  
Hlavni_screen_Y = 1080


Background_menu = pygame.image.load('background.jpg')
Obraz = pygame.display.set_mode((Hlavni_screen_X, Hlavni_screen_Y))


start_button = pygame.image.load('start_button.png')
quit_button = pygame.image.load('quit_button.png')


start_button_rect = start_button.get_rect()
quit_button_rect = quit_button.get_rect()



start_button_rect.topleft = ((Hlavni_screen_X - start_button_rect.width) // 2, (Hlavni_screen_Y // 2) - 200)  # 200 pixelů nad střed
quit_button_rect.topleft = ((Hlavni_screen_X - quit_button_rect.width) // 2, (Hlavni_screen_Y // 2) + 300)  # 300 pixelů pod střed


smycka = True
while smycka:
    for event in pygame.event.get():
        if event.type == QUIT:
            smycka = False

        
        if event.type == MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):  
                smycka = False  

    
    Obraz.blit(Background_menu, (0, 0))

    
    Obraz.blit(start_button, start_button_rect.topleft)

    
    Obraz.blit(quit_button, quit_button_rect.topleft)

    
    pygame.display.update()


pygame.quit()

