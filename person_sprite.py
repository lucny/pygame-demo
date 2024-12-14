import pygame


class PersonSprite(pygame.sprite.Sprite):
    '''Třída reprezentující animovanou postavu'''
    def __init__(self, x, y, sprite_sheet_path):
        super().__init__()
        # Načtení sprite sheetu
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Konstanty pro rozdělení sprite sheetu
        self.frame_width = 64  # Šířka jednoho snímku
        self.frame_height = 64  # Výška jednoho snímku
        self.directions = ["down", "left", "right", "up"]
        self.frames = self.load_frames()

        # Počáteční stav
        self.image = self.frames["down"][0]  # Výchozí snímek (stojící postava)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.current_direction = "down"
        self.animation_index = 0
        self.animation_speed = 0.1  # Rychlost animace
        self.animation_counter = 0
        self.speed = 5

    def load_frames(self):
        '''Načte snímky ze sprite sheetu a uloží je do slovníku'''
        frames = {direction: [] for direction in self.directions}

        for i, direction in enumerate(self.directions):
            for j in range(4):  # Každý směr má 4 snímky
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(j * self.frame_width, i * self.frame_height, self.frame_width, self.frame_height)
                )
                frames[direction].append(frame)

        return frames

    def update(self, keys, walls):
        '''Aktualizace postavy (pohyb + animace)'''
        dx, dy = 0, 0
        direction = None

        # Pohyb a směr
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

        # Předběžný pohyb
        new_rect = self.rect.move(dx, dy)

        # Kontrola kolizí se zdmi
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect

        # Animace
        if direction:
            self.current_direction = direction
            self.animate()
        else:
            self.animation_index = 0  # Reset na první snímek, pokud postava stojí
            self.image = self.frames[self.current_direction][0]

    def animate(self):
        '''Animace postavy'''
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.frames[self.current_direction])
            self.image = self.frames[self.current_direction][self.animation_index]
