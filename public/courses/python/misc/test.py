triangle = []

for row in range(5):
    current_row = []
    for col in range(row + 1):
        if col == 0 or col == row:
            # 提示：每行两端都是 1
            current_row.append(1)
        else:
            # 提示：中间值 = 左上 + 右上
            value = (
                triangle[row - 1][col - 1]
                + triangle[row - 1][col]
            )
            current_row.append(value)
    triangle.append(current_row)

for row in triangle:
    print(row)