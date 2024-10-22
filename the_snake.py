from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский class."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализатор родительского класса"""
        self.position = CENTER_POSITION
        self.body_color = None

    def draw(self):
        """Отрисовка объектов"""
        # Отрисовка объектов - изначально pass.
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        super().__init__(position=self.randomize_position(),
                         body_color=APPLE_COLOR)
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Определение позиции яблока на экране"""
        new_position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                        randint(0, GRID_HEIGHT) * GRID_SIZE)
        return new_position

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self):
        super().__init__(CENTER_POSITION, SNAKE_COLOR)
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [CENTER_POSITION]

    def update_direction(self):
        """Изменение направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змеи"""
        head_dx, head_dy = self.get_head_position()
        head = ((head_dx + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                (head_dy + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка змеи"""
        for self.position in self.positions[0:]:
            rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
            # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Позиция головы змеи"""
        return self.positions[0]

    def reset(self):
        """Сброс змеи в начальное положение"""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Управление движением змеи"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описание основной логики игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.position = apple.randomize_position()
        elif snake.get_head_position() == apple.position:
            snake.length = snake.length + 1
            apple.position = apple.randomize_position()
        elif apple.position in snake.positions[0:]:
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
