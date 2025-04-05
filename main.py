import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Windowed mode
pygame.display.set_caption("Medieval Coding Encounter")
clock = pygame.time.Clock()

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

# Player and NPC
player = pygame.Rect(100, 100, 40, 40)
player_speed = 5
npc = pygame.Rect(500, 300, 50, 50)

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


def draw_map_scene():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, GREEN, npc)


def draw_dialogue_scene():
    screen.fill(DARK_GRAY)
    box_height = 150
    pygame.draw.rect(screen, (20, 20, 20), (30, HEIGHT - box_height - 30, WIDTH - 60, box_height))
    pygame.draw.rect(screen, WHITE, (30, HEIGHT - box_height - 30, WIDTH - 60, box_height), 2)
    if dialogue_index < len(dialogue_lines):
        full_line = dialogue_lines[dialogue_index]
        if ":" in full_line:
            speaker, message = full_line.split(":", 1)
            speaker_text = font.render(speaker.strip(), True, (200, 200, 50))
            screen.blit(speaker_text, (50, HEIGHT - box_height - 10))
            line_text = font.render(message.strip(), True, WHITE)
            screen.blit(line_text, (50, HEIGHT - box_height + 30))


def draw_code_challenge():
    screen.fill((20, 20, 25))
    padding = 30
    mid_x = WIDTH // 2

    left_panel = pygame.Rect(padding, padding, mid_x - padding * 2, int(HEIGHT * 0.6))
    right_panel = pygame.Rect(mid_x + padding // 2, padding, mid_x - padding * 1.5, int(HEIGHT * 0.6))
    bottom_left = pygame.Rect(padding, HEIGHT - 140, 110, 110)
    bottom_right = pygame.Rect(padding + 120, HEIGHT - 140, WIDTH - (padding * 2 + 120), 110)

    pygame.draw.rect(screen, (40, 40, 50), left_panel, 0)
    pygame.draw.rect(screen, (30, 30, 40), right_panel, 0)
    pygame.draw.rect(screen, (20, 20, 30), bottom_left, 0)
    pygame.draw.rect(screen, (25, 25, 35), bottom_right, 0)

    y_offset = left_panel.top + 10
    for line in challenge_prompt:
        rendered = font.render(line, True, (230, 230, 230))
        screen.blit(rendered, (left_panel.left + 10, y_offset))
        y_offset += 28

    line_height = 25
    for i, line in enumerate(code_lines):
        line_number = font.render(f"{i+1}", True, (100, 100, 100))
        screen.blit(line_number, (right_panel.left + 10, right_panel.top + 10 + i * line_height))
        code_text = font.render(line, True, (0, 255, 0))
        screen.blit(code_text, (right_panel.left + 40, right_panel.top + 10 + i * line_height))

    if cursor_visible:
        if 0 <= cursor_line < len(code_lines):
            current_text = code_lines[cursor_line][:cursor_col]
            cursor_x = right_panel.left + 40 + font.size(current_text)[0]
            cursor_y = right_panel.top + 10 + cursor_line * line_height
            pygame.draw.line(screen, (0, 255, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 20), 2)

    pygame.draw.circle(screen, (200, 180, 120), (85, HEIGHT - 85), 45)
    pygame.draw.circle(screen, BLACK, (70, HEIGHT - 95), 5)
    pygame.draw.circle(screen, BLACK, (100, HEIGHT - 95), 5)
    pygame.draw.arc(screen, BLACK, (65, HEIGHT - 70, 40, 20), 3.14, 0, 2)

    screen.blit(font.render("Can you solve this, traveler?", True, WHITE), (bottom_right.left + 10, bottom_right.top + 10))
    screen.blit(font.render(f"Result: {output_message}", True, (180, 180, 180)), (bottom_right.left + 10, bottom_right.top + 40))

    # Run Code Button
    mouse_pos = pygame.mouse.get_pos()
    is_hover = run_button_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_hover else BUTTON_COLOR, run_button_rect)
    pygame.draw.rect(screen, WHITE, run_button_rect, 2)
    screen.blit(font.render("Run Code", True, WHITE), (run_button_rect.x + 20, run_button_rect.y + 10))

    if challenge_solved:
        msg = large_font.render("✨ Well done, hero! You have solved the riddle. ✨", True, GREEN)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 240))


# Main game loop
running = True
while running:
    dt = clock.tick(60)
    cursor_timer += dt
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
        if keys[pygame.K_w]: player.y -= player_speed
        if keys[pygame.K_s]: player.y += player_speed
        if keys[pygame.K_a]: player.x -= player_speed
        if keys[pygame.K_d]: player.x += player_speed
        if player.colliderect(npc):
            scene = "dialogue"
            dialogue_index = 0
        draw_map_scene()
    elif scene == "dialogue":
        draw_dialogue_scene()
    elif scene == "code_challenge":
        draw_code_challenge()

    pygame.display.flip()

pygame.quit()
sys.exit()
