from Block import Block


def worlds(width, height, level):
    """ gives blocks for nth world """

    blocks = list()
    if level == 1:
        block_left_top1 = Block(0, 0, int(width / 3), 10)
        block_left_top2 = Block(0, 0, 10, int(height / 3))

        block_right_top1 = Block(width - int(width / 3), 0, int(width / 3), 10)
        block_right_top2 = Block(width - 10, 0, 10, int(height / 3))

        block_left_bottom1 = Block(0, height - 10, int(width / 3), 10)
        block_left_bottom2 = Block(0, height - int(height / 3), 10, int(height / 3))

        block_right_bottom1 = Block(width - int(width / 3), height - 10, int(width / 3), 10)
        block_right_bottom2 = Block(width - 10, height - int(height / 3), 10, int(height / 3))

        blocks.append(block_left_top1)
        blocks.append(block_left_top2)
        blocks.append(block_left_bottom1)
        blocks.append(block_left_bottom2)
        blocks.append(block_right_top1)
        blocks.append(block_right_top2)
        blocks.append(block_right_bottom1)
        blocks.append(block_right_bottom2)
    elif level == 2:

        block_top = Block(0, 0, width, 10)
        block_left = Block(0, 0, 10, height)
        block_bottom = Block(0, height - 10, width, 10)
        block_right = Block(width - 10, 0, 10, height)

        blocks.append(block_top)
        blocks.append(block_left)
        blocks.append(block_bottom)
        blocks.append(block_right)

    elif level > 2:
        block_top = Block(0, 0, width, 10)
        block_left = Block(0, 0, 10, height)
        block_bottom = Block(0, height - 10, width, 10)
        block_right = Block(width - 10, 0, 10, height)

        block_mid1 = Block(int(width / 2), 0, 10, int(height / 3))
        block_mid2 = Block(int(width / 2), height - int(height / 3), 10, int(height / 3))

        blocks.append(block_top)
        blocks.append(block_left)
        blocks.append(block_bottom)
        blocks.append(block_right)
        blocks.append(block_mid1)
        blocks.append(block_mid2)

    return blocks
