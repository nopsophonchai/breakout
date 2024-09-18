import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *


import src.CommonRender as CommonRender
from src.Ball import Ball

class ServeState(BaseState):
    def __init__(self):
        super(ServeState, self).__init__()

    def Enter(self, params):
        self.paddle = params["paddle"]
        self.bricks = params["bricks"]
        self.health = params["health"]
        self.score = params["score"]
        self.high_scores = params["high_scores"]
        self.level = params["level"]
        self.recover_points = params["recover_points"]


        self.ball = Ball(1)
        self.ball.skin = 0
        self.dt = 0



    def Exit(self):
        pass

    def update(self,  dt, events):
        self.dt = dt
        self.paddle.update(dt)
        # put the ball above the paddle
        self.ball.rect.x = self.paddle.x + (self.paddle.width/2) - 12
        self.ball.rect.y = self.paddle.y - 24

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('play', {
                        'paddle':self.paddle,
                        'level':self.level,
                        'health':self.health,
                        'score':self.score,
                        'high_scores': self.high_scores,
                        'ball':self.ball,
                        'recover_points': self.recover_points,
                        'bricks':self.bricks
                    })

    def render(self, screen):
        color = [
                            [255, 0, 0],
                            [255, 79, 0],
                            [255, 158, 0],
                            [255, 237, 0],
                            [192, 255, 0],
                            [113, 255, 0],
                            [34, 255, 0],
                            [0, 255, 44],
                            [0, 255, 124],
                            [0, 255, 203],
                            [0, 227, 255],
                            [0, 148, 255],
                            [0, 68, 255],
                            [10, 0, 255],
                            [89, 0, 255],
                            [169, 0, 255],
                            [247, 0, 254],
                            [255, 0, 182],
                            [255, 0, 103],
                            [255, 0, 23]
                        ]
        rectcolor = color[self.level % 20]

        filter_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        filter_surface.fill((rectcolor))
        screen.blit(filter_surface, (0,0))

        self.paddle.render(screen)
        self.ball.render(screen)

        brick = self.bricks[0]
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


        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        t_level = gFonts['large'].render("Level" + str(self.level), False, (255, 255, 255))
        rect = t_level.get_rect(center=(WIDTH/2, HEIGHT / 3))
        screen.blit(t_level, rect)

        t_press_enter = gFonts['medium'].render("Press Enter to Serve", False, (255, 255, 255))
        rect = t_press_enter.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(t_press_enter, rect)