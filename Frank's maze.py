import pygame
from pygame.locals import *
import time
import heapq
import random
pygame.init()
#---------------------------------------------------------------------------------------#


# Seznam soundtrack
soundtracks = ["song1.mp3", "song2.mp3", "song3.mp3"]
pred_song = None

def hraj_hudbu():
    global pred_song
    pouzitelne_songs = [song for song in soundtracks if song != pred_song] 
    if not pouzitelne_songs:  
        pouzitelne_songs = soundtracks
    
    song = random.choice(pouzitelne_songs)
    pygame.mixer.music.stop()  
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)  
    pred_song = song  

hraj_hudbu()

# Timer pro změnu soundtracku každé 2 minuty (120 000 ms)
pygame.time.set_timer(pygame.USEREVENT, 180000)


#---------------------------------------------------------------------------------------#
HP = 8  # Počet životů hráče

def vykresli_zivoty(herni_okno):
    global HP
    max_zivoty = 8  # Maximální počet životů
    x_vsesrdce = 10  # Počáteční pozice x pro první srdce
    y_vsesrdce = 10  # Pozice y pro všechna srdce

    for i in range(max_zivoty):
        if i < HP:
            herni_okno.blit(heart_full, (x_vsesrdce + i * 55, y_vsesrdce))  # Plné srdce
        else:
            herni_okno.blit(heart_empty, (x_vsesrdce + i * 55, y_vsesrdce))  # Prázdné srdce



#---------------------------------------------------------------------------------------#
Hlavni_screen_X = 1980
Hlavni_screen_Y = 1080
BLACK = (0, 0, 0)  # Barva stěn
WHITE = (255, 255, 255)
GREEN = (0, 0, 0)  # Barva pozadí
BROWN = (169, 66, 19)  # Casovac
font = pygame.font.SysFont("Arial", 30)

velikost_policka = 40
Herni_okno_X = 1400
Herni_okno_Y = 800                       
Herni_okno = pygame.Surface((Herni_okno_X, Herni_okno_Y))

smycka = True
clock = pygame.time.Clock()


#---------------------------------------------------------------------------------------#


Pozadi_menu = pygame.image.load('background.png')
image_width, image_height = Pozadi_menu.get_size()
pomer_stran = image_width / image_height
if Hlavni_screen_X / Hlavni_screen_Y > pomer_stran:
    new_width = int(Hlavni_screen_Y * pomer_stran)
    new_height = Hlavni_screen_Y
else:
    new_width = Hlavni_screen_X
    new_height = int((Hlavni_screen_X / pomer_stran))
Backgroundcele = pygame.transform.scale(Pozadi_menu, (new_width, new_height))
center_x = (Hlavni_screen_X - new_width) // 2
center_y = (Hlavni_screen_Y - new_height) // 2
Obraz = pygame.display.set_mode((Hlavni_screen_X, Hlavni_screen_Y))




#---------------------------------------------------------------------------------------#


end_screen_image = pygame.image.load("END.png")
end_screen_image = pygame.transform.scale(end_screen_image, (1400, 790))

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (velikost_policka, velikost_policka))


