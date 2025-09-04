import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# 设置字体
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1, 1], [0, 0, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# 方块颜色
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 时钟控制游戏速度
clock = pygame.time.Clock()

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def rotate(self):
        # 转置矩阵实现旋转
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        self.shape = rotated

class Tetris:
    def __init__(self):
        self.board = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 1.0  # 每秒下落的方块数
        self.last_fall_time = pygame.time.get_ticks()

    def new_piece(self):
        # 在屏幕顶部中央生成新方块
        return Tetromino(GRID_WIDTH // 2 - 1, 0)

    def valid_position(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x
                    new_y = piece.y + y
                    if (new_x < 0 or new_x >= GRID_WIDTH or
                        new_y >= GRID_HEIGHT or self.board[new_y][new_x] != BLACK):
                        return False
        return True

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_position(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(cell != BLACK for cell in self.board[y]):
                # 清除整行
                del self.board[y]
                # 在顶部添加新行
                self.board.insert(0, [BLACK for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        # 根据消除的行数增加分数
        self.score += lines_cleared * 100 * self.level
        # 每消除10行升级
        self.level = self.score // 1000 + 1
        # 调整下落速度
        self.fall_speed = 1.0 + (self.level - 1) * 0.2

    def update(self):
        current_time = pygame.time.get_ticks()
        # 控制方块下落速度
        if current_time - self.last_fall_time > 1000 / self.fall_speed:
            self.current_piece.y += 1
            if not self.valid_position(self.current_piece):
                self.current_piece.y -= 1
                self.merge_piece()
                self.clear_lines()
            self.last_fall_time = current_time

    def draw_board(self):
        # 绘制游戏区域边框
        pygame.draw.rect(screen, WHITE, (0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 2)
        # 绘制网格
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, self.board[y][x], rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((piece.x + x + offset_x) * GRID_SIZE, 
                                      (piece.y + y + offset_y) * GRID_SIZE, 
                                      GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, piece.color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_info(self):
        # 绘制分数
        score_text = font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * GRID_SIZE + 20, 50))
        # 绘制等级
        level_text = font.render(f"等级: {self.level}", True, WHITE)
        screen.blit(level_text, (GRID_WIDTH * GRID_SIZE + 20, 100))
        # 绘制下一个方块
        next_text = font.render("下一个:", True, WHITE)
        screen.blit(next_text, (GRID_WIDTH * GRID_SIZE + 20, 150))
        self.draw_piece(self.next_piece, offset_x=GRID_WIDTH // 2 - 1, offset_y=6)
        # 如果游戏结束，显示游戏结束文字
        if self.game_over:
            game_over_text = font.render("游戏结束!按R键重新开始", True, RED)
            screen.blit(game_over_text, (GRID_WIDTH * GRID_SIZE // 2 - 150, GRID_HEIGHT * GRID_SIZE // 2))

    def draw(self):
        screen.fill(BLACK)
        self.draw_board()
        self.draw_piece(self.current_piece)
        self.draw_info()
        pygame.display.flip()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.x -= 1
                    if not self.valid_position(self.current_piece):
                        self.current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    self.current_piece.x += 1
                    if not self.valid_position(self.current_piece):
                        self.current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    self.current_piece.y += 1
                    if not self.valid_position(self.current_piece):
                        self.current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()
                    if not self.valid_position(self.current_piece):
                        # 如果旋转后位置无效，旋转回来
                        for _ in range(3):
                            self.current_piece.rotate()
                elif event.key == pygame.K_SPACE:
                    # 空格直接下落到底部
                    while self.valid_position(self.current_piece):
                        self.current_piece.y += 1
                    self.current_piece.y -= 1
                    self.merge_piece()
                    self.clear_lines()
                elif event.key == pygame.K_r and self.game_over:
                    # 重新开始游戏
                    self.__init__()

def main():
    game = Tetris()
    while True:
        game.handle_keys()
        if not game.game_over:
            game.update()           
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()