import pygame
from paddle import Paddle
from powerup import speedUP
from pygame import mixer
import sys
from ball import Ball
import time

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTRED = (255, 100, 100)
point_sound = mixer.Sound('point.wav')
hit_sound = mixer.Sound('hit.wav')
#paddleA_img = pygame.image.load("paddle_A.png")
redline = pygame.image.load("red_line.png")
BLUE = (0, 0, 128)

paddleB_hit_stats = 0
paddleB_big_paddle_stats = 0
paddleB_mini_paddle_stats = 0
paddleB_miss = 0

paddleA_hit_stats = 0
paddleA_big_paddle_stats = 0
paddleA_mini_paddle_stats = 0
paddleA_miss = 0

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong typ")
paddleA = Paddle(BLUE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleA_mini = Paddle(BLUE, 10, 50)
paddleA_mini.rect.x = 300
paddleA_mini.rect.y = 100

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

paddleB_mini = Paddle(WHITE, 10, 50)
paddleB_mini.rect.x = 400
paddleB_mini.rect.y = 100

ball = Ball(WHITE, 10, 10)
#ballimg = pygame.image.load("ball.png")
ball.rect.x = 345
ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
all_sprites_list.add(paddleB_mini)
all_sprites_list.add(paddleA_mini)


clock = pygame.time.Clock()

scoreA = 0
scoreB = 0

extra_scoreA = 0
extra_scoreB = 0


moveback = 0

moved = False


class game:
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]:
            scoreA = 50
        if keys[pygame.K_b]:
            scoreB = 50
        if keys[pygame.K_w]:
            paddleA.moveUp(5)
            paddleA_mini.moveDown(5)
            if paddleA.rect.x != 20:
                paddleA.moveLeft(80)
        if keys[pygame.K_s]:
            paddleA.moveDown(5)
            paddleA_mini.moveUp(5)
            if paddleA.rect.x != 20:
                paddleA.moveLeft(80)
        if keys[pygame.K_SPACE]:
            paddleA.moveRight(80)
            print(paddleA.rect.x)

        if paddleB.rect.y < ball.rect.y:
            paddleB.moveDown(5)
            paddleB_mini.moveUp(5)
        if paddleB.rect.y > ball.rect.y:
            paddleB.moveUp(5)
            paddleB_mini.moveDown(5)

        all_sprites_list.update()

        if ball.rect.x >= 690:
            scoreA += 1
            scoreA += extra_scoreA
            paddleB_miss += 1

            extra_scoreA = 0
            extra_scoreB = 0
            point_sound.play()
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            scoreB += 1
            scoreB += extra_scoreB
            paddleA_miss += 1
            extra_scoreB = 0
            extra_scoreA = 0
            #point_sound = mixer.Sound('point.wav')
            point_sound.play()
            ball.velocity[0] = -ball.velocity[0]

        if ball.rect.y > 490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:

            ball.velocity[1] = -ball.velocity[1]

        if pygame.sprite.collide_mask(ball, paddleA):
            paddleA_hit_stats += 1
            paddleA_big_paddle_stats += 1
        if pygame.sprite.collide_mask(ball, paddleB):
            paddleB_hit_stats += 1
            paddleB_big_paddle_stats += 1

        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
            hit_sound.play()
            ball.bounce()
        if pygame.sprite.collide_mask(ball, paddleA_mini):
            hit_sound.play()
            ball.bounce()
            extra_scoreA += 2
            paddleA_mini_paddle_stats += 1
            paddleA_hit_stats += 1
        if pygame.sprite.collide_mask(ball, paddleB_mini):
            hit_sound.play()
            ball.bounce()
            extra_scoreB += 2
            paddleB_mini_paddle_stats += 1
            paddleB_hit_stats += 1

        screen.fill(BLACK)

        all_sprites_list.draw(screen)

        screen.blit(redline, (349, 0))

        font = pygame.font.Font(None, 74)
        text = font.render(str(scoreA), 1, BLUE)
        screen.blit(text, (150, 10))
        text = font.render(str(scoreB), 1, WHITE)
        screen.blit(text, (420, 10))
        text = font.render("(+ " + str(extra_scoreA) + ")", 1, RED)
        screen.blit(text, (200, 10))
        text = font.render("(+"+str(extra_scoreB)+")", 1, RED)
        screen.blit(text, (540, 10))
        font = pygame.font.Font(None, 30)
        text = font.render("controlls: W,A,S,D", 1, LIGHTRED)
        screen.blit(text, (100, 200))

        clock.tick(60)
        class score():

            def endscoreB():
                font = pygame.font.Font(None, 90)
                screen.fill(BLACK)
                point_sound.stop()
                hit_sound.stop()
                stat = pygame.font.Font(None, 40)

                #centerx, centery = pygame.display.get_surface()
                text = font.render("AI WINS", 1, WHITE)
                #text_rect = text.get_rect(center=(700/2, 500/2))
                screen.blit(text, (110, 30))

                text = stat.render(
                    "AI Hits : " + str(paddleB_hit_stats), 1, WHITE)
                screen.blit(text, (110, 200))

                text = stat.render("AI big paddle hits : " +
                                   str(paddleB_big_paddle_stats), 1, WHITE)
                screen.blit(text, (110, 225))

                text = stat.render("AI mini paddle hits : " +
                                   str(paddleB_mini_paddle_stats), 1, WHITE)
                screen.blit(text, (110, 250))

                text = stat.render("AI Miss : " + str(paddleB_miss), 1, WHITE)
                screen.blit(text, (110, 275))

                text = stat.render("Player Hits : " +
                                   str(paddleA_hit_stats), 1, BLUE)
                screen.blit(text, (110, 90))

                text = stat.render("Player big paddle hits : " +
                                   str(paddleA_big_paddle_stats), 1, BLUE)
                screen.blit(text, (110, 115))

                text = stat.render("Player mini paddle hits : " +
                                   str(paddleA_mini_paddle_stats), 1, BLUE)
                screen.blit(text, (110, 140))
                text = stat.render("Player Miss : " +
                                   str(paddleA_miss), 1, BLUE)
                screen.blit(text, (110, 165))

            def endscoreA():

                font = pygame.font.Font(None, 90)
                stat = pygame.font.Font(None, 40)
                screen.fill(BLACK)
                point_sound.stop()
                hit_sound.stop()
                ball.kill()
                #centerx, centery = pygame.display.get_surface()
                text = font.render("PLAYER WINS", 1, BLUE)
                screen.blit(text, (110, 30))

                text = stat.render("Player Hits : " +
                                   str(paddleA_hit_stats), 1, BLUE)
                screen.blit(text, (110, 90))

                text = stat.render("Player big paddle hits : " +
                                   str(paddleA_big_paddle_stats), 1, BLUE)
                screen.blit(text, (110, 115))

                text = stat.render("Player mini paddle hits : " +
                                   str(paddleA_mini_paddle_stats), 1, BLUE)
                screen.blit(text, (110, 140))
                # paddleA_miss
                text = stat.render("Player Miss : " +
                                   str(paddleA_miss), 1, BLUE)
                screen.blit(text, (110, 165))

                text = stat.render(
                    "AI Hits : " + str(paddleB_hit_stats), 1, WHITE)
                screen.blit(text, (110, 200))

                text = stat.render("AI big paddle hits : " +
                                   str(paddleB_big_paddle_stats), 1, WHITE)
                screen.blit(text, (110, 225))

                text = stat.render("AI mini paddle hits : " +
                                   str(paddleB_mini_paddle_stats), 1, WHITE)
                screen.blit(text, (110, 250))

                text = stat.render(
                    "AI Miss : " + str(paddleB_miss), 1, WHITE)
                screen.blit(text, (110, 275))

        if scoreA >= 50:
            score.endscoreA()
        if scoreB >= 50:
            score.endscoreB()

        pygame.display.flip()


pygame.quit()
