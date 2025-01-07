import pygame

from bullet import Bullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class PersonSprite(pygame.sprite.Sprite):
    '''Třída reprezentující animovanou postavu'''
    def __init__(self, x, y, sprite_sheet_path, bullets_group):
        super().__init__()
        # Načtení sprite sheetu
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Konstanty pro rozdělení sprite sheetu
        self.frame_width = 64  # Šířka jednoho snímku
        self.frame_height = 64  # Výška jednoho snímku
        self.directions = ["down", "left", "right", "up"] # Směry postavy
        self.frames = self.load_frames()  # Načtení snímků ze sprite sheetu

        # Skupina střel
        self.bullets_group = bullets_group

        # Počáteční stav
        self.image = self.frames["down"][0]  # Výchozí snímek (stojící postava)
        self.rect = self.image.get_rect(topleft=(x, y)) # Obdélníková oblast postavy
        self.current_direction = "down" # Aktuální směr
        self.animation_index = 0 # Index aktuálního snímku
        self.animation_speed = 0.1  # Rychlost animace
        self.animation_counter = 0 # Čítač pro animaci
        self.speed = 5 # Rychlost postavy
        self.is_active = False  # Příznak, zda je postava aktivní
        self.space_pressed = False  # Příznak, zda byla mezerník předtím stisknut
        self.score = 0

    def load_frames(self):
        '''Načte snímky ze sprite sheetu a uloží je do slovníku'''
        frames = {direction: [] for direction in self.directions} # Slovník pro snímky

        # Načtení snímků pro každý směr
        for i, direction in enumerate(self.directions):
            for j in range(4):  # Každý směr má 4 snímky
                # Výběr snímku ze sprite sheetu
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(j * self.frame_width, i * self.frame_height, self.frame_width, self.frame_height)
                )
                # Přidání snímku do slovníku
                frames[direction].append(frame)

        return frames

    def update(self, keys, walls):
        '''Aktualizace postavy (pohyb + animace)'''
        if not self.is_active:  # Neaktivní postava se neaktualizuje
            return
        # Nulování pohybu
        dx, dy = 0, 0
        direction = None

        # Pohyb postavy
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            direction = "left"
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            direction = "right"
        if keys[pygame.K_UP]:
            dy = -self.speed
            direction = "up"
        if keys[pygame.K_DOWN]:
            dy = self.speed
            direction = "down"

        # Pohyb postavy
        new_rect = self.rect.move(dx, dy)

        # Kontrola kolize se zdmi
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect

        # Animace postavy
        if direction:
            self.current_direction = direction # Nastavení aktuálního směru
            self.animate() # Animace postavy
        else:
            self.animation_index = 0 # Nastavení prvního snímku
            self.image = self.frames[self.current_direction][0] # Nastavení prvního snímku

        # Střelba při uvolnění mezerníku
        if keys[pygame.K_SPACE]: # Pokud je mezerník stisknut
            self.space_pressed = True # Příznak, že mezerník byl stisknut
        elif self.space_pressed:  # Pokud byla mezerník uvolněna
            self.shoot(self.bullets_group) # Vystřelení střely
            self.space_pressed = False # Příznak, že mezerník byl uvolněn

    def animate(self):
        '''Animace postavy'''
        # Přepínání snímků
        self.animation_counter += self.animation_speed # Inkrementace čítače
        if self.animation_counter >= 1: # Pokud je čítač větší nebo roven 1
            self.animation_counter = 0 # Nulování čítače
            # Přepnutí na další snímek, pokud je to možné (ještě nebyl dosažen konec seznamu)
            self.animation_index = (self.animation_index + 1) % len(self.frames[self.current_direction])
            # Nastavení nového snímku
            self.image = self.frames[self.current_direction][self.animation_index]

    def shoot(self, bullets_group):
        '''Vystřelení střely'''
        # Vytvoření střely a přidání do skupiny
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.current_direction)
        bullets_group.add(bullet)

