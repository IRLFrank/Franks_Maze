import pygame
from pygame.locals import * 
pygame.init()

Hlavni_screen_X = 1980  
Hlavni_screen_Y = 1080

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

Background_menu = pygame.image.load('background.jpg')
Obraz = pygame.display.set_mode((Hlavni_screen_X, Hlavni_screen_Y))

start_button = pygame.image.load('start_button.png')
quit_button = pygame.image.load('quit_button.png')

start_button_rect = start_button.get_rect()
quit_button_rect = quit_button.get_rect()

start_button_rect.topleft = ((Hlavni_screen_X - start_button_rect.width) // 2, (Hlavni_screen_Y // 2) - 200)  
quit_button_rect.topleft = ((Hlavni_screen_X - quit_button_rect.width) // 2, (Hlavni_screen_Y // 2) + 300)  

velikost_policka = 40

Herni_okno_X = 800
Herni_okno_Y = 600
Herni_okno = pygame.Surface((Herni_okno_X, Herni_okno_Y))


maze_lvl_1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

main_screen = True
game_screen = False

Hrac_velikost = 40
Hrac_X = 40
Hrac_Y = 40
Hrac_speed = 2

Hrac_textura = pygame.image.load('hrac.png')
Hrac_textura = pygame.transform.scale(Hrac_textura, (Hrac_velikost, Hrac_velikost))

smycka = True
while smycka:
    for event in pygame.event.get():
        if event.type == QUIT:
            smycka = False

        if event.type == MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):  
                smycka = False  
            
            if start_button_rect.collidepoint(event.pos):
                game_screen = True  
                main_screen = False

    if main_screen:
        Obraz.blit(Background_menu, (0, 0))
        Obraz.blit(start_button, start_button_rect.topleft)
        Obraz.blit(quit_button, quit_button_rect.topleft)

    if game_screen:
        Herni_okno.fill(GREEN)  

        
        for radky in range(len(maze_lvl_1)):
            for sloupce in range(len(maze_lvl_1[radky])):
                if maze_lvl_1[radky][sloupce] == 1:
                    pygame.draw.rect(Herni_okno, BLACK, (sloupce * velikost_policka, radky * velikost_policka, velikost_policka, velikost_policka))

        
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            Hrac_Y -= Hrac_speed
        if keys[K_s]:
            Hrac_Y += Hrac_speed
        if keys[K_a]:
            Hrac_X -= Hrac_speed
        if keys[K_d]:
            Hrac_X += Hrac_speed
        
        
        Hrac_X = max(0, min(Herni_okno_X - Hrac_velikost, Hrac_X))
        Hrac_Y = max(0, min(Herni_okno_Y - Hrac_velikost, Hrac_Y))

        
        Herni_okno.blit(Hrac_textura, (Hrac_X, Hrac_Y))

        Herni_okno_text = pygame.font.SysFont('Arial', 50).render('Herní obrazovka', True, (255, 255, 255))
        Herni_okno.blit(Herni_okno_text, (Herni_okno_X // 2 - Herni_okno_text.get_width() // 2, 50))

        
        Obraz.blit(Herni_okno, (Hlavni_screen_X // 2 - Herni_okno_X // 2, Hlavni_screen_Y // 2 - Herni_okno_Y // 2))

    pygame.display.update()

pygame.quit()
