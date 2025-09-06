import pygame
import random

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

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

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 游戏时钟
clock = pygame.time.Clock()

# 游戏区域左上角的坐标
GAME_AREA_X = (SCREEN_WIDTH - SIDEBAR_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
GAME_AREA_Y = (SCREEN_HEIGHT - GRID_HEIGHT * GRID_SIZE) // 2

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

# 创建游戏网格
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# 绘制游戏网格
def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
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

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

# 获取随机方块
def get_random_piece():
    shape = random.choice(SHAPES)
    # 调整初始位置，确保方块居中
    x = GRID_WIDTH // 2 - len(shape[0]) // 2
    return Piece(x, 0, shape)

# 绘制当前方块
def draw_piece(surface, piece):
    shape_format = piece.shape
    for i, row in enumerate(shape_format):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, 
                                (GAME_AREA_X + (piece.x + j) * GRID_SIZE, 
                                 GAME_AREA_Y + (piece.y + i) * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                0)
                pygame.draw.rect(surface, (50, 50, 50), 
                                (GAME_AREA_X + (piece.x + j) * GRID_SIZE, 
                                 GAME_AREA_Y + (piece.y + i) * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                1)

def convert_piece_format(piece):
    positions = []
    shape_format = piece.shape
    
    for i, row in enumerate(shape_format):
        for j, cell in enumerate(row):
            if cell:
                positions.append((piece.x + j, piece.y + i))
    
    return positions

def valid_space(piece, grid):
    accepted_pos = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == BLACK:
                accepted_pos.append((x, y))
    
    formatted = convert_piece_format(piece)
    
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] >= 0:  # 只检查游戏区域内的位置
                return False
    return True

def rotate_piece(piece):
    # 旋转方块（顺时针90度）
    rows = len(piece.shape)
    cols = len(piece.shape[0])
    
    # 创建旋转后的形状
    rotated = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for r in range(rows):
        for c in range(cols):
            rotated[c][rows - 1 - r] = piece.shape[r][c]
    
    new_piece = Piece(piece.x, piece.y, rotated)
    return new_piece

def clear_rows(grid, locked):
    inc = 0
    # 从底部向上检查每一行
    for i in range(GRID_HEIGHT - 1, -1, -1):
        if all(cell != BLACK for cell in grid[i]):
            inc += 1
            # 移除该行
            for j in range(GRID_WIDTH):
                if (j, i) in locked:
                    del locked[(j, i)]
    
    if inc > 0:
        # 重新组织锁定位置
        new_locked = {}
        for y in range(GRID_HEIGHT - 1, -1, -1):
            for x in range(GRID_WIDTH):
                if (x, y) in locked:
                    new_y = y + inc
                    # 只保留在网格内的方块
                    while new_y < GRID_HEIGHT and (x, new_y) not in new_locked:
                        new_locked[(x, new_y)] = locked[(x, y)]
                        break
        locked.clear()
        locked.update(new_locked)
    
    return inc

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 0:
            return True
    return False

def draw_next_piece(surface, piece):
    # 绘制下一个方块预览
    font = pygame.font.SysFont('comicsans', 20)
    label = font.render("下一个方块:", 1, WHITE)
    
    sx = GAME_AREA_X + GRID_WIDTH * GRID_SIZE + 20
    sy = GAME_AREA_Y
    
    surface.blit(label, (sx, sy + 20))
    
    shape_format = piece.shape
    for i, row in enumerate(shape_format):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, piece.color, 
                                (sx + j * GRID_SIZE, 
                                 sy + 50 + i * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                0)
                pygame.draw.rect(surface, (50, 50, 50), 
                                (sx + j * GRID_SIZE, 
                                 sy + 50 + i * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                1)

def draw_score(surface, score, level):
    # 绘制分数和等级
    sx = GAME_AREA_X + GRID_WIDTH * GRID_SIZE + 20
    sy = GAME_AREA_Y + 150
    
    font = pygame.font.SysFont('comicsans', 20)
    
    score_label = font.render(f"分数: {score}", 1, WHITE)
    level_label = font.render(f"等级: {level}", 1, WHITE)
    
    surface.blit(score_label, (sx, sy))
    surface.blit(level_label, (sx, sy + 30))

def draw_shadow(surface, piece, grid):
    shadow_piece = Piece(piece.x, piece.y, piece.shape)
    shadow_piece.color = (50, 50, 50)  # 灰色阴影
    
    # 将阴影降到底部
    while valid_space(shadow_piece, grid):
        shadow_piece.y += 1
    shadow_piece.y -= 1
    
    # 绘制阴影
    shape_format = shadow_piece.shape
    for i, row in enumerate(shape_format):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, shadow_piece.color, 
                                (GAME_AREA_X + (shadow_piece.x + j) * GRID_SIZE, 
                                 GAME_AREA_Y + (shadow_piece.y + i) * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                0)
                pygame.draw.rect(surface, (50, 50, 50), 
                                (GAME_AREA_X + (shadow_piece.x + j) * GRID_SIZE, 
                                 GAME_AREA_Y + (shadow_piece.y + i) * GRID_SIZE, 
                                 GRID_SIZE, GRID_SIZE), 
                                1)

# 初始化游戏状态
locked_positions = {}
grid = create_grid(locked_positions)
current_piece = get_random_piece()
next_piece = get_random_piece()
score = 0
level = 1
lines_cleared = 0
game_over = False
paused = False

# 游戏循环标志
running = True
fall_time = 0
fall_speed = 0.5  # 方块下落的速度（秒）
last_fall_time = pygame.time.get_ticks()

# 主游戏循环
while running:
    # 计算下落时间
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_fall_time) / 1000.0
    last_fall_time = current_time
    
    if not game_over and not paused:
        fall_time += delta_time
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and game_over:
                # 重新开始游戏
                locked_positions = {}
                grid = create_grid(locked_positions)
                current_piece = get_random_piece()
                next_piece = get_random_piece()
                score = 0
                level = 1
                lines_cleared = 0
                game_over = False
            elif event.key == pygame.K_p:
                paused = not paused
            
            if not game_over and not paused:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(current_piece)
                    if valid_space(rotated_piece, grid):
                        current_piece = rotated_piece
                elif event.key == pygame.K_SPACE:
                    # 硬降落 - 立即将方块降到底部
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
    
    if not game_over and not paused:
        # 方块自动下落
        if fall_time >= fall_speed / level:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                # 锁定当前方块
                for pos in convert_piece_format(current_piece):
                    if pos[1] >= 0:  # 只保存网格内的位置
                        locked_positions[pos] = current_piece.color
                
                # 更新网格
                grid = create_grid(locked_positions)
                
                # 消除完整的行
                rows_cleared = clear_rows(grid, locked_positions)
                if rows_cleared > 0:
                    score += (rows_cleared ** 2) * 100 * level
                    lines_cleared += rows_cleared
                    level = lines_cleared // 10 + 1
                
                # 生成新方块
                current_piece = next_piece
                next_piece = get_random_piece()
                
                # 更新网格
                grid = create_grid(locked_positions)
                
                # 检查游戏是否结束
                if not valid_space(current_piece, grid):
                    game_over = True
    
    # 清空屏幕
    screen.fill(BLACK)
    
    # 绘制游戏区域边框
    pygame.draw.rect(screen, WHITE, 
                    (GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                     GRID_WIDTH * GRID_SIZE + 4, GRID_HEIGHT * GRID_SIZE + 4), 
                    2)
    
    # 绘制侧边栏区域
    sidebar_x = GAME_AREA_X + GRID_WIDTH * GRID_SIZE + 20
    pygame.draw.rect(screen, GRAY, 
                    (sidebar_x, GAME_AREA_Y, 
                     SIDEBAR_WIDTH, GRID_HEIGHT * GRID_SIZE), 
                    2)
    
    # 绘制网格
    draw_grid(screen, grid)
    
    # 绘制当前方块和阴影
    if not game_over:
        draw_shadow(screen, current_piece, grid)
        draw_piece(screen, current_piece)
    
    # 绘制下一个方块、分数和等级
    draw_next_piece(screen, next_piece)
    draw_score(screen, score, level)
    
    # 如果游戏暂停，显示暂停信息
    if paused:
        font = pygame.font.SysFont('comicsans', 40)
        label = font.render("游戏暂停", 1, YELLOW)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    # 如果游戏结束，显示游戏结束信息
    if game_over:
        font = pygame.font.SysFont('comicsans', 40)
        label = font.render("游戏结束!", 1, RED)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        font = pygame.font.SysFont('comicsans', 20)
        label = font.render("按R键重新开始", 1, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    # 更新屏幕
    pygame.display.flip()
    
    # 控制游戏帧率
    clock.tick(60)

# 退出游戏
pygame.quit()