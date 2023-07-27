import random
import sys
from typing import List, Tuple, Dict, Union

import pygame


class Settings:
    """Settings"""
    SCREEN_WIDTH: int = 390
    SCREEN_HEIGHT: int = 600
    GRID_SIZE: int = 30
    GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    FPS: int = 60
    MOVE_DELAY: int = 50
    ROTATE_DELAY: int = 150
    BLOCK_COLORS: List[Tuple[int, int, int]] = [(253, 200, 0), (1, 158, 77), (249, 124, 30), (126, 192, 235)]
    SHAPES: List[List[List[int]]] = [
        [[1, 1, 1, 1]],  # I-shape
        [[1, 1, 1], [0, 1, 0]],  # T-shape
        [[1, 1, 1], [1, 0, 0]],  # L-shape
        [[1, 1, 1], [0, 0, 1]],  # J-shape
        [[1, 1], [1, 1]],  # O-shape
        [[1, 1], [1, 0], [1, 0]],  # S-shape
        [[1, 1], [0, 1], [0, 1]]  # Z-shape
    ]


class Block(Settings):
    """Game Block Class"""
    def __init__(self, shape: List[List[int]], color: Tuple[int, int, int]):
        self.shape: List[List[int]] = shape
        self.color: Tuple[int, int, int] = color
        self.x: int = self.GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y: int = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def draw(self, surface: pygame.Surface, grid_size: int):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[0])):
                if self.shape[row][col]:
                    rect = pygame.Rect((self.x + col) * grid_size, (self.y + row) * grid_size, grid_size, grid_size)
                    pygame.draw.rect(surface, self.color, rect)


class TetrisRenderer:
    """TetrisRenderer class to handle rendering"""
    def __init__(self, game: 'Tetris'):
        self.game = game

    def draw_grid(self):
        for row in range(self.game.GRID_HEIGHT):
            for col in range(self.game.GRID_WIDTH):
                cell_color = self.game.grid[row][col]
                if cell_color:
                    pygame.draw.rect(self.game.screen, cell_color,
                                     pygame.Rect(col * self.game.GRID_SIZE, row * self.game.GRID_SIZE,
                                                 self.game.GRID_SIZE, self.game.GRID_SIZE))
                else:
                    pygame.draw.rect(self.game.screen, (29, 30, 33),
                                     pygame.Rect(col * self.game.GRID_SIZE, row * self.game.GRID_SIZE,
                                                 self.game.GRID_SIZE, self.game.GRID_SIZE), 1)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.game.score}', True, self.game.WHITE)
        level_text = font.render(f'Level: {self.game.level}', True, self.game.WHITE)
        self.game.screen.blit(score_text, (20, 20))
        self.game.screen.blit(level_text, (20, 60))

    def render(self):
        self.game.screen.fill(self.game.BLACK)
        self.draw_grid()
        self.game.current_block.draw(self.game.screen, self.game.GRID_SIZE)
        self.draw_score()
        pygame.display.update()


class Tetris(Settings):
    """Game Class"""
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.renderer: TetrisRenderer = TetrisRenderer(self)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.grid: List[List[Union[Tuple[int, int, int], int]]] = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_block: Block = self.create_new_block()
        self.score: int = 0
        self.level: int = 1
        self.fall_time: int = 1000
        self.last_fall_time: int = pygame.time.get_ticks()
        self.game_over: bool = False
        self.keys_held: Dict[int, bool] = {}
        self.move_timer: int = 0
        self.rotate_timer: int = 0

    def create_new_block(self) -> Block:
        shape = random.choice(self.SHAPES)
        color = random.choice(self.BLOCK_COLORS)
        return Block(shape, color)

    def check_collision(self, block: Block) -> bool:
        for row in range(len(block.shape)):
            for col in range(len(block.shape[0])):
                if block.shape[row][col]:
                    x, y = block.x + col, block.y + row
                    if not 0 <= x < self.GRID_WIDTH or not 0 <= y < self.GRID_HEIGHT or self.grid[y][x]:
                        return True
        return False

    def update_grid(self, block: Block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[0])):
                if block.shape[row][col]:
                    self.grid[block.y + row][block.x + col] = block.color

    def remove_line(self, row: int) -> List[Union[Tuple[int, int, int], int]]:
        del self.grid[row]
        return [0 for _ in range(self.GRID_WIDTH)]

    def check_for_lines(self):
        lines_to_remove = []
        for row in range(self.GRID_HEIGHT):
            if all(self.grid[row]):
                lines_to_remove.append(row)

        for row in lines_to_remove:
            self.grid.insert(0, self.remove_line(row))
            self.score += 10 * self.level

    def update_level(self):
        self.level = 1 + self.score // 100
        self.fall_time = 1000 // self.level

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                self.keys_held[event.key] = True
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                                pause = False
            elif event.type == pygame.KEYUP:
                self.keys_held[event.key] = False

    def run(self):
        while not self.game_over:
            self.clock.tick(self.FPS)
            self.handle_events()

            current_time = pygame.time.get_ticks()

            # Handling block movement with timers
            if self.keys_held.get(pygame.K_DOWN, False):
                self.current_block.move(0, 1)
                if self.check_collision(self.current_block):
                    self.current_block.move(0, -1)
                self.move_timer = current_time

            if self.keys_held.get(pygame.K_LEFT, False):
                if current_time - self.move_timer > self.MOVE_DELAY:
                    self.current_block.move(-1, 0)
                    if self.check_collision(self.current_block):
                        self.current_block.move(1, 0)
                    self.move_timer = current_time

            if self.keys_held.get(pygame.K_RIGHT, False):
                if current_time - self.move_timer > self.MOVE_DELAY:
                    self.current_block.move(1, 0)
                    if self.check_collision(self.current_block):
                        self.current_block.move(-1, 0)
                    self.move_timer = current_time

            # Handling block rotation with timers
            if self.keys_held.get(pygame.K_UP, False):
                if current_time - self.rotate_timer > self.ROTATE_DELAY:
                    self.current_block.rotate()
                    if self.check_collision(self.current_block):
                        self.current_block.rotate()
                        self.current_block.rotate()
                        self.current_block.rotate()
                    self.rotate_timer = current_time

            # Automatic block falling
            if current_time - self.last_fall_time > self.fall_time:
                self.current_block.move(0, 1)
                if self.check_collision(self.current_block):
                    self.current_block.move(0, -1)
                    self.update_grid(self.current_block)
                    self.check_for_lines()
                    self.current_block = self.create_new_block()
                    if self.check_collision(self.current_block):
                        self.game_over = True
                self.last_fall_time = current_time

            self.update_level()
            self.renderer.render()
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()
