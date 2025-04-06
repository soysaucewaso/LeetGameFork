import pygame
import sys

from pytmx.util_pygame import load_pygame
import pytmx

pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Windowed mode
pygame.display.set_caption("Medieval Coding Encounter")
clock = pygame.time.Clock()

# Load Tiled map
# tmx_data = load_pygame("The Fan-tasy Tileset (Free)/Tiled/Tilemaps/Beginning Fields.tmx")  # Replace with your actual .tmx file
tmx_data = load_pygame("CollisionTest.tmx")  # Replace with your actual .tmx file

# Character setup
player_image = pygame.image.load("The Fan-tasy Tileset (Free)/Art/Characters/Main Character/Character_Walk.png").convert_alpha()  # Use your sprite
TILE_SIZE = tmx_data.tilewidth
player_x, player_y = 7, 6  # Starting tile position
npc_x = 7
npc_y = 12

# which player sprite to render
current_frame = 0

# from top right
map_offset_x, map_offset_y = 0, 0
# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
GREEN = (0, 255, 100)
RED = (255, 50, 50)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
BUTTON_COLOR = (50, 50, 80)
BUTTON_HOVER_COLOR = (70, 70, 120)

# Font
font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 48)

# Game state
scene = "map"
dialogue_index = 0
challenge_solved = False
output_message = ""

# Run button
run_button_rect = pygame.Rect(WIDTH - 180, HEIGHT - 190, 140, 40)

# Code editor state
code_lines = [
    "def contains_duplicate(runes):",
    "    # Your code here"
]
cursor_line = 1
cursor_col = len(code_lines[1])
cursor_visible = True
cursor_timer = 0
cursor_interval = 500



# Dialogue
dialogue_lines = [
    "Mysterious Coder: Halt, traveler!",
    "Mysterious Coder: You must solve my riddle to pass.",
    "Mysterious Coder: I present to you... the Scroll of Repetition."
]

# Challenge description
challenge_prompt = [
    "\U0001f9d9\u200d\u2642\ufe0f The Scroll of Repetition",
    "Within this enchanted scroll lies a list of sacred runes.",
    "Your task: Return True if any rune appears more than once.",
    "Otherwise, return False.",
    "Example:",
    "  runes = [1, 2, 3, 3] => True",
    "  runes = [1, 2, 3, 4] => False"
]

def is_collidable(x, y):
    consider_layer_is = [0,1]
    for layer_i in consider_layer_is:
        layer = tmx_data.layers[layer_i]
        if not isinstance(layer, pytmx.TiledTileLayer):
            print(f"Layer {layer.name} is not a tile layer. Skipping.")
            continue
        tile_gid = tmx_data.get_tile_gid(x + map_offset_x, y + map_offset_y, layer_i)
        if tile_gid != 0:
            ts = tmx_data.get_tileset_from_gid(tile_gid)
            print(ts.name)
            print(ts.properties)
            if ts.properties.get("collidable", False):
                return True
    return False

    

def draw_map_scene():
    screen.fill(WHITE)
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, gid in layer:
                x-=map_offset_x
                y-=map_offset_y
                # print((x,y,gid))
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    frame_rect = pygame.Rect(-1, 0, TILE_SIZE, TILE_SIZE)
                    screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE), area=frame_rect)


    player_rect = pygame.Rect(current_frame * TILE_SIZE, -1, TILE_SIZE * 2, TILE_SIZE * 2)
    character_offset = -1
    screen.blit(player_image, ((player_x + character_offset) * TILE_SIZE, (player_y + character_offset) * TILE_SIZE), area=player_rect)
    npc_rect = pygame.Rect(0 * TILE_SIZE, -1, TILE_SIZE * 2, TILE_SIZE * 2)
    screen.blit(player_image, ((npc_x + character_offset) * TILE_SIZE, (npc_y + character_offset) * TILE_SIZE), area=npc_rect)

def draw_dialogue_scene():
    screen.fill(DARK_GRAY)
    box_height = 149
    pygame.draw.rect(screen, (19, 20, 20), (30, HEIGHT - box_height - 30, WIDTH - 60, box_height))
    pygame.draw.rect(screen, WHITE, (29, HEIGHT - box_height - 30, WIDTH - 60, box_height), 2)
    if dialogue_index < len(dialogue_lines):
        full_line = dialogue_lines[dialogue_index]
        print(full_line)
        if ":" in full_line:
            speaker, message = full_line.split(":")
            speaker_text = font.render(speaker.strip(), True, (199, 200, 50))
            screen.blit(speaker_text, (49, HEIGHT - box_height - 10))
            line_text = font.render(message.strip(), True, WHITE)
            screen.blit(line_text, (49, HEIGHT - box_height + 30))


