import numpy as np

def assign_tasks(starting_points, ending_points):
    """
    根據給定的起點和終點，進行任務分配，最小化最大任務距離。

    參數：
    - starting_points：numpy.ndarray，形狀為 (m, 2)，表示 m 個起點的二維座標。
    - ending_points：numpy.ndarray，形狀為 (m, 2)，表示 m 個終點的二維座標。

    返回：
    - assignments：dict，鍵為起點索引，值為分配到的終點索引。
    - max_cost：float，任務分配中最大的距離。
    """
    m = len(starting_points)  # 起點和終點的數量，假設相同

    # 步驟 1：建立成本表（cost_table），計算每個起點和終點之間的歐式距離
    cost_table = np.zeros((m, m))  # 初始化一個 m*m 的零矩陣作為成本表
    for i in range(m):
        for j in range(m):
            # 計算起點 i 和終點 j 之間的距離，並存入成本表
            cost_table[i][j] = np.linalg.norm(starting_points[i] - ending_points[j])

    # 步驟 2：建立一個全為 1 的選擇表（choose_table）
    choose_table = np.ones((m, m), dtype=int)

    # 步驟 3：將成本表中的內容排序，得到 list_cost_sort
    list_cost = []  # 初始化一個空列表，用於存儲成本和對應的索引
    for i in range(m):
        for j in range(m):
            # 將成本值和對應的起點、終點索引存入列表
            list_cost.append((cost_table[i][j], i, j))
    # 按照成本從大到小排序
    list_cost_sort = sorted(list_cost, key=lambda x: -x[0])

    # 初始化任務分配字典和已分配的行、列集合
    assignments = {}       # 用於存儲最終的任務分配結果，鍵為起點索引，值為終點索引
    assigned_rows = set()  # 已分配的起點索引集合
    assigned_cols = set()  # 已分配的終點索引集合

    # 步驟 4-8：循環處理，直到所有任務都分配完畢
    while len(assignments) < m:
        # 步驟 4：從排序後的列表中取出最大的成本值
        while list_cost_sort:
            cost, i, j = list_cost_sort.pop(0)  # 取出成本最大的一組 (cost, i, j)
            # 如果起點或終點已經被分配，跳過這一組
            if i in assigned_rows or j in assigned_cols:
                continue
            # 步驟 5：將選擇表中對應的位置設為 0，表示不再考慮這個組合
            choose_table[i][j] = 0
            break  # 跳出內層循環，進入檢查階段
        else:
            break  # 如果列表已空，退出主循環

        # 步驟 6：檢查選擇表中是否有行或列只剩下一個 1
        updated = True  # 用於判斷是否需要繼續檢查
        while updated:
            updated = False
            # 檢查每一行
            for i in range(m):
                if i in assigned_rows:
                    continue  # 如果起點已被分配，跳過
                if np.sum(choose_table[i, :]) == 1:
                    # 如果該行只剩一個 1，找到對應的終點
                    j = np.where(choose_table[i, :] == 1)[0][0]
                    if j in assigned_cols:
                        continue  # 如果終點已被分配，跳過
                    # 記錄任務分配
                    assignments[i] = j
                    assigned_rows.add(i)  # 標記起點已被分配
                    assigned_cols.add(j)  # 標記終點已被分配
                    # 將該行和該列的其他位置設為 0，表示不再考慮
                    choose_table[i, :] = 0
                    choose_table[:, j] = 0
                    # 保留自己本身的位置為 1
                    choose_table[i][j] = 1
                    updated = True  # 發生更新，繼續檢查
            # 檢查每一列
            for j in range(m):
                if j in assigned_cols:
                    continue  # 如果終點已被分配，跳過
                if np.sum(choose_table[:, j]) == 1:
                    # 如果該列只剩一個 1，找到對應的起點
                    i = np.where(choose_table[:, j] == 1)[0][0]
                    if i in assigned_rows:
                        continue  # 如果起點已被分配，跳過
                    # 記錄任務分配
                    assignments[i] = j
                    assigned_rows.add(i)  # 標記起點已被分配
                    assigned_cols.add(j)  # 標記終點已被分配
                    # 將該行和該列的其他位置設為 0
                    choose_table[i, :] = 0
                    choose_table[:, j] = 0
                    # 保留自己本身的位置為 1
                    choose_table[i][j] = 1
                    updated = True  # 發生更新，繼續檢查

    # 計算最大任務距離（最小化最大距離）
    max_cost = max(cost_table[i][assignments[i]] for i in assignments)

    #print(choose_table)

    #print(cost_table)

    # 返回任務分配結果和最大距離
    return assignments, max_cost

# 示例使用
if __name__ == "__main__":
    # 生成示例的起點和終點
    m = 5
    np.random.seed(0)
    starting_points = np.random.rand(m, 2) * 10
    ending_points = np.random.rand(m, 2) * 10

    # 調用函數進行任務分配
    assignments, max_cost = assign_tasks(starting_points, ending_points)

    # 輸出結果
    print("任務分配結果：")
    for i in range(m):
        if i in assignments:
            j = assignments[i]
            distance = np.linalg.norm(starting_points[i] - ending_points[j])
            print(f"起點 {i} 分配到終點 {j}，距離 = {distance:.2f}")
        else:
            print(f"起點 {i} 未分配到終點")

    print(f"最大任務距離：{max_cost:.2f}")

    print(assignments)
