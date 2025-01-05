import pygame
import math
import sys
from random import randint, choice

pygame.init()

w, h = 800, 800

#IMAGES
rock = pygame.image.load("rock.png")
paper = pygame.image.load("paper.png")
scissors = pygame.image.load("scissors.png")

class Character:
    def __init__(self, image: pygame.Surface, x: int, y: int, type = None) -> None:
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.x_direction = choice([-1, 1])
        self.y_direction = choice([-1, 1])
        self.type = type

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self):
        if self.x <= 0:
            self.x_direction = 1
        if self.x >= w-self.width:
            self.x_direction = -1
        self.x += self.x_direction

        if self.y <= 0:
            self.y_direction = 1
        if self.y >= w-self.height:
            self.y_direction = -1
        self.y += self.y_direction
    
    def collide(self, other: "Character"):
        if self.x + self.width >= other.x and self.x <= other.x + other.width and self.y + self.height >= other.y and self.y <= other.y + other.height:
            if self.x >= other.x and self.y <= other.y:
                self.x_direction = 1.2
                self.y_direction = -1.2
                other.x_direction = -1.2
                other.y_direction = 1.2
            else:
                self.x_direction *= -1.1
                other.x_direction *= -1.1
                self.y_direction *= -1.1
                other.y_direction *= -1.1
            if self.type == "rock":
                if other.type == "scissors":
                    other.image = rock
                    other.type = "rock"
                elif other.type == "paper":
                    self.image = paper
                    self.type = "paper"
            elif self.type == "paper":
                if other.type == "scissors":
                    self.image = scissors
                    self.type = "scissors"
                elif other.type == "rock":
                    other.image = paper
                    other.type = "paper"
            elif self.type == "scissors":
                if other.type == "rock":
                    self.image = rock
                    self.type = "rock"
                elif other.type == "paper":
                    other.image = scissors
                    other.type = "scissors"
                    
            

characters: list[Character] = []
for _ in range(7):
    characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height()), type="rock"))
    characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height()), type="paper"))
    characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height()), type="scissors"))




screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Pock, Scaper, Rissors")

clock = pygame.time.Clock()




def run():
    running = True
    while running:
        #EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #GAME LOGIG
        for i, character in enumerate(characters):
            for j in range(i+1, len(characters)):
                character.collide(characters[j])
        for character in characters:
            character.move()
        
        
        #DRAW ON SCREEN
        screen.fill((120, 120, 120))
        for character in characters:
            character.draw(screen)
        
        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run()

