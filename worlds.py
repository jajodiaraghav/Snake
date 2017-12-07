def worlds(n):
    # gives blocks for nth world
    blocks = list()

    if n == 1:
        for i in range(0, 250 // 10):
            blocks.append((i * 10, 0))
            blocks.append((550 + i * 10, 0))
            blocks.append((i * 10, 590))
            blocks.append((550 + i * 10, 590))
        for i in range(0, 20):
            blocks.append((0, (i + 1) * 10))
            blocks.append((0, 400 + (i + 1) * 10))
            blocks.append((790, (i + 1) * 10))
            blocks.append((790, 400 + (i + 1) * 10))
    elif n == 2:
        for i in range(0, 800 // 10):
            blocks.append((i * 10, 0))
            blocks.append((i * 10, 590))
        for i in range(0, 58):
            blocks.append((0, (i + 1) * 10))
            blocks.append((790, (i + 1) * 10))

    elif n > 2:
        for i in range(0, 800 // 10):
            blocks.append((i * 10, 0))
            blocks.append((i * 10, 590))
        for i in range(0, 58):
            blocks.append((0, (i + 1) * 10))
            blocks.append((790, (i + 1) * 10))
        for i in range(0, 25):
            blocks.append((400, (i + 1) * 10))
        for i in range(35, 58):
            blocks.append((400, (i + 1) * 10))

    return blocks
