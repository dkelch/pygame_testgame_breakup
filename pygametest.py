#!/usr/bin/env python3
import sys
import pygame
import time
import pygame.midi as midi

class BreackUp():
    def __init__(self):
        # Initialize here
        pygame.init()  # Initialize pygame

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        midi.init() # Initialize midi
        self.midi = 'lavaree1.mid'
        self.score = 0

    def gameloop(self):
        # Add midi music
        # High scores

        # Press enter to release ball
        # When paddle hit side, stop it
        # Stop ball sticking to paddle
        # better bounce physics
        # Add start menu

        # Initialize variables
        size = width, height = 640, 480
        speed = [2, 2]
        black = 0, 0, 0
        rt = 0
        lives = 3

        screen = pygame.display.set_mode(size)  # Set window size

        # Initialize surfaces (sprites)
        # Ball
        ball = pygame.image.load("intro_ball.gif")
        ball = pygame.transform.scale(ball, (20, 20))
        ballrect = ball.get_rect(center=(320,380))

        # Paddle
        paddle = pygame.image.load("paddle1.png")
        paddle = pygame.transform.scale(paddle, (90,20))
        paddlerect = paddle.get_rect(center=(320,400))

        # Brick
        bbrick = pygame.image.load("blue_brick.png")
        bbrick = pygame.transform.scale(bbrick, (40,20))
        rbrick = pygame.image.load("red_brick.png")
        rbrick = pygame.transform.scale(rbrick, (40,20))
        gbrick = pygame.image.load("green_brick.png")
        gbrick = pygame.transform.scale(gbrick, (40,20))
        ybrick = pygame.image.load("yellow_brick.png")
        ybrick = pygame.transform.scale(ybrick, (40,20))

        #Display current score
        font = pygame.font.Font(None, 22)
        text = font.render("Score: ", 1, (150,150,150))


        # Create an array of bricks
        bricks = []

        for num in range(80):
            if num >= 40: rt = 80
            if num < 10 or num >= 40 and num < 50:
                bricks.append([bbrick,bbrick.get_rect(center=(500-(num%10 * 40),10 + rt))])
            if num >= 10 and num < 20 or num >= 50 and num < 60:
                bricks.append([rbrick,rbrick.get_rect(center=(500-(num%10 * 40),30 + rt))])
            if num >= 20 and num < 30 or num >=60 and num < 70:
                bricks.append([gbrick,gbrick.get_rect(center=(500-(num%10 * 40),50 + rt))])
            if num >= 30 and num < 40 or num >= 70 and num < 80:
                bricks.append([ybrick, ybrick.get_rect(center=(500-(num%10 * 40),70 + rt))])
        # Display lives
        balls = []

        for num in range(3):
            liveloc = ((50 + num * 20),450)
            balls.append([ball,liveloc])

        # Music
        pygame.mixer.music.load(self.midi)
        pygame.mixer.music.play(-1)

        while 1:
            # Look for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                # Get keypressed and move paddle accordingly
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_RIGHT]:
                paddlerect = paddlerect.move([10, 0])
            if keys[pygame.K_LEFT]:
                paddlerect = paddlerect.move([-10, 0])
            # Move the ball randomly around the screen
            # If touches edge, move opposite direction
            ballrect = ballrect.move(speed)
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]
            # If ball touches paddle, bounce off
            if ballrect.colliderect(paddlerect):
                speed[1] = -speed[1]
            # If ball touches brick, remove and increment score
            for brick in bricks:
                if ballrect.colliderect(brick[1]):
                    bricks.remove(brick)
                    speed[1] = -speed[1]
                    self.score += 100
            # If paddle hits side of screen, stop
            # If ball hits the bottom of the screen, remove and decrement lives
            for live in balls:
                if ballrect.bottom > height:
                    ballrect = ball.get_rect(center=(320, 380))
                    balls.remove(live)
                    lives -= 1

            # If lives are 0, break out of game loop and display game over
            if lives == 0:
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.stop()
                game.gameover()

            # If bricks are gone, restart
            if len(bricks) == 0:
                break

            # Update score
            scoretext = font.render(str(self.score), 1, (150, 150, 150))
            # Create the window and place sprites on the screen
            screen.fill(black)
            screen.blit(ball, ballrect)
            screen.blit(paddle, paddlerect)
            # Put brick design on screen
            for brick in bricks:
                screen.blit(brick[0], brick[1])

            # Show lives
            for live in balls:
                screen.blit(live[0], live[1])

            screen.blit(text, (50,430))
            screen.blit(scoretext, (100, 430))
            pygame.display.flip()
            time.sleep(0.01)

    def gameover(self):
        size = width, height = 640, 480
        black = [0,0,0]
        screen = pygame.display.set_mode(size)  # Set window size
        # Display game over
        font = pygame.font.Font(None, 45)
        text = font.render("Game Over", 1, (150, 150, 150))

        while(1):
            # Look for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                # Get keypressed and move paddle accordingly
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: game.highscores()
            screen.blit(text, (320 - int(text.get_rect().width / 2), 240))
            pygame.display.flip()
            time.sleep(0.01)

    def highscores(self):
        size = width, height = 640, 480
        black = [0,0,0]
        screen = pygame.display.set_mode(size)  # Set window size
        # Display game over
        font = pygame.font.Font(None, 45)
        text = font.render("High Scores", 1, (150, 150, 150))
        scores = []
        # Read highscores from file
        with open("highscores.txt") as file:
            file = file.readlines()
            file = [x.strip() for x in file]
            # Add scores to display
            # Todo: split score from string and compare to current
            # then ask for user input if larger
            for score in file:
                scores.append(font.render(score, 1, (150, 150, 150)))
        screen.blit(text,(150,100))
        # Show scores
        count = 1
        for score in scores:
            screen.blit(score, (150,100 + (30*count)))
            count += 1

        while(1):
            # Look for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                # Get keypressed and move paddle accordingly
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
            pygame.display.flip()
            time.sleep(0.01)

if __name__ == "__main__":
    game = BreackUp()

    while(1):
        game.gameloop()

