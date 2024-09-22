import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import src.CommonRender as CommonRender
import inspect
import time

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False
        self.explode = False
        self.dt = 0
        self.ballOne = 0

    def Enter(self, params):
        # print(f"Enter method called from: {inspect.stack()[1].function}")
        # print(f"Called at line: {inspect.stack()[1].lineno}")
        self.paddle = params['paddle']
        self.bricks = params['bricks']
        self.health = params['health']
        self.score = params['score']
        self.high_scores = params['high_scores']
        self.ball = params['ball']
        self.level = params['level']
        # print(self.bricks)
        self.recover_points = 5000

        self.ball.dx = random.randint(-600, 600)  # -200 200
        self.ball.dy = random.randint(-180, -150)
        self.balls = []
        self.brickBall = 0
        self.explodeTime = 0
        self.cooldown = 0
        # self.power = False


    def update(self,  dt, events):
        self.dt = dt
        self.currentTime = math.floor(time.time())
        if self.currentTime - self.cooldown == 5:
            self.cooldown = 0
        # print(self.explode)
        # print(currentTime)
        # print(self.explodeTime)
        # print(currentTime - explodeTime)
        print(self.currentTime - self.explodeTime)
        # print(self.explodeTime)
        print(self.currentTime - self.cooldown)
        if self.explode and (self.currentTime - self.explodeTime) == 5:
            self.explode = False
            self.ball.skin = 0
            self.cooldown = math.floor(time.time())
            
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    gSounds['pause'].play()
                    #music_channel.play(sounds_list['pause'])
                if event.key == pygame.K_e:
                    # print('extrue')
                    if not self.explode and (self.cooldown == 0):
                        self.explodeTime = math.floor(time.time())
                        self.explode = True
                        self.ball.skin = 3
                        

                    


        if self.paused:
            return

        self.paddle.update(dt)
        self.ball.update(dt, self.level)
        # if self.brickBall != 0:
        #     self.brickBall.update(dt)
        for i in self.balls:
            i.update(dt, self.level)
            
            if i.Collides(self.paddle):
                # raise ball above paddle
                ####can be fixed to make it natural####
                i.rect.y = i.rect.y - 24
                i.dy = -i.dy

                # half left hit while moving left (side attack) the more side, the faster
                if i.rect.x + i.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                    i.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - i.rect.x))
                # right paddle and moving right (side attack)
                elif i.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                    i.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - i.rect.x))

        if self.ball.Collides(self.paddle):
            # raise ball above paddle
            ####can be fixed to make it natural####
            self.ball.rect.y = self.paddle.rect.y - 24
            self.ball.dy = -self.ball.dy

            # half left hit while moving left (side attack) the more side, the faster
            if self.ball.rect.x + self.ball.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                self.ball.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            # right paddle and moving right (side attack)
            elif self.ball.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                self.ball.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            gSounds['paddle-hit'].play()
        locationList = []

        for i in range(self.bricks[1]*self.bricks[2]):
            row = i // self.bricks[2]
            col = i % self.bricks[2]
            brick = self.bricks[0][row][col]
            # print(brick)
            

            if brick != 0:
                for j in self.balls:
                    if brick.alive and j.Collides(brick):
                        print('Collided!')
                        if brick.type != 'wall':
                            self.score = self.score + (brick.tier * 200 + brick.color * 25)
                        brick.Hit()
                        
                        # hit brick from left while moving right -> x flip
                        if j.rect.x + 6 < brick.rect.x and j.dx > 0:
                            j.dx = -j.dx
                            j.rect.x = brick.rect.x - 24

                        # hit brick from right while moving left -> x flip
                        elif j.rect.x + 18 > brick.rect.x + brick.width and j.dx < 0:
                            j.dx = -j.dx
                            j.rect.x = brick.rect.x + 96

                        # hit from above -> y flip
                        elif j.rect.y < brick.rect.y:
                            j.dy = -j.dy
                            j.rect.y = brick.rect.y - 24

                        # hit from bottom -> y flip
                        else:
                            j.dy = -j.dy
                            j.rect.y = brick.rect.y + 48

                        # whenever hit, speed is slightly increase, maximum is 450
                        if abs(j.dy) < 450:
                            j.dy = j.dy * 1.02
                        if self.CheckVictory():
                            gSounds['victory'].play()

                            g_state_manager.Change('victory', {
                                'level':self.level,
                                'paddle':self.paddle,
                                'health':self.health,
                                'score':self.score,
                                'high_scores':self.high_scores,
                                'ball':self.ball,
                                'recover_points':self.recover_points
                            })

         

                if brick.alive and self.ball.Collides(brick):
                    if brick.type != 'wall':
                        self.score = self.score + (brick.tier * 200 + brick.color * 25)
                    
                    brick.Hit()
                    if brick.type == 'freaky':
                        self.balls.append(brick.ballOne)
                    print(self.balls)
                    # self.ballOne = Ball(6)
                    # self.ballOne.rect.x = brick.x
                    # self.ballOne.rect.y = brick.y
                    # self.ballOne.dx = random.randint(-300,300)
                    # self.ballOne.dy = random.randint(-300,300)
        


                    # self.bricks.
                    row = self.bricks[1]
                    column = self.bricks[2]
                    # Get the number of rows and columns
                    num_rows = self.bricks[1]
                    num_cols = self.bricks[2]
                    row = i // num_cols
                    col = i % num_cols

                    topIndex = i - num_cols
                    if self.explode:
                        # print('explode')

                        if topIndex >= 0:  
                            topRow = topIndex // num_cols
                            topCol = topIndex % num_cols
                            if self.bricks[0][topRow][topCol] != 0:
                                self.bricks[0][topRow][topCol].Hit()

                        botIndex = i + num_cols
                        if botIndex < num_rows * num_cols: 
                            botRow = botIndex // num_cols
                            botCol = botIndex % num_cols
                            if self.bricks[0][botRow][botCol] != 0:
                                self.bricks[0][botRow][botCol].Hit()

                        if col > 0: 
                            leftIndex = i - 1
                            leftRow = leftIndex // num_cols
                            leftCol = leftIndex % num_cols
                            if self.bricks[0][leftRow][leftCol] != 0:
                                self.bricks[0][leftRow][leftCol].Hit()

                        if col < num_cols - 1:  
                            rightIndex = i + 1
                            rightRow = rightIndex // num_cols
                            rightCol = rightIndex % num_cols
                            if self.bricks[0][rightRow][rightCol] != 0:
                                self.bricks[0][rightRow][rightCol].Hit()

                    

                    # topBrickXY = ((brick.rect.x + brick.rect.width) // 2, (brick.rect.y - brick.rect.height) // 2)
                    # print(topBrickXY)
                    # print(f'column: {column}\trow: {row}')
                    # print(f'topBrickIndex: {topBrickIndex}\tbrickhit: {k}')
                    # topBrick = self.bricks[0][topBrickIndex]
                    # 
                    # for topBrick in self.bricks[0]:
                    #     # print(f'topBrick X: {topBrick.rect.x}\ttopBrick Y: {topBrick.rect.y}\ttopBrick Height: {topBrick.rect.height}\ttopBrick Width: {topBrick.rect.width}')
                    #     if (topBrickXY[0] >= topBrick.rect.x) and (topBrickXY[0] <= topBrick.rect.x + topBrick.rect.width) and (topBrickXY[1] <= topBrick.rect.y) and (topBrickXY[1] >= topBrick.rect.y + topBrick.rect.height):
                    #         topBrick.Hit()
                    #         print('Called')
                    # if self.explode:
                    # #Adjacent explosion code

                

                    # if self.score > self.recover_points:
                    #     self.health = min(3, self.health + 1)
                    #     self.recover_points = min(100000, self.recover_points * 2)

                    #     gSounds['recover'].play()
                        #music_channel.play(sounds_list['recover'])

                    if self.CheckVictory():
                        gSounds['victory'].play()

                        g_state_manager.Change('victory', {
                            'level':self.level,
                            'paddle':self.paddle,
                            'health':self.health,
                            'score':self.score,
                            'high_scores':self.high_scores,
                            'ball':self.ball,
                            'recover_points':self.recover_points
                        })

                    # hit brick from left while moving right -> x flip
                    if self.ball.rect.x + 6 < brick.rect.x and self.ball.dx > 0:
                        self.ball.dx = -self.ball.dx
                        self.ball.rect.x = brick.rect.x - 24

                    # hit brick from right while moving left -> x flip
                    elif self.ball.rect.x + 18 > brick.rect.x + brick.width and self.ball.dx < 0:
                        self.ball.dx = -self.ball.dx
                        self.ball.rect.x = brick.rect.x + 96

                    # hit from above -> y flip
                    elif self.ball.rect.y < brick.rect.y:
                        self.ball.dy = -self.ball.dy
                        self.ball.rect.y = brick.rect.y - 24

                    # hit from bottom -> y flip
                    else:
                        self.ball.dy = -self.ball.dy
                        self.ball.rect.y = brick.rect.y + 48

                    # whenever hit, speed is slightly increase, maximum is 450
                    if abs(self.ball.dy) < 450:
                        self.ball.dy = self.ball.dy * 1.02

                    break

        if self.ball.rect.y >= HEIGHT:
            self.explode = 0
            self.health -= 1
            gSounds['hurt'].play()

            if self.health == 0:
                g_state_manager.Change('game-over', {
                    'score':self.score,
                    'high_scores': self.high_scores
                })
            else:
                g_state_manager.Change('serve', {
                    'level': self.level,
                    'paddle': self.paddle,
                    'bricks': self.bricks,
                    'health': self.health,
                    'score': self.score,
                    'high_scores': self.high_scores,
                    'recover_points': self.recover_points
                })

    def Exit(self):
        pass

    def render(self, screen):
        color = [
            [255, 0, 0, 64],
            [255, 79, 0, 64],
            [255, 158, 0, 64],
            [255, 237, 0, 64],
            [192, 255, 0, 64],
            [113, 255, 0, 64],
            [34, 255, 0, 64],
            [0, 255, 44, 64],
            [0, 255, 124, 64],
            [0, 255, 203, 64],
            [0, 227, 255, 64],
            [0, 148, 255, 64],
            [0, 68, 255, 64],
            [10, 0, 255, 64],
            [89, 0, 255, 64],
            [169, 0, 255, 64],
            [247, 0, 254, 64],
            [255, 0, 182, 64],
            [255, 0, 103, 64],
            [255, 0, 23, 64]
        ]

        rectcolor = color[self.level % 20]

        filter_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        filter_surface.fill(rectcolor)
        screen.blit(filter_surface, (0, 0))

        brick = self.bricks[0]
        
        for i in self.balls:
            i.render(screen)
        # if self.brickBall != 0:
        #     self.brickBall.render(screen)
        # print(self.bricks[1])
        # print(self.bricks[2])
        # print(brick)
        for i in range(self.bricks[1] * self.bricks[2]):
            row = i // self.bricks[2]
            col = i % self.bricks[2]
            # print(brick[row][col])
            # print(f'{row}\t,\t{col}')
            if brick[row][col] != 0:
                brick[row][col].render(screen,self.dt)


        self.paddle.render(screen)
        self.ball.render(screen)

        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)
        small_font = pygame.font.Font('./fonts/font.ttf', 24)
        t_score = small_font.render("Speed:", False, (255, 255, 255))
        t_score_val = small_font.render(str(math.floor(math.sqrt((self.ball.dx*self.level)**2+(self.ball.dy*self.level)**2))), False, (255, 255, 255))
        screen.blit(t_score, (WIDTH - 180, 30))
        rect = t_score_val.get_rect()
        rect.topright = (WIDTH - 10, 30)
        screen.blit(t_score_val, rect)

        explodeshow = small_font.render("Explosion:", False, (255, 255, 255))
        screen.blit(explodeshow, (10, 5))
        # explodecounter = small_font.render(str(self.exp), False, (255, 255, 255))
        if not self.explode and self.cooldown == 0:
            screen.blit(small_font.render("Ready", False, (255, 255, 255)), (140, 5))
        elif not self.explode:
            screen.blit(small_font.render(f"Cooldown: {str(5-(self.currentTime-self.cooldown))}", False, (255, 255, 255)), (140, 5))
        if self.explode:
            screen.blit(small_font.render(str(5-(self.currentTime-self.explodeTime)), False, (255, 255, 255)), (140, 5))

        

        if self.paused:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)


    def CheckVictory(self):
        brick = self.bricks[0]
        # print(self.bricks[1])
        # print(self.bricks[2])
        # print(brick)
        # print(brick)
        for i in range(self.bricks[1] * self.bricks[2]):
            row = i // self.bricks[2]
            col = i % self.bricks[2]
            # print(brick[row][col])
            # print(f'{row}\t,\t{col}')
            if brick[row][col] != 0:
                if brick[row][col].alive and brick[row][col].type != 'wall':
                    return False
                

        # for brick in self.bricks[0]:
        #     if brick.alive:
        #         return False
        self.explode = 0
        self.cooldown = 0
        self.explode = False
        return True