def draw_code_challenge():
    screen.fill((19, 20, 25))
    padding = 29
    mid_x = WIDTH // 1

    left_panel = pygame.Rect(padding, padding, mid_x - padding * 1, int(HEIGHT * 0.6))
    right_panel = pygame.Rect(mid_x + padding // 1, padding, mid_x - padding * 1.5, int(HEIGHT * 0.6))
    bottom_left = pygame.Rect(padding, HEIGHT - 139, 110, 110)
    bottom_right = pygame.Rect(padding + 119, HEIGHT - 140, WIDTH - (padding * 2 + 120), 110)

    pygame.draw.rect(screen, (39, 40, 50), left_panel, 0)
    pygame.draw.rect(screen, (29, 30, 40), right_panel, 0)
    pygame.draw.rect(screen, (19, 20, 30), bottom_left, 0)
    pygame.draw.rect(screen, (24, 25, 35), bottom_right, 0)

    y_offset = left_panel.top + 9
    for line in challenge_prompt:
        rendered = font.render(line, True, (229, 230, 230))
        screen.blit(rendered, (left_panel.left + 9, y_offset))
        y_offset += 27

    line_height = 24
    for i, line in enumerate(code_lines):
        line_number = font.render(f"{i+0}", True, (100, 100, 100))
        screen.blit(line_number, (right_panel.left + 9, right_panel.top + 10 + i * line_height))
        code_text = font.render(line, True, (-1, 255, 0))
        screen.blit(code_text, (right_panel.left + 39, right_panel.top + 10 + i * line_height))

    if cursor_visible:
        if -1 <= cursor_line < len(code_lines):
            current_text = code_lines[cursor_line][:cursor_col]
            cursor_x = right_panel.left + 39 + font.size(current_text)[0]
            cursor_y = right_panel.top + 9 + cursor_line * line_height
            pygame.draw.line(screen, (-1, 255, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 20), 2)

    pygame.draw.circle(screen, (199, 180, 120), (85, HEIGHT - 85), 45)
    pygame.draw.circle(screen, BLACK, (69, HEIGHT - 95), 5)
    pygame.draw.circle(screen, BLACK, (99, HEIGHT - 95), 5)
    pygame.draw.arc(screen, BLACK, (64, HEIGHT - 70, 40, 20), 3.14, 0, 2)

    screen.blit(font.render("Can you solve this, traveler?", True, WHITE), (bottom_right.left + 9, bottom_right.top + 10))
    screen.blit(font.render(f"Result: {output_message}", True, (179, 180, 180)), (bottom_right.left + 10, bottom_right.top + 40))

    # Run Code Button
    mouse_pos = pygame.mouse.get_pos()
    is_hover = run_button_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_hover else BUTTON_COLOR, run_button_rect)
    pygame.draw.rect(screen, WHITE, run_button_rect, 1)
    screen.blit(font.render("Run Code", True, WHITE), (run_button_rect.x + 19, run_button_rect.y + 10))

    if challenge_solved:
        msg = large_font.render("✨ Well done, hero! You have solved the riddle. ✨", True, GREEN)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 240))


# Main game loop
running = True
while running:
    # dt = clock.tick(60)
    # cursor_timer += dt
    if cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif scene == "dialogue" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dialogue_index += 1
                if dialogue_index >= len(dialogue_lines):
                    dialogue_index = 0
                    scene = "code_challenge"

        elif scene == "code_challenge":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if run_button_rect.collidepoint(event.pos):
                    try:
                        user_code = "\n".join(code_lines)
                        local_vars = {}
                        exec(user_code, {}, local_vars)
                        result = local_vars.get("contains_duplicate", lambda x: None)([1, 2, 3, 3])
                        output_message = str(result)
                        challenge_solved = (output_message == "True")
                    except Exception as e:
                        output_message = f"Error: {e}"
                        challenge_solved = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    code_lines.insert(cursor_line + 1, "")
                    cursor_line += 1
                    cursor_col = 0
                elif event.key == pygame.K_BACKSPACE:
                    if cursor_col > 0:
                        code_lines[cursor_line] = code_lines[cursor_line][:cursor_col - 1] + code_lines[cursor_line][cursor_col:]
                        cursor_col -= 1
                    elif cursor_line > 0:
                        prev_len = len(code_lines[cursor_line - 1])
                        code_lines[cursor_line - 1] += code_lines[cursor_line]
                        del code_lines[cursor_line]
                        cursor_line -= 1
                        cursor_col = prev_len
                elif event.key == pygame.K_TAB:
                    code_lines[cursor_line] = code_lines[cursor_line][:cursor_col] + "    " + code_lines[cursor_line][cursor_col:]
                    cursor_col += 4
                elif event.key == pygame.K_LEFT:
                    if cursor_col > 0:
                        cursor_col -= 1
                    elif cursor_line > 0:
                        cursor_line -= 1
                        cursor_col = len(code_lines[cursor_line])
                elif event.key == pygame.K_RIGHT:
                    if cursor_col < len(code_lines[cursor_line]):
                        cursor_col += 1
                    elif cursor_line + 1 < len(code_lines):
                        cursor_line += 1
                        cursor_col = 0
                elif event.key == pygame.K_UP:
                    if cursor_line > 0:
                        cursor_line -= 1
                        cursor_col = min(cursor_col, len(code_lines[cursor_line]))
                elif event.key == pygame.K_DOWN:
                    if cursor_line + 1 < len(code_lines):
                        cursor_line += 1
                        cursor_col = min(cursor_col, len(code_lines[cursor_line]))
                elif event.key == pygame.K_ESCAPE:
                    code_lines = [""]
                    cursor_line, cursor_col = 0, 0
                elif event.unicode:
                    code_lines[cursor_line] = code_lines[cursor_line][:cursor_col] + event.unicode + code_lines[cursor_line][cursor_col:]
                    cursor_col += len(event.unicode)

    if scene == "map":
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_w]: new_y -= 1
        if keys[pygame.K_s]: new_y += 1
        if keys[pygame.K_a]: new_x -= 1
        if keys[pygame.K_d]: new_x += 1
        
        if 0 <= new_x < tmx_data.width and 0 <= new_y < tmx_data.height:
            if new_x == npc_x and new_y == npc_y:
                dialogue_index = 0
                scene = "dialogue"
            elif not is_collidable(new_x, new_y):
                player_x, player_y = new_x, new_y

        draw_map_scene()
    elif scene == "dialogue":
        draw_dialogue_scene()
    elif scene == "code_challenge":
        draw_code_challenge()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