start_button = pygame.image.load('start_button.png')    
quit_button = pygame.image.load('quit_button.png')
start_button_rect = start_button.get_rect()
quit_button_rect = quit_button.get_rect()                       
start_button_rect.topleft = ((Hlavni_screen_X - start_button_rect.width) // 2, (Hlavni_screen_Y // 2) - 0)  
quit_button_rect.topleft = ((Hlavni_screen_X - quit_button_rect.width) // 2, (Hlavni_screen_Y // 2) + 395)


#---------------------------------------------------------------------------------------#


# Načtení obrázků srdcí (50x50 px, neprůhledné)
heart_full = pygame.image.load("heart_full.png")  # Plné srdce
heart_half = pygame.image.load("heart_half.png")  # Poloviční srdce
heart_empty = pygame.image.load("heart_empty.png")  # Prázdné srdce

# Změna velikosti na 50x50 px (pro jistotu)
heart_full = pygame.transform.scale(heart_full, (50, 50))
heart_half = pygame.transform.scale(heart_half, (50, 50))
heart_empty = pygame.transform.scale(heart_empty, (50, 50))

# Počet životů hráče (max 8)
zivoty = 8


#---------------------------------------------------------------------------------------#


# pozadi lvls
background_lvls = [
    pygame.image.load('Background_herni_image1.png'),  
    pygame.image.load('Background_herni_image2.png'),  
    pygame.image.load('Background_herni_image3.png'),  
    pygame.image.load('Background_herni_image4.png')   
]

death_screen = pygame.image.load("DIED.png")  # Ujisti se, že soubor existuje

def load_maze_from_file(filename):
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip().split()]
            maze.append(row)
    return maze

maze_lvls = [
    load_maze_from_file("level1.txt"), 
    load_maze_from_file("level2.txt"), 
    load_maze_from_file("level3.txt"),        
    load_maze_from_file("level4.txt")
]

aktualni_lvl = 0
maze = maze_lvls[aktualni_lvl]

main_screen = True
game_screen = False


#---------------------------------------------------------------------------------------#


Hrac_velikost = 25
start_x = 40  
start_y = 40  
Hrac_X = start_x  
Hrac_Y = start_y  

Hrac_rychlost_enemy = 10
Hrac_textura = pygame.image.load('hrac.png')
Hrac_textura = pygame.transform.scale(Hrac_textura, (Hrac_velikost, Hrac_velikost))    

start_time = None  
uplynulicas = 0


#---------------------------------------------------------------------------------------#

mapa_zobrazena = False
text_dungeonu = font.render("Našel jsi mapu dungeonu!", True, (255, 255, 255))  
aktivovane_barel = set()

#---------------------------------------------------------------------------------------#
end_screen_shown = False
dokoncenych_levelu = 0

def check_level_complete():
    global aktualni_lvl, maze, Hrac_X, Hrac_Y, main_screen, game_screen, start_time, dokoncenych_levelu, end_screen_shown
    
    misto_x = (len(maze[0]) - 2) * velikost_policka
    misto_y = (len(maze) - 2) * velikost_policka

    if maze[Hrac_Y // velikost_policka][Hrac_X // velikost_policka] == 2:
        dokoncenych_levelu += 1
        if aktualni_lvl + 1 < len(maze_lvls):
            aktualni_lvl += 1
            maze = maze_lvls[aktualni_lvl]
            Hrac_X, Hrac_Y = 40, 40
            start_time = time.time()
        else:
            end_screen_shown = True 
            game_screen = False 
           

def zobrazit_informace(herni_okno, font, aktualni_lvl, dokoncenych_levelu):
    level_text = font.render(f"Level: {aktualni_lvl + 1}", True, BROWN)
    herni_okno.blit(level_text, (100, 10))
            
def zobrazit_end_screen():
    global end_screen_shown
    if end_screen_shown:
        Obraz.blit(end_screen_image, ( 290, 140 ))
        pygame.display.update()

        
          
#---------------------------------------------------------------------------------------#
            
            
def byla_kolize(nove_x, nove_y):
    body_ke_kontrole = [         
        (nove_x, nove_y),  
        (nove_x + Hrac_velikost - 1, nove_y),  
        (nove_x, nove_y + Hrac_velikost - 1),                                     
        (nove_x + Hrac_velikost - 1, nove_y + Hrac_velikost - 1)  
    ]

    for bx, by in body_ke_kontrole:
        maze_x = bx // velikost_policka
        maze_y = by // velikost_policka
        if maze[maze_y][maze_x] == 1:  
            return True  
    return False


#---------------------------------------------------------------------------------------#


def zobraz_vizi(maze, player_x, player_y, radius=0):
    for radky in range(player_y - radius, player_y + radius + 0):
        for sloupce in range(player_x - radius, player_x + radius + 0):
            if 0 <= radky < len(maze) and 0 <= sloupce < len(maze[radky]):                              
                if maze[radky][sloupce] == 1:  
                    pygame.draw.rect(Herni_okno, GREEN, (sloupce * velikost_policka, radky * velikost_policka, velikost_policka, velikost_policka))  
                elif maze[radky][sloupce] == 2:  
                    exit_image = pygame.image.load('cil.png')
                    exit_image = pygame.transform.scale(exit_image, (velikost_policka, velikost_policka))
                    Herni_okno.blit(exit_image, (sloupce * velikost_policka, radky * velikost_policka))
                elif maze[radky][sloupce] == 5:  
                    barrel_image = pygame.image.load('barel.png')  
                    barrel_image = pygame.transform.scale(barrel_image, (velikost_policka, velikost_policka))
                    Herni_okno.blit(barrel_image, (sloupce * velikost_policka, radky * velikost_policka))  


#---------------------------------------------------------------------------------------#
                    
                    
def check_barrel():
    global start_time, mapa_zobrazena
    barel_x, barel_y = Hrac_X // velikost_policka, Hrac_Y // velikost_policka
    
    if maze[barel_y][barel_x] == 5 and (barel_x, barel_y) not in aktivovane_barel:
        aktivovane_barel.add((barel_x, barel_y))  
        start_time = time.time()  
        mapa_zobrazena = True
             
def zobrazit_celou_mapu(maze, player_x, player_y, radius=0):
    for radky in range(len(maze)):
        for sloupce in range(len(maze[radky])):
            if maze[radky][sloupce] == 1:  # Stěny
                pygame.draw.rect(Herni_okno, GREEN, (sloupce * velikost_policka, radky * velikost_policka, velikost_policka, velikost_policka))
            elif maze[radky][sloupce] == 2:  # Cíl
                exit_image = pygame.image.load('cil.png')
                exit_image = pygame.transform.scale(exit_image, (velikost_policka, velikost_policka))
                Herni_okno.blit(exit_image, (sloupce * velikost_policka, radky * velikost_policka))
            elif maze[radky][sloupce] == 5:  # Barely
                barrel_image = pygame.image.load('barel.png')
                barrel_image = pygame.transform.scale(barrel_image, (velikost_policka, velikost_policka))
                Herni_okno.blit(barrel_image, (sloupce * velikost_policka, radky * velikost_policka))

# Hlavní smyčka
smycka = True
clock = pygame.time.Clock()
#---------------------------------------------------------------------------------------#
class Enemy:
    def __init__(self, x, y):
        self.x = x * velikost_policka
        self.y = y * velikost_policka
        self.path = []

    def move_towards(self):
        if not self.path:  # Pokud nepřítel nemá žádnou cestu, nic nedělá
            return  

        next_x, next_y = self.path.pop(0)  # Vezme další bod v cestě
        rychlost_enemy = 1  # Nastav rychlost pohybu nepřítele

        # Výpočet směru pohybu
        smer_x = (next_x * velikost_policka - self.x)
        smer_y = (next_y * velikost_policka - self.y)

        if abs(smer_x) > rychlost_enemy:
            self.x += rychlost_enemy if smer_x > 0 else -rychlost_enemy
        else:
            self.x = next_x * velikost_policka

        if abs(smer_y) > rychlost_enemy:
            self.y += rychlost_enemy if smer_y > 0 else -rychlost_enemy
        else:
            self.y = next_y * velikost_policka

        # Kontrola kolize s hráčem
        if abs(self.x - Hrac_X) < velikost_policka and abs(self.y - Hrac_Y) < velikost_policka:
            print("Nepřítel zasáhl hráče! Odebrání nepřítele.")
            enemies.remove(self)  # Nepřítel zmizí

    def draw(self, screen):
        screen.blit(enemy_image, (self.x, self.y))

# Funkce pro načtení nepřátel
def load_enemies():
    enemies = []  # Seznam nepřátel
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 8:  # Pokud je to nepřítel
                enemies.append(Enemy(x, y))  # Vytvoří instanci třídy Enemy
    return enemies  # Vrátí seznam nepřátel

# Inicializace nepřátel
enemies = load_enemies()

#---------------------------------------------------------------------------------------#
            
            
# A* Algoritmus pro nalezení nejkratší cesty
def astar(start, goal, maze):
    heap = []
    heapq.heappush(heap, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    while heap:
        _, current = heapq.heappop(heap)
        
        if current == goal:
            break
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (int(current[0] + dx), int(current[1] + dy))
            if 0 <= next_pos[1] < len(maze) and 0 <= next_pos[0] < len(maze[0]) and maze[next_pos[1]][next_pos[0]] != 1:
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(goal[0] - next_pos[0]) + abs(goal[1] - next_pos[1])
                    heapq.heappush(heap, (priority, next_pos))
                    came_from[next_pos] = current
    
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()

    # Debugging výpis
    print(f"A* cesta z {start} do {goal}: {path}")

    return path
#---------------------------------------------------------------------------------------#

def reset_game():
    global HP, Hrac_X, Hrac_Y, enemies, aktualni_lvl, start_time, mapa_zobrazena
    HP = 8  # Reset životů
    Hrac_X, Hrac_Y = start_x, start_y  # Reset pozice hráče
    enemies = load_enemies()  # Načtení nepřátel z mapy
    aktualni_lvl = 0  # Reset úrovně na první
    start_time = None  # Reset času startu
    mapa_zobrazena = False  # Reset mapy


#---------------------------------------------------------------------------------------#

# Přidání proměnných pro sledování smrti
player_dead = False
death_time = None

# Hlavní smyčka hry
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
                reset_game()  # Když začne nová hra, vše se resetuje

        if event.type == pygame.USEREVENT:
            hraj_hudbu()

    if main_screen:
        Obraz.blit(Backgroundcele, (center_x, center_y))
        Obraz.blit(start_button, start_button_rect.topleft)
        Obraz.blit(quit_button, quit_button_rect.topleft)

    if game_screen:
        if not player_dead:
            Herni_okno.fill(GREEN)
            current_background = background_lvls[aktualni_lvl]
            current_background = pygame.transform.scale(current_background, (Herni_okno_X, Herni_okno_Y))
            Herni_okno.blit(current_background, (0, 0))

            if start_time is None:
                start_time = time.time()

            zobraz_vizi(maze, Hrac_X // velikost_policka, Hrac_Y // velikost_policka, radius=3)
            check_barrel()

            # Ovládání hráče
            keys = pygame.key.get_pressed()
            new_x, new_y = Hrac_X, Hrac_Y

            if keys[K_w]:
                new_y -= Hrac_rychlost_enemy
            if keys[K_s]:
                new_y += Hrac_rychlost_enemy
            if keys[K_a]:
                new_x -= Hrac_rychlost_enemy
            if keys[K_d]:
                new_x += Hrac_rychlost_enemy

            if not byla_kolize(new_x, new_y):
                Hrac_X, Hrac_Y = new_x, new_y

            Herni_okno.blit(Hrac_textura, (Hrac_X, Hrac_Y))

            check_level_complete()

            zobrazit_informace(Herni_okno, font, aktualni_lvl, dokoncenych_levelu)

            if mapa_zobrazena:
                zobrazit_celou_mapu(maze, Hrac_X // velikost_policka, Hrac_Y // velikost_policka, radius=0)

            if mapa_zobrazena and time.time() - start_time > 3:
                mapa_zobrazena = False

            for enemy in enemies:
                distance_x = abs(enemy.x - Hrac_X) // velikost_policka
                distance_y = abs(enemy.y - Hrac_Y) // velikost_policka

                if distance_x <= 5 and distance_y <= 5:
                    enemy.draw(Herni_okno)

            # 💀 ***Pohyb nepřátel a kontrola kolize*** 💀
            to_remove = []

            for enemy in enemies:
                enemy_grid_x, enemy_grid_y = enemy.x // velikost_policka, enemy.y // velikost_policka
                player_grid_x, player_grid_y = Hrac_X // velikost_policka, Hrac_Y // velikost_policka

                if abs(enemy_grid_x - player_grid_x) <= 5 and abs(enemy_grid_y - player_grid_y) <= 3:
                    enemy.path = astar((enemy_grid_x, enemy_grid_y), (player_grid_x, player_grid_y), maze)

                enemy.move_towards()

                if abs(enemy.x - Hrac_X) < velikost_policka and abs(enemy.y - Hrac_Y) < velikost_policka:
                    print("Nepřítel zasáhl hráče! Odebrání nepřítele.")
                    HP -= 1
                    to_remove.append(enemy)

                    if HP <= 0:
                        player_dead = True
                        death_time = pygame.time.get_ticks()

            for enemy in to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)

            # 🩸 ***Vykreslení health baru*** 🩸
            vykresli_zivoty(Herni_okno)

            Obraz.blit(Herni_okno, (Hlavni_screen_X // 2 - Herni_okno_X // 2, Hlavni_screen_Y // 2 - Herni_okno_Y // 2))

        else:  # Když je hráč mrtvý
            Obraz.blit(death_screen, (0, 0))  # Zobrazení died.png

            if pygame.time.get_ticks() - death_time > 6000:  # Po 6 sekundách přepnout na menu a restartovat hru
                game_screen = False
                main_screen = True
                player_dead = False
                death_time = None
                reset_game()  # Reset hry

    if end_screen_shown:
        zobrazit_end_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
