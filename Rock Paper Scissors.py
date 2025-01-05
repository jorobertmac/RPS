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
    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.x_direction = 1
        self.y_direction = 1

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
        if self.x + self.width > other.x and self.x < other.x + other.width and self.y + self.height < other.y and self.y > other.y + other.height:
            self.x = 1
            other.x = w - self.width
            self.y = 1
            other.y = h - self.height
            

characters: list[Character] = []
for _ in range(10):
    characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
    characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height())))
    characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))




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
        for character in characters:
            character.move()
        
        for i, character in enumerate(characters):
            for j in range(i+1, len(characters)):
                character.collide(characters[j])
        
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

