# Name: Starbit Commander II
# Coder: Marco Janssen (twitter @marc0janssen, mail: marco@mjanssen.nl)
# year: 2021-04-07
# version: 1.0
# notes: Explosion code borrowed with permission from Derek Graham.
# notes: (https://deejaygraham.github.io/2016/10/28/tiny-asteroids-for-microbit/)
# notes: All other code is my own.

from microbit import *
import random


class Game:
    def __init__(self):
        self.screenMinX, self.screenMinY = 0, 0
        self.screenMaxX, self.screenMaxY = 4, 4
        self.brightnessMin, self.brightnessMax = 0, 9
        self.score = 0
        self.frameRate = 1000
        self.chanceSecondAstroid = 15
        self.scoreBonus = 1
        self.ticks = 0
        self.rowOfAstroids = 2
        

    def gameOver(self):
        spaceship.blowUpShip()
        sleep(300)
        display.scroll("Game Over")
        sleep(300)
        display.scroll("Score : " + str(self.score))
        sleep(500)
        display.scroll("Marco Janssen (c)2021", delay=50)

    def countScore(self):
        self.score += self.scoreBonus

    def increaseDifficulty(self):
        if self.ticks % 10 == 0:
            self.frameRate = max(self.frameRate - 100, 400)
            self.scoreBonus += 1

        if self.ticks % 15 == 0:
            self.chanceSecondAstroid = max(self.chanceSecondAstroid - 2, 3)
            self.scoreBonus += 3

        if self.ticks % 25 == 0:
            self.rowOfAstroids = min(self.rowOfAstroids + 1, 5)
            self.scoreBonus += 5

    def gameStart(self):
        
        display.scroll("3... 2... 1... Launch...", delay=70)
        
        while True:
            astroidField.createAstroid()

            astroidField.drawAstroids()
            spaceship.draw()

            if spaceship.collide():
                self.gameOver()
                break

            sleep(self.frameRate)

            astroidField.hideAstroids()
            spaceship.hide()

            if button_a.was_pressed():
                spaceship.moveLeft()
            elif button_b.was_pressed():
                spaceship.moveRight()

            astroidField.moveAstroids()
            astroidField.clearPassedAstroids()
            self.increaseDifficulty()


class Spaceship:
    def __init__(self):
        self.properties = [2, game.screenMaxY, game.brightnessMax]

    def moveLeft(self):
        self.properties[0] = max(self.properties[0] - 1, game.screenMinX)

    def moveRight(self):
        self.properties[0] = min(self.properties[0] + 1, game.screenMaxX)

    def draw(self):
        display.set_pixel(self.properties[0], self.properties[1], self.properties[2])

    def hide(self):
        display.set_pixel(self.properties[0], self.properties[1], game.brightnessMin)

    def collide(self):
        for astroid in astroidField.astroidField:
            if (
                astroid.properties[0] == self.properties[0]
                and astroid.properties[1] == self.properties[1]
            ):
                return True
        return False

    def blowUpShip(self):
        self.hide()

        self.drawExplosion(self.properties[2], 1)
        sleep(200)
        display.clear()

        for brightness in range(self.properties[2], 0, -1):
            self.drawExplosion(brightness, 2)
            sleep(200)
            display.clear()

    def drawExplosion(self, brightness, radius):
        x = self.properties[0]
        y = self.properties[1]
        left_of_centre = x - radius
        right_of_centre = x + radius
        above_centre = y - radius

        if left_of_centre >= game.screenMinX:
            display.set_pixel(left_of_centre, y, brightness)
            display.set_pixel(left_of_centre, above_centre, brightness)

        display.set_pixel(x, above_centre, brightness)

        if right_of_centre <= game.screenMaxX:
            display.set_pixel(right_of_centre, y, brightness)
            display.set_pixel(right_of_centre, above_centre, brightness)


class Astroid:
    def __init__(self):
        self.properties = [0, 0, 0]
        self.properties[0] = random.randint(game.screenMinX, game.screenMaxX)
        self.properties[2] = random.randint(
            game.brightnessMin + 1, game.brightnessMax - 3
        )

    def draw(self):
        display.set_pixel(self.properties[0], self.properties[1], self.properties[2])

    def hide(self):
        display.set_pixel(self.properties[0], self.properties[1], game.brightnessMin)

    def move(self):
        self.properties[1] = min(self.properties[1] + 1, game.screenMaxY + 1)


class AstroidField:
    def __init__(self):
        self.astroidField = []

    def drawAstroids(self):
        for astroid in self.astroidField:
            astroid.draw()

    def moveAstroids(self):
        for astroid in self.astroidField:
            astroid.move()

        game.ticks += 1

    def clearPassedAstroids(self):
        for astroid in self.astroidField:
            if self.astroidField[0].properties[1] > game.screenMaxY:
                self.astroidField.pop(0)
                del astroid
                game.countScore()

    def hideAstroids(self):
        for astroid in self.astroidField:
            astroid.hide()

    def createAstroid(self):
        if not game.ticks % game.rowOfAstroids == 0:
            astroid = Astroid()
            self.astroidField.append(astroid)
            xPosFirstAstroid = astroid.properties[0]

            chance = random.randrange(game.chanceSecondAstroid)
            astroid = Astroid()
            if xPosFirstAstroid != astroid.properties[0] and chance == 0:
                self.astroidField.append(astroid)
            else:
                del astroid


game = Game()
spaceship = Spaceship()
astroidField = AstroidField()

game.gameStart()
