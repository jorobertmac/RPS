import pygame
import sys
import math
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
        self.x_direction = choice([-1, 1])
        self.y_direction = choice([-1, 1])

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
    
    def unlock_collision(self, other: "Character"):
        abs_x = abs(self.x - other.x)
        abs_y = abs(self.y - other.y)
        if abs_x >= abs_y:
            if self.x >= other.x:
                self.x = other.x+other.width
            else:
                other.x = self.x+self.width
        else:
            if self.y >= other.y:
                self.y = other.y+other.height
            else:
                other.y = self.y+self.height

    
    def check_collision(self, other: "Character"):
        return self.x + self.width >= other.x and self.x <= other.x + other.width and self.y + self.height >= other.y and self.y <= other.y + other.height
    def change_x_direction(self):
            self.x_direction *= -1
    def change_y_direction(self):
            self.y_direction *= -1
    def change_image(self, image):
        self.image = image
    def collision_winner(self, other: "Character"):
        # CHECK ROCK
        if self.image == rock and other.image == scissors:
            other.change_image(rock)
        elif self.image == rock and other.image == paper:
            self.change_image(paper)
        # CHECK PAPER
        elif self.image == paper and other.image == rock:
            other.change_image(paper)
        elif self.image == paper and other.image == scissors:
            self.change_image(scissors)
        # CHECK SCISSORS
        elif self.image == scissors and other.image == paper:
            other.change_image(scissors)
        elif self.image == scissors and other.image == rock:
            self.change_image(rock)


    def collide(self, other: "Character"):
        if self.check_collision(other):
            self.unlock_collision(other)
            self.change_x_direction()
            other.change_x_direction()
            self.change_y_direction()
            other.change_y_direction()
            self.collision_winner(other)
            

characters: list[Character] = []
def validate(self: Character, other: Character):
    while self.check_collision(other):
        self.x -= 1
        self.y -= 1


for _ in range(20):
    characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
    characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height())))
    characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))

for i, character in enumerate(characters):
    for j in range(i+1, len(characters)):
        validate(character, characters[j])

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

