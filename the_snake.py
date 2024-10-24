from random import randint

import pygame as pg

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

# Константы для цветов
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский class."""

    def __init__(self, position=CENTER_POSITION,
                 body_color=SNAKE_COLOR):
        """Инициализатор родительского класса."""
        self.position = position
        self.body_color = body_color
        self.border_color = BORDER_COLOR
        self.last = None
        self.color = self.body_color

    def draw(self):
        """Отрисовка объектов."""

    def draw_single_cell(self, position):
        """Отрисовка клетки."""
        cell = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.color, cell)
        pg.draw.rect(screen, self.border_color, cell, 1)

    def delete_cell(self, position):
        """Закрашивание клетки."""
        cell_del = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, cell_del)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        if occupied_positions is None:
            occupied_positions = []
        super().__init__(position=self.randomize_position(occupied_positions),
                         body_color=APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """Определение позиции яблока на экране."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in occupied_positions:
                break
        return new_position

    def draw(self):
        """Отрисовка яблока."""
        self.draw_single_cell(self.position)


class Snake(GameObject):
    """Класс змеи."""

    def __init__(self, position=CENTER_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()

    def update_direction(self, new_direction=None):
        """Изменение направления."""
        self.direction = new_direction

    def move(self):
        """Движение змеи."""
        head_dx, head_dy = self.get_head_position()
        dir_x, dir_y = self.direction
        head = ((head_dx + (dir_x * GRID_SIZE)) % SCREEN_WIDTH,
                (head_dy + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT)

        self.positions.insert(0, head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змеи."""
        self.draw_single_cell(self.get_head_position())
        if self.last:
            self.delete_cell(self.last)

    def get_head_position(self):
        """Позиция головы змеи"""
        return self.positions[0]

    def reset(self):
        """Сброс змеи в начальное положение."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Управление движением змеи."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            if event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            if event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            if event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Описание основной логики игры."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)
        elif snake.get_head_position() == apple.position:
            snake.length = snake.length + 1
            apple.position = apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
