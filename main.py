import pygame

from custom_surface import CustomSurface

# Konstanty
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60    # Počet snímků za sekundu


class App:
    '''Hlavní třída aplikace'''
    def __init__(self):
        '''Konstruktor - Inicializace hry'''
        pygame.init()   # Inicializace Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Vytvoření okna
        pygame.display.set_caption("Pygame Demo")   # Název okna
        self.clock = pygame.time.Clock()    # Vytvoření hodin
        self.running = True     # Hra běží

        # Komponenty
        # Vytvoření vlastního Surface
        self.custom_surface = CustomSurface(200, 200, (100, 100))

    def run(self):
        '''Hlavní smyčka hry'''
        while self.running:
            self.handle_events()    # Zpracování událostí
            self.update()   # Aktualizace stavu
            self.draw()    # Vykreslení prvků
            self.clock.tick(FPS)    # Případné čekání na další snímek - nastavení počtu snímků za sekundu
        pygame.quit()   # Ukončení Pygame

    def handle_events(self):
        '''Zpracování všech událostí v hlavní smyčce hry'''
        for event in pygame.event.get():   # Projít všechny události ve frontě
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Ukončení hry
                self.running = False


    def update(self):
        '''Aktualizace herního stavu'''
        pass

    def draw(self):
        '''Vykreslení herních prvků'''
        self.screen.fill((255, 255, 0)) # Vyplnění obrazovky žlutou barvou
        self.custom_surface.draw(self.screen) # Vykreslení vlastního Surface
        pygame.display.flip() # Zobrazení vykreslených prvků


# Spuštění aplikace
if __name__ == "__main__":
    app = App()     # Vytvoření instance třídy App
    app.run()      # Spuštění hlavní smyčky hry