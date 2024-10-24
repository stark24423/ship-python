import pygame
import numpy as np
import heapq
import sys

# 可調整的參數

# 網格和顯示參數
GRID_SIZE = 100  # 網格尺寸
CELL_SIZE = 6    # 每個網格的像素大小
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # 窗口大小
FPS = 60  # 幀率

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 0)  # 路徑顏色
LIGHT_GRAY = (200, 200, 200)  # 圓周顏色

# 船隻初始位置和速度
FLEET_LEADER_START_X = 10
FLEET_LEADER_START_Y = 10
FLEET_LEADER_SPEED = 10

ENEMY_SHIP_START_X = 50
ENEMY_SHIP_START_Y = 50
ENEMY_SHIP_SPEED = 5

# 艦隊隊形偏移
FORMATION_OFFSETS = [
    (0, 0),         # 領隊
    (-2, -2),       # 左側第一艘船
    (-2, 2),        # 右側第一艘船
    (-4, -4),       # 左側第二艘船
    (-4, 4),        # 右側第二艘船
]

# 距離閾值
FORMATION_CHANGE_DISTANCE = 30  # 距離小於此值時改變隊形

# 包圍敵方船隻時的圓周半徑
SURROUND_RADIUS = 15  # 圓的半徑

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("船隻追擊模擬 - 個別路線顯示")
clock = pygame.time.Clock()

# 船隻類別定義
class Ship:
    def __init__(self, x, y, color, speed):
        self.x = x  # 位置可以是浮點數
        self.y = y
        self.color = color
        self.speed = speed  # 每秒移動的格子數
        self.path = []  # A* 路徑
        self.prev_x = x  # 上一幀的位置
        self.prev_y = y
        self.target_x = x  # 目標位置 X
        self.target_y = y  # 目標位置 Y

    def move_along_path(self, dt):
        # 沿著路徑移動
        if self.path:
            next_node = self.path[0]
            self.move_towards(next_node[0], next_node[1], dt)
            # 如果到達下一個節點，彈出
            if abs(self.x - next_node[0]) < 0.1 and abs(self.y - next_node[1]) < 0.1:
                self.path.pop(0)
        else:
            # 沒有路徑，停留在當前位置
            pass

    def move_towards(self, target_x, target_y, dt):
        # 保存上一幀的位置
        self.prev_x = self.x
        self.prev_y = self.y
        # 計算方向
        dir_x = target_x - self.x
        dir_y = target_y - self.y
        distance = np.hypot(dir_x, dir_y)
        if distance == 0:
            return
        # 方向單位化
        dir_x /= distance
        dir_y /= distance
        # 移動
        move_distance = self.speed * dt
        self.x += dir_x * move_distance
        self.y += dir_y * move_distance

    def move(self, dx, dy, dt):
        # 移動船隻，考慮邊界
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        if 0 <= new_x <= GRID_SIZE - 1:
            self.x = new_x
        if 0 <= new_y <= GRID_SIZE - 1:
            self.y = new_y

    def draw(self):
        # 繪製船隻
        rect = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)

    def draw_path(self):
        # 繪製路徑
        if len(self.path) > 1:
            points = [(x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2) for x, y in self.path]
            pygame.draw.lines(screen, YELLOW, False, points, 2)

# A* 演算法實現
def astar(start, goal, grid):
    def heuristic(a, b):
        # 使用歐幾里得距離作為啟發式函數
        return np.hypot(a[0] - b[0], a[1] - b[1])
        # 如果起點和終點相同，直接回傳起點

    if start == goal:
        return [start]

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # 重建路徑
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor, move_cost in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + move_cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def get_neighbors(pos, grid):
    neighbors = []
    x, y = pos
    # 八個方向
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),   # 上下左右
                  (-1, -1), (-1, 1), (1, -1), (1, 1)] # 對角線
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            # 計算移動成本，直行為1，對角線為sqrt(2)
            move_cost = np.hypot(dx, dy)
            neighbors.append(((nx, ny), move_cost))
    return neighbors

# 初始化船隻
# 創建艦隊領隊（中心船隻）
fleet_leader = Ship(FLEET_LEADER_START_X, FLEET_LEADER_START_Y, BLUE, FLEET_LEADER_SPEED)

# 定義艦隊的初始隊形（局部座標系下）
# 這裡定義一個 V 字形的固定隊形
formation_offsets = FORMATION_OFFSETS

# 創建艦隊
fleet = []
for offset in formation_offsets:
    ship = Ship(fleet_leader.x, fleet_leader.y, BLUE, FLEET_LEADER_SPEED)
    ship.local_offset = np.array(offset)  # 局部偏移，用於計算隊形位置
    fleet.append(ship)

# 敵方船隻
enemy_ship = Ship(ENEMY_SHIP_START_X, ENEMY_SHIP_START_Y, RED, ENEMY_SHIP_SPEED)  # 敵方船隻速度

# 主循環
running = True
formation_flag = True
create_surround_position_flag = False
while running:
    dt = clock.tick(FPS) / 1000.0  # 轉換為秒
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 獲取鍵盤輸入
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    # 按鍵方向歸一化，防止對角線速度過快
    if dx != 0 and dy != 0:
        dx *= np.sqrt(0.5)
        dy *= np.sqrt(0.5)

    # 控制敵方船隻移動
    enemy_ship.move(dx, dy, dt)

    # 計算領隊與敵方船隻的距離
    distance_to_enemy = np.hypot(fleet_leader.x - enemy_ship.x, fleet_leader.y - enemy_ship.y)
    if distance_to_enemy < FORMATION_CHANGE_DISTANCE:
        formation_flag = False

    if distance_to_enemy > FORMATION_CHANGE_DISTANCE and formation_flag is True:
        # 與之前相同的剛性隊形移動
        # 每隔一定時間重新計算路徑
        if not fleet_leader.path or (round(fleet_leader.path[-1][0]) != round(enemy_ship.x) or round(fleet_leader.path[-1][1]) != round(enemy_ship.y)):
            start = (round(fleet_leader.x), round(fleet_leader.y))
            goal = (round(enemy_ship.x), round(enemy_ship.y))
            grid = np.zeros((GRID_SIZE, GRID_SIZE))
            fleet_leader.path = astar(start, goal, grid)

        # 領隊船隻移動
        if fleet_leader.path:
            next_node = fleet_leader.path[1] if len(fleet_leader.path) > 1 else fleet_leader.path[0]
            fleet_leader.move_towards(next_node[0], next_node[1], dt)
            # 如果達到下一個節點，則彈出
            if abs(fleet_leader.x - next_node[0]) < 0.1 and abs(fleet_leader.y - next_node[1]) < 0.1:
                fleet_leader.path.pop(0)

        # 計算領隊的移動方向角度
        dir_x = fleet_leader.x - fleet_leader.prev_x
        dir_y = fleet_leader.y - fleet_leader.prev_y
        angle = np.arctan2(dir_y, dir_x)  # 領隊的朝向角度
        if dir_x == 0 and dir_y == 0:
            angle = 0  # 當領隊靜止時，保持之前的角度

        # 構造旋轉矩陣
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        rotation_matrix = np.array([[cos_a, -sin_a],
                                    [sin_a, cos_a]])

        # 更新艦隊中每艘船隻的位置
        for ship in fleet:
            # 計算在全局座標系下的位置
            if ship == fleet_leader:
                continue  # 領隊已經移動，無需更新
            local_position = ship.local_offset
            rotated_offset = rotation_matrix.dot(local_position)
            target_x = fleet_leader.x + rotated_offset[0]
            target_y = fleet_leader.y + rotated_offset[1]
            # 更新目標位置
            ship.target_x = target_x
            ship.target_y = target_y
            # 平滑移動到目標位置
            ship.move_towards(target_x, target_y, dt)
            # 清除個人路徑
            ship.path = []
    else:
        if create_surround_position_flag is False:
            # 靠近敵方船隻，改變隊形，為每艘船隻計算個別路徑
            num_ships = len(fleet)
            angle_between_ships = 2 * np.pi / num_ships
            radius = SURROUND_RADIUS  # 圓的半徑

            # 計算從領隊到敵方船隻的連線方向角度
            dir_x = enemy_ship.x - fleet_leader.x
            dir_y = enemy_ship.y - fleet_leader.y
            base_angle = np.arctan2(dir_y, dir_x)
            create_surround_position_flag = True

        for i, ship in enumerate(fleet):
            # 計算每艘船在圓周上的目標角度
            theta = base_angle + i * angle_between_ships
            # 計算目標位置
            target_x = enemy_ship.x + radius * np.cos(theta)
            target_y = enemy_ship.y + radius * np.sin(theta)
            # 更新目標位置
            ship.target_x = target_x
            ship.target_y = target_y
            #Todo 在這裡加入避碰 以及 task assignment
            # 如果需要重新計算路徑（第一次或目標位置改變）

            if not ship.path or (round(ship.path[-1][0]) != round(target_x) or round(ship.path[-1][1]) != round(target_y)):
                start = (round(ship.x), round(ship.y))
                goal = (round(target_x), round(target_y))
                if start == goal:
                    continue
                grid = np.zeros((GRID_SIZE, GRID_SIZE))
                ship.path = astar(start, goal, grid)

            # 沿著個人路徑移動
            ship.move_along_path(dt)

    # 繪製領隊的路徑（僅在距離大於 FORMATION_CHANGE_DISTANCE 時）
    if distance_to_enemy > FORMATION_CHANGE_DISTANCE and formation_flag is True:
        fleet_leader.draw_path()

    # 繪製艦隊中的所有船隻和他們的路徑
    for ship in fleet:
        ship.draw()
        # 繪製個人路徑（靠近敵方船隻時）
        if formation_flag is False:
            ship.draw_path()

    # 繪製敵方船隻
    enemy_ship.draw()

    # 繪製半徑為 FORMATION_CHANGE_DISTANCE 格和 SURROUND_RADIUS 格的圓周
    # 需要將圓的半徑從格子單位轉換為像素單位
    radius_large = FORMATION_CHANGE_DISTANCE * CELL_SIZE
    radius_small = SURROUND_RADIUS * CELL_SIZE
    enemy_pos_px = (int(enemy_ship.x * CELL_SIZE), int(enemy_ship.y * CELL_SIZE))

    # 繪製半徑為 FORMATION_CHANGE_DISTANCE 格的圓周（淡灰色）
    pygame.draw.circle(screen, LIGHT_GRAY, enemy_pos_px, int(radius_large), 1)

    # 繪製半徑為 SURROUND_RADIUS 格的圓周（淡灰色）
    pygame.draw.circle(screen, LIGHT_GRAY, enemy_pos_px, int(radius_small), 1)

    # 刷新顯示
    pygame.display.flip()

pygame.quit()
sys.exit()
