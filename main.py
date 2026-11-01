import pygame
import random
import sys

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Цвета
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0) # Яркий цвет для еды
LIGHT_BLUE = (100, 200, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Змейка: Полная версия")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont("Arial", 60, bold=True)
font_medium = pygame.font.SysFont("Arial", 35, bold=True)
font_small = pygame.font.SysFont("Arial", 25)
font_emoji = pygame.font.SysFont("Segoe UI Emoji", 40)

# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ НАСТРОЕК ---
current_state = "MENU"
difficulty = "Средняя"
snake_color = GREEN
snake_color_name = "Зеленый"
wall_chance = 30

COLOR_OPTIONS = [
    ("Зеленый", (0, 255, 0)),
    ("Синий", (50, 150, 255)),
    ("Желтый", (255, 255, 0)),
    ("Розовый", (255, 105, 180)),
    ("Красный", (255, 50, 50))
]
color_index = 0

DIFFICULTY_SETTINGS = {
    "Легкая": {"speed": 6, "wall_chance": 0, "locked": True},
    "Средняя": {"speed": 8, "wall_chance": 30, "locked": False},
    "Хардкор": {"speed": 12, "wall_chance": 70, "locked": True}
}

# --- ФУНКЦИИ ИГРЫ ---
def spawn_food(snake, walls):
    while True:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        # Еда не должна быть в змейке, и не должна пересекаться со стенами
        if pos not in snake and pos not in walls:
            return pos

def generate_walls():
    walls = set()
    if wall_chance == 0: return walls
    num_walls = int((wall_chance / 100) * 15)
    for _ in range(num_walls):
        wall_type = random.choice([0, 1])
        if random.random() < (wall_chance / 100) * 0.3:
            length = COLS if wall_type == 0 else ROWS
        else:
            length = random.randint(3, 10)
        if wall_type == 0:
            start_x = random.randint(0, max(0, COLS - length))
            start_y = random.randint(0, ROWS - 1)
            for i in range(length): walls.add((start_x + i, start_y))
        else:
            start_x = random.randint(0, COLS - 1)
            start_y = random.randint(0, max(0, ROWS - length))
            for i in range(length): walls.add((start_x, start_y + i))
    safe_zone = set()
    for x in range(COLS//2 - 2, COLS//2 + 3):
        for y in range(ROWS//2 - 2, ROWS//2 + 3):
            safe_zone.add((x, y))
    return walls - safe_zone

snake = []
direction = (1, 0)
new_direction = direction
walls = set()
food = (0,0)
score = 0
game_over = False
is_paused = False
current_speed = 8

def reset_game():
    global snake, direction, new_direction, walls, food, score, game_over, is_paused, current_speed
    snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2)]
    direction = (1, 0)
    new_direction = direction
    walls = generate_walls()
    # Даем генератору еды актуальные координаты змейки и стен
    food = spawn_food(snake, walls)
    score = 0
    game_over = False
    is_paused = False
    current_speed = DIFFICULTY_SETTINGS[difficulty]["speed"]

# --- ФУНКЦИЯ ОТРИСОВКИ КНОПОК ---
def draw_button(text, x, y, w, h, color, text_color=WHITE, is_transparent=False, is_home=False):
    if is_transparent:
        pygame.draw.rect(screen, GRAY, (x, y, w, h), 2, border_radius=10)
        surf = font_small.render(text, True, GRAY)
    else:
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2, border_radius=10)
        if is_home:
            surf = font_emoji.render("🏠", True, text_color)
        else:
            surf = font_medium.render(text, True, text_color)
    
    screen.blit(surf, (x + (w - surf.get_width())//2, y + (h - surf.get_height())//2))

# --- ГЛАВНЫЙ ЦИКЛ ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            if current_state == "MENU":
                if WIDTH//2 - 150 < mx < WIDTH//2 + 150:
                    if HEIGHT//2 - 100 < my < HEIGHT//2 - 40:
                        current_state = "GAME"
                        reset_game()
                    elif HEIGHT//2 - 10 < my < HEIGHT//2 + 50:
                        current_state = "SETTINGS"
                    elif HEIGHT//2 + 80 < my < HEIGHT//2 + 140:
                        current_state = "DIFFICULTY"
            
            elif current_state == "DIFFICULTY":
                if 20 < mx < 80 and 20 < my < 80:
                    current_state = "MENU"
                elif WIDTH//2 - 200 < mx < WIDTH//2 + 200:
                    if 200 < my < 260: difficulty = "Легкая"
                    elif 300 < my < 360: difficulty = "Средняя"
                    elif 400 < my < 460: difficulty = "Хардкор"
            
            elif current_state == "SETTINGS":
                if 20 < mx < 80 and 20 < my < 80:
                    current_state = "MENU"
                elif WIDTH//2 - 200 < mx < WIDTH//2 + 200:
                    if 200 < my < 260:
                        color_index = (color_index + 1) % len(COLOR_OPTIONS)
                        snake_color_name, snake_color = COLOR_OPTIONS[color_index]
                    elif 380 < my < 440 and not DIFFICULTY_SETTINGS[difficulty]["locked"]:
                        if WIDTH//2 - 150 < mx < WIDTH//2 - 90:
                            wall_chance = max(0, wall_chance - 10)
                        elif WIDTH//2 + 90 < mx < WIDTH//2 + 150:
                            wall_chance = min(100, wall_chance + 10)
            
            elif current_state == "GAME":
                if not game_over and not is_paused:
                    if WIDTH - 90 < mx < WIDTH - 20 and 20 < my < 80:
                        is_paused = True
                elif is_paused:
                    if WIDTH//2 - 150 < mx < WIDTH//2 + 150:
                        if HEIGHT//2 - 100 < my < HEIGHT//2 - 40: is_paused = False
                        elif HEIGHT//2 - 20 < my < HEIGHT//2 + 40: reset_game()
                        elif HEIGHT//2 + 60 < my < HEIGHT//2 + 120:
                            current_state = "MENU"
                            is_paused = False
                elif game_over:
                    if WIDTH//2 - 150 < mx < WIDTH//2 + 150:
                        if HEIGHT//2 + 80 < my < HEIGHT//2 + 140:
                            current_state = "MENU"
                            game_over = False
                        elif HEIGHT//2 < my < HEIGHT//2 + 60:
                            reset_game()

        if current_state == "GAME" and not game_over and not is_paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_start_x, touch_start_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                dx = event.pos[0] - touch_start_x
                dy = event.pos[1] - touch_start_y
                if abs(dx) > 50 or abs(dy) > 50:
                    if abs(dx) > abs(dy):
                        if dx > 0 and direction != (-1, 0): new_direction = (1, 0)
                        elif dx < 0 and direction != (1, 0): new_direction = (-1, 0)
                    else:
                        if dy > 0 and direction != (0, -1): new_direction = (0, 1)
                        elif dy < 0 and direction != (0, 1): new_direction = (0, -1)

    if current_state == "GAME" and not game_over and not is_paused:
        direction = new_direction
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        new_head = (new_head[0] % COLS, new_head[1] % ROWS)

        if new_head in snake or new_head in walls:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 1
                # После того как съели яблоко - генерируем новое (проверяя стены!)
                food = spawn_food(snake, walls)
                if current_speed < 20: current_speed += 0.3
            else:
                snake.pop()

    screen.fill(BLACK)
    
    if current_state == "MENU":
        title = font_large.render("ЗМЕЙКА", True, snake_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        draw_button("ИГРАТЬ", WIDTH//2 - 150, HEIGHT//2 - 100, 300, 60, DARK_GREEN)
        draw_button("НАСТРОЙКИ", WIDTH//2 - 150, HEIGHT//2 - 10, 300, 60, BLUE)
        draw_button(f"СЛОЖНОСТЬ: {difficulty}", WIDTH//2 - 150, HEIGHT//2 + 80, 300, 60, DARK_GRAY)

    elif current_state == "SETTINGS":
        draw_button("", 20, 20, 60, 60, DARK_GRAY, is_home=True)
        title = font_large.render("НАСТРОЙКИ", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        draw_button(f"ЦВЕТ: {snake_color_name}", WIDTH//2 - 200, 200, 400, 60, DARK_GRAY)
        pygame.draw.rect(screen, snake_color, (WIDTH//2 - 40, 280, 80, 30), border_radius=5)
        
        is_locked = DIFFICULTY_SETTINGS[difficulty]["locked"]
        if is_locked:
            draw_button("ШАНС СТЕН: ЗАБЛОКИРОВАНО", WIDTH//2 - 200, 380, 400, 60, None, is_transparent=True)
        else:
            draw_button("-", WIDTH//2 - 150, 380, 60, 60, RED)
            draw_button("+", WIDTH//2 + 90, 380, 60, 60, DARK_GREEN)
            chance_text = font_medium.render(f"{wall_chance}%", True, WHITE)
            screen.blit(chance_text, (WIDTH//2 - chance_text.get_width()//2, 395))
            sub_text = font_small.render("ШАНС ПОЯВЛЕНИЯ СТЕН:", True, GRAY)
            screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, 340))

    elif current_state == "DIFFICULTY":
        draw_button("", 20, 20, 60, 60, DARK_GRAY, is_home=True)
        title = font_large.render("СЛОЖНОСТЬ", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        color_l = GREEN if difficulty == "Легкая" else DARK_GRAY
        color_m = GREEN if difficulty == "Средняя" else DARK_GRAY
        color_h = GREEN if difficulty == "Хардкор" else DARK_GRAY
        
        draw_button("ЛЕГКАЯ (без стен)", WIDTH//2 - 200, 200, 400, 60, color_l)
        draw_button("СРЕДНЯЯ", WIDTH//2 - 200, 300, 400, 60, color_m)
        draw_button("ХАРДКОР (70% стен)", WIDTH//2 - 200, 400, 400, 60, color_h)

    elif current_state == "GAME":
        for wall in walls:
            pygame.draw.rect(screen, GRAY, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Рисуем еду (теперь она ЯРКО-ЖЕЛТАЯ)
        pygame.draw.rect(screen, YELLOW, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE + 5, food[1]*CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10), border_radius=5) # Внутренний красный кружок
        
        for i, segment in enumerate(snake):
            color = snake_color if i == 0 else (snake_color[0]//2, snake_color[1]//2, snake_color[2]//2)
            pygame.draw.rect(screen, color, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        score_text = font_medium.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        if not game_over and not is_paused:
            pygame.draw.rect(screen, DARK_GRAY, (WIDTH - 80, 20, 60, 60), border_radius=10)
            pygame.draw.rect(screen, WHITE, (WIDTH - 65, 35, 10, 30))
            pygame.draw.rect(screen, WHITE, (WIDTH - 45, 35, 10, 30))

        if is_paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            title = font_large.render("ПАУЗА", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 200))
            draw_button("ПРОДОЛЖИТЬ", WIDTH//2 - 150, HEIGHT//2 - 100, 300, 60, DARK_GREEN)
            draw_button("ЗАНОВО", WIDTH//2 - 150, HEIGHT//2 - 20, 300, 60, YELLOW)
            draw_button("В ГЛАВНОЕ МЕНЮ", WIDTH//2 - 150, HEIGHT//2 + 60, 300, 60, RED)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            over_text = font_large.render("ИГРА ОКОНЧЕНА", True, RED)
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 150))
            draw_button("ЗАНОВО", WIDTH//2 - 150, HEIGHT//2, 300, 60, DARK_GREEN)
            draw_button("В МЕНЮ", WIDTH//2 - 150, HEIGHT//2 + 80, 300, 60, DARK_GRAY)

    pygame.display.flip()
    
    if current_state == "GAME":
        clock.tick(current_speed)
    else:
        clock.tick(60)

pygame.quit()
sys.exit()
