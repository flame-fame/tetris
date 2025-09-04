import pygame
import random

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH_NUM = 10
GRID_HEIGHT_NUM = 20

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# 游戏时钟
clock = pygame.time.Clock()

# 游戏区域左上角的坐标
GAME_AREA_X = (SCREEN_WIDTH - GRID_WIDTH_NUM * GRID_SIZE) // 2
GAME_AREA_Y = (SCREEN_HEIGHT - GRID_HEIGHT_NUM * GRID_SIZE) // 2



# 创建游戏网格
def create_grid(locked_positions={}):
    # 初始化网格为全黑
    grid = [[(0, 0, 0) for _ in range(GRID_WIDTH_NUM)] for _ in range(GRID_HEIGHT_NUM)]
    
    # 填充已锁定的方块位置
    for y in range(GRID_HEIGHT_NUM):
        for x in range(GRID_WIDTH_NUM):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# 绘制游戏网格
def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT_NUM):
        for x in range(GRID_WIDTH_NUM):
            # 绘制每个网格单元
            pygame.draw.rect(surface, grid[y][x], 
                            (GAME_AREA_X + x * GRID_SIZE, 
                             GAME_AREA_Y + y * GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE), 
                            0)
            
            # 绘制网格线
            pygame.draw.rect(surface, (50, 50, 50), 
                            (GAME_AREA_X + x * GRID_SIZE, 
                             GAME_AREA_Y + y * GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE), 
                            1)


# 游戏循环标志
running = True

# 主游戏循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 清空屏幕
    screen.fill(BLACK)
    
    # 绘制游戏区域边框
    pygame.draw.rect(screen, WHITE, 
                    (GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                     GRID_WIDTH_NUM * GRID_SIZE + 4, GRID_HEIGHT_NUM * GRID_SIZE + 4), 
                    2)
    # 网格绘制   
    #locked_positions是一个字典，用于存储已锁定的方块位置
    #每个键是一个元组(x, y)，表示方块的位置
    #每个值是一个颜色元组(r, g, b)，表示方块的颜色
    locked_positions = {}  # 初始为空
    grid = create_grid(locked_positions)
    draw_grid(screen, grid)
    
    # 更新屏幕
    pygame.display.flip()
    
    # 控制游戏帧率
    clock.tick(60)

# 退出游戏
pygame.quit()