import pygame
import sys
import math
from random import randint, choice

pygame.init()
pygame.font.init()


w, h = 800, 800
chars = 20
black = (0,0,0)
dark_gray = (30,30,30)
white = (255,255,255)

#IMAGES
rock = pygame.image.load("rock.png")
paper = pygame.image.load("paper.png")
scissors = pygame.image.load("scissors.png")

# FONTS AND TEXT
score_font = pygame.font.SysFont("Ariel", 60)


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
    
    def get_direction(self, other: "Character"):
        abs_x = abs(self.x - other.x)
        abs_y = abs(self.y - other.y)
        if abs_x >= abs_y:
            if self.x >= other.x:
                return "right"
            else:
                return "left"
        else:
            if self.y >= other.y:
                return "bottom"
            else:
                return "top"

    
    def unlock_collision(self, other: "Character"):
        bounce = self.get_direction(other)
        offset = 1
        if bounce == "right":
                self.x = other.x+other.width + offset
        elif bounce == "left":
                other.x = self.x+self.width + offset
        elif bounce == "bottom":
                self.y = other.y+other.height + offset
        elif bounce == "top":
                other.y = self.y+self.height + offset

    
    def check_collision(self, other: "Character"):
        return self.x + self.width >= other.x and self.x <= other.x + other.width and self.y + self.height >= other.y and self.y <= other.y + other.height
    def change_x_direction(self):
            self.x_direction *= -1
    def change_y_direction(self):
            self.y_direction *= -1
    def bounce(self, other: "Character"):
        direction = self.get_direction(other)
        if direction in ["right", "left"]:
            self.change_x_direction()
            other.change_x_direction()
        elif direction in ["top", "bottom"]:
            self.change_y_direction()
            other.change_y_direction()
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
            self.bounce(other)
            self.collision_winner(other)
            

characters: list[Character] = []

def count_characters(list: list[Character]):
    total_rock = 0
    total_paper = 0
    total_scissors = 0
    for char in list:
        if char.image == rock:
            total_rock += 1
        elif char.image == paper:
            total_paper += 1
        elif char.image == scissors:
            total_scissors += 1
    return {"rock": total_rock, "paper": total_paper, "scissors": total_scissors}


for _ in range(chars):
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
        totals = count_characters(characters)
        def score_color(character: str):
            scores = [totals["rock"], totals["paper"], totals["scissors"]]
            if totals[character] == 0:
                return black
            elif totals[character] == max(scores):
                return (0,255,0)
            elif totals[character] == min(scores):
                return (255,0,0)
            return white

        # UPDATE SCORES
        rock_text = score_font.render("Rock:", False, score_color("rock"))
        paper_text = score_font.render("Paper:", False, score_color("paper"))
        scissors_text = score_font.render("Scissors:", False, score_color("scissors"))
        
        rock_score = score_font.render(f"{totals['rock']:02}", False, score_color("rock"))
        paper_score = score_font.render(f"{totals['paper']:02}", False, score_color("paper"))
        scissors_score = score_font.render(f"{totals['scissors']:02}", False, score_color("scissors"))
        
        # UPDATE CHARACTERS
        for i, character in enumerate(characters):
            for j in range(i+1, len(characters)):
                character.collide(characters[j])
        for character in characters:
            character.move()
        
        
        #DRAW ON SCREEN
        screen.fill(dark_gray)

        for character in characters:
            character.draw(screen)
        
        screen.blit(rock_text, (10, h-rock_text.get_height()-10))
        screen.blit(paper_text, (w/2-paper_text.get_width()/2-50, h-paper_text.get_height()-10))
        screen.blit(scissors_text, (w-scissors_text.get_width()-50-10, h-scissors_text.get_height()-10))

        screen.blit(rock_score, (rock_text.get_width()+ 10 + 10, h-rock_score.get_height()-10))
        screen.blit(paper_score, (w/2 + paper_score.get_width()/2, h-paper_score.get_height()-10))
        screen.blit(scissors_score, (w-scissors_score.get_width()-10, h-scissors_score.get_height()-10))
        
        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run()

