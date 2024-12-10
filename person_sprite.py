import pygame


class PersonSprite(pygame.sprite.Sprite):
    '''Třída představující pohyblivou postavu'''
    def __init__(self, x, y, image_path="media/person.png"):
        super().__init__()
        self.image = pygame.image.load(image_path)  # Načtení obrázku postavy
        self.image = pygame.transform.scale(self.image, (40, 60))  # Změna velikosti
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys, walls):
        '''Aktualizace pozice postavy'''
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Předběžný pohyb
        new_rect = self.rect.move(dx, dy)

        # Kontrola kolizí se zdmi
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect
