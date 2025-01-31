import pygame
from pygame.locals import *
import random

pygame.init()

# -------------------------- HLAVNÍ ROZMĚRY OKNA -----------------------------
Hlavni_screen_X = 1980  
Hlavni_screen_Y = 1080
Obraz = pygame.display.set_mode((Hlavni_screen_X, Hlavni_screen_Y))

# ----------------------------- POZADÍ ---------------------------------------
Background_menu = pygame.image.load('background.jpg')

# ----------------------------- TLAČÍTKA --------------------------------------
start_button = pygame.image.load('start_button.png')
quit_button = pygame.image.load('quit_button.png')

start_button_rect = start_button.get_rect()
quit_button_rect = quit_button.get_rect()

start_button_rect.topleft = ((Hlavni_screen_X - start_button_rect.width) // 2,
                             (Hlavni_screen_Y // 2) - 200)  
quit_button_rect.topleft = ((Hlavni_screen_X - quit_button_rect.width) // 2,
                            (Hlavni_screen_Y // 2) + 300)  

# ------------------------ ROZMĚRY HERNÍHO OKNA --------------------------------
Herni_okno_X = 800
Herni_okno_Y = 600
Herni_okno = pygame.Surface((Herni_okno_X, Herni_okno_Y))

# ------------------------ PARAMETRY BUŇKY A BLUDIŠTĚ -------------------------
velikost_bunky = 40
sloupce = Herni_okno_X // velikost_bunky
radky = Herni_okno_Y // velikost_bunky      

# ----------------------------  BUNKA -----------------------------------
class Bunka:
    def __init__(self, sloupec, radek):
        self.sloupec = sloupec      
        self.radek = radek          
        self.steny = {'hore': True, 'vpravo': True, 'dole': True, 'vlevo': True}
        self.navstivena = False

# ------------------ DEJ_INDEX  ------------------
def dej_index(sloupec, radek):
    
    if sloupec < 0 or radek < 0 or sloupec >= sloupce_global or radek >= radky_global:
        return None
    return radek * sloupce_global + sloupec


sloupce_global = sloupce
radky_global = radky

# -----------------  GENERUJ_BLUDIŠTĚ recursive backtracking -----------------------
def generuj_bludiste():
    
    mrizka_local = [Bunka(c, r) for r in range(radky) for c in range(sloupce)]
    
    zasobnik = []
    
    aktualni = mrizka_local[0]
    aktualni.navstivena = True

    while True:
        sousedi = []  
       
        smery = [('hore', 0, -1), ('vpravo', 1, 0), ('dole', 0, 1), ('vlevo', -1, 0)]
        
        for smer, d_sloupec, d_radek in smery:
            index_souseda = dej_index(aktualni.sloupec + d_sloupec, aktualni.radek + d_radek)
            if index_souseda is not None:
                soused = mrizka_local[index_souseda]
                if not soused.navstivena:
                    sousedi.append((smer, soused))
        
        if sousedi:
            
            vybrany_smer, vybrany = random.choice(sousedi)
            
            
            if vybrany_smer == 'hore':
                aktualni.steny['hore'] = False
                vybrany.steny['dole'] = False
            elif vybrany_smer == 'vpravo':
                aktualni.steny['vpravo'] = False
                vybrany.steny['vlevo'] = False
            elif vybrany_smer == 'dole':
                aktualni.steny['dole'] = False
                vybrany.steny['hore'] = False
            elif vybrany_smer == 'vlevo':
                aktualni.steny['vlevo'] = False
                vybrany.steny['vpravo'] = False

            zasobnik.append(aktualni)
            aktualni = vybrany
            aktualni.navstivena = True
        elif zasobnik:
            aktualni = zasobnik.pop()
        else:
            break
    return mrizka_local

# ----------------------- PARAMETRY HRÁČE a HERNÍ PROMĚNNÉ -----------------------
Hrac_velikost = 40
Hrac_X = Herni_okno_X // 2 - Hrac_velikost // 2
Hrac_Y = Herni_okno_Y // 2 - Hrac_velikost // 2
Hrac_speed = 2

Hrac_textura = pygame.image.load('hrac.png')
Hrac_textura = pygame.transform.scale(Hrac_textura, (Hrac_velikost, Hrac_velikost))

main_screen = True
game_screen = False


bludiste = None
bludiste_vygenerovano = False

# ------------------------- HLAVNÍ SMYČKA ---------------------------------------
smycka = True
while smycka:
    for udalost in pygame.event.get():
        if udalost.type == QUIT:
            smycka = False
        if udalost.type == MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(udalost.pos):
                smycka = False
            if start_button_rect.collidepoint(udalost.pos):
                game_screen = True
                main_screen = False

    if main_screen:
        Obraz.blit(Background_menu, (0, 0))
        Obraz.blit(start_button, start_button_rect.topleft)
        Obraz.blit(quit_button, quit_button_rect.topleft)

    if game_screen:
        Herni_okno.fill((0, 255, 0))  #  herní okno barva

       
        if not bludiste_vygenerovano:
            bludiste = generuj_bludiste()
            bludiste_vygenerovano = True

        # Vykreslení bludiště
        for bunka in bludiste:
            x = bunka.sloupec * velikost_bunky
            y = bunka.radek * velikost_bunky
            if bunka.steny['hore']:
                pygame.draw.line(Herni_okno, (0, 0, 0), (x, y), (x + velikost_bunky, y), 2)
            if bunka.steny['vpravo']:
                pygame.draw.line(Herni_okno, (0, 0, 0), (x + velikost_bunky, y), (x + velikost_bunky, y + velikost_bunky), 2)
            if bunka.steny['dole']:
                pygame.draw.line(Herni_okno, (0, 0, 0), (x + velikost_bunky, y + velikost_bunky), (x, y + velikost_bunky), 2)
            if bunka.steny['vlevo']:
                pygame.draw.line(Herni_okno, (0, 0, 0), (x, y + velikost_bunky), (x, y), 2)

        # Ovládání hráče
        klavesy = pygame.key.get_pressed()
        if klavesy[K_w]:
            Hrac_Y -= Hrac_speed
        if klavesy[K_s]:
            Hrac_Y += Hrac_speed
        if klavesy[K_a]:
            Hrac_X -= Hrac_speed
        if klavesy[K_d]:
            Hrac_X += Hrac_speed

        
        Hrac_X = max(0, min(Herni_okno_X - Hrac_velikost, Hrac_X))
        Hrac_Y = max(0, min(Herni_okno_Y - Hrac_velikost, Hrac_Y))

        Herni_okno.blit(Hrac_textura, (Hrac_X, Hrac_Y))
        Obraz.blit(Herni_okno, (Hlavni_screen_X // 2 - Herni_okno_X // 2,
                                 Hlavni_screen_Y // 2 - Herni_okno_Y // 2))

    pygame.display.update()

pygame.quit()
