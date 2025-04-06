import pygame
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Load Tiled map
tmx_data = load_pygame("CollisionTest.tmx")  # Replace with your actual .tmx file

# Character setup
player_image = pygame.image.load("The Fan-tasy Tileset (Free)/Art/Characters/Main Character/Character_Walk.png").convert_alpha()  # Use your sprite
TILE_SIZE = tmx_data.tilewidth
player_x, player_y = 8, 8  # Starting tile position

current_frame = 0

def is_collidable(x, y):
    tile_gid = tmx_data.get_tile_gid(x, y, 0)
    tile_props = tmx_data.get_tile_properties_by_gid(tile_gid)
    return tile_props and tile_props.get("collidable", False)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))
    
    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    if keys[pygame.K_LEFT]:
        new_x -= 1
    elif keys[pygame.K_RIGHT]:
        new_x += 1
    elif keys[pygame.K_UP]:
        new_y -= 1
    elif keys[pygame.K_DOWN]:
        new_y += 1

    # Check for collision before moving
    if 0 <= new_x < tmx_data.width and 0 <= new_y < tmx_data.height:
        if not is_collidable(new_x, new_y):
            player_x, player_y = new_x, new_y

    # Draw map tiles
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, gid in layer:
                x-=10
                y-=10
                print((x,y,gid))
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    frame_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
                    screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE), area=frame_rect)
                else:
                    print((x,y,gid))

    # Draw character
    frame_rect = pygame.Rect(current_frame * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, (player_x * TILE_SIZE, player_y * TILE_SIZE), area=frame_rect)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
