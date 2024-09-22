import random, pygame, math
from src.Brick import Brick
from src.ModBrick import ModBrick
import inspect
from src.BrickWall import BrickWall

#patterns
NONE = 1
SINGLE_PYRAMID = 2
MULTI_PYRAMID = 3

SOLID = 1            # all colors the same in this row
ALTERNATE = 2        # alternative colors
SKIP = 3             # skip every other brick
NONE = 4             # no block this row


class LevelMaker:
    def __init__(self):
        pass

    @classmethod
    def CreateMap(cls, level, screen):
        bricks = []
        # print(f"Enter method called from: {inspect.stack()[1]}")
        # print(f"Called at line: {inspect.stack()[1].lineno}")
        # Not gooood enough!!


        num_rows = random.randint(5, 10)
        num_cols = random.randint(7, 13)
        # num_cols = 13
        if num_cols % 2 == 0:
            num_cols += 1
        clicks = []
        clicks = [[0 for i in range(num_cols)] for x in range(num_rows)]
        bricks = [[0 for i in range(num_cols)] for x in range(num_rows)]

        #Make it harder by adding 
        highest_tier = math.floor(level/5.0)
        highest_color = min(5, level % 5 + 3)
        pyramid_pattern = random.choice([True,False])
        # pyramid_pattern = True
        brickCol = random.choice([True,True])
        # brickCol = Fa
        wallIndex = random.randint(0, num_cols-1)
        wallSym = num_cols - wallIndex -1

        for y in range(num_rows):
            floorChoice = (level+10)/100 if (level+10)/100 != 90 else 90
            brickFloor = random.choices([True,False],[1-floorChoice,1-floorChoice])[0]
            # brickFloor = True
            # brickFloor = random.choices([False,True],[50,50])[0]
            # brickWall = random.choices([True,False],[floorChoice,1-floorChoice])[0]
            skip_pattern = random.choice([True, False])
            alternate_pattern = random.choice([True, False])
            

            alternate_color1 = random.randint(1, highest_color)
            alternate_color2 = random.randint(1, highest_color)
            a = level-1
            b = highest_tier
            if a > b:
                alternate_tier1 = random.randint(b, a)
                alternate_tier2 = random.randint(b, a)
            else:
                alternate_tier1 = random.randint(a, b)
                alternate_tier2 = random.randint(a, b)

            skip_flag = random.choice([True, False])

            alternate_flag = random.choice([True, False])

            solid_color = random.randint(1, highest_color)
            solid_tier = random.randint(0, highest_tier)

            for x in range(num_cols):
                if pyramid_pattern:
                    prob = 20+(level*10) if 20+(level*10) != 90 else 90
                    if y <= num_rows // 2:
                        
                        if x >= (num_cols // 2) - y and x <= (num_cols // 2) + y:
                            if brickFloor:
                                b = BrickWall(x*96+24 + (13-num_cols) * 48, y*48,screen)
                            else:
                                b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)[0]
                    else:
                        if x >= (num_cols // 2) - (num_rows - y - 1) and x <= (num_cols // 2) + (num_rows - y - 1):
                            b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)[0]
                    if random.choice([True,False]) and x == num_cols-1:
                        pyramid_pattern = False
                    # print(b)
                else:
                    if skip_pattern and skip_flag:
                        skip_flag = not skip_flag
                        continue
                    else:
                        skip_flag = not skip_flag
                    prob = 20+(level*10) if 20+(level*10) != 90 else 90
                    # print(prob)
                    # print(f'First: {(y == num_rows-1 and y!= 0)}\tSecond: {(x != 0 and x != num_cols-1)}')
                    # if brickWall:
                    #     print('BrickWall')
                    #     if x == 0 or x == num_cols-1: 
                    #         b = [BrickWall(x*96+24 + (13-num_cols) * 48, y*48,screen)]
                    #     else:
                    #         b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)
                    if brickFloor:
                        print(f"Called\t{y}")
                        if (y!= 0) and num_cols != 13: 
                            b = [BrickWall(x*96+24 + (13-num_cols) * 48, y*48,screen)]
                        if (y!= 0) and num_cols == 13: 
                            if x == 0 or x == 12:
                                b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)
                            else:
                                b = [BrickWall(x*96+24 + (13-num_cols) * 48, y*48,screen)]
                        else:
                            # print(f'{y} \t called')
                            b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)
                    else:
                        b = random.choices([ModBrick(x*96+24 + (13-num_cols) * 48, y*48,screen),Brick(x*96+24 + (13-num_cols) * 48, y*48,screen)],[100-prob, prob], k=1)
                    if random.choice([True,False]) and x == num_cols-1:
                        pyramid_pattern = True
                    b = b[0]
                if brickCol:
                    # print(f'1st Col: {wallIndex}\t2nd Col:{wallSym}')
                    if (x == wallIndex or x == wallSym ) and y != 0:
                        print(x)
                        b = BrickWall(x*96+24 + (13-num_cols) * 48, y*48,screen)
                if b != 0:
                    if alternate_pattern and alternate_flag:
                        b.color = alternate_color1
                        b.tier = alternate_tier1
                        alternate_flag = not alternate_flag
                    else:
                        b.color = alternate_color2
                        b.tier = alternate_tier2
                        alternate_flag = not alternate_flag

                    if not alternate_pattern:
                        b.color = solid_color
                        b.tier = solid_tier
                clicks[y][x] = 1
                bricks[y][x] = b
                
            #table.insert(bricks, b)

        # print(bricks)
        # print(clicks)
        if all(all(element == 0 for element in sublist) for sublist in bricks):
            return LevelMaker.CreateMap(level, screen)

        else:
            return (bricks,num_rows,num_cols)