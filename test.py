import pygame
import sys
from pytmx.util_pygame import load_pygame

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TMX Map Test")
clock = pygame.time.Clock()

# Load your TMX map
tmx_map = load_pygame("The Fan-tasy Tileset (Free)/Tiled/Tilemaps/Beginning Fields.tmx")

def draw_tmx_map():
    for layer in tmx_map.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, surface in layer.tiles():
                screen.blit(surface, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

# Main game loop
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    draw_tmx_map()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
