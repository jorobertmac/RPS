import pygame
import sys
import math
from random import randint, choice

pygame.init()
pygame.font.init()

# CONSTANTS
w, h = 800, 800
chars = 20
black = (0,0,0)
dark_gray = (30,30,30)
white = (255,255,255)
red = (255, 15, 15)

screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Pock, Scaper, Rissors")
clock = pygame.time.Clock()

#IMAGES
rock = pygame.image.load("rock.png")
paper = pygame.image.load("paper.png")
scissors = pygame.image.load("scissors.png")

# FONTS
main_font = pygame.font.SysFont("Ariel", 60)
large_font = pygame.font.SysFont("Ariel", 150)

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

# MAKE CHARACTERS AND APPEND TO -characters- LIST
test = True
def make_characters():
    if not test:
        for _ in range(chars):
            characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
            characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height())))
            characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))

    # TEST
    else:
        for _ in range(55):
            characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
        for _ in range(5):
            characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))

make_characters()
# START SCREEN
def start_screen():
    running = True
    rock_click = False
    paper_click = False
    scissors_click = False

    while running:
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        who_win_text = "who will win?"
        who_win_surface = large_font.render(who_win_text, False, white)
        who_win_rect = who_win_surface.get_rect(centerx=w//2, bottom=h//3)

        rock_text = 'rock'
        rock_surface = main_font.render(rock_text, False, red if rock_click else white)
        rock_rect = rock_surface.get_rect(midtop=who_win_rect.midbottom)
        
        paper_text = 'paper'
        paper_surface = main_font.render(paper_text, False, red if paper_click else white)
        paper_rect = paper_surface.get_rect(midtop=rock_rect.midbottom)

        scissors_text = 'scissors'
        scissors_surface = main_font.render(scissors_text, False, red if scissors_click else white)
        scissors_rect = scissors_surface.get_rect(midtop=paper_rect.midbottom)

        mouse_pos = pygame.mouse.get_pos()

        if rock_rect.collidepoint(mouse_pos):
            rock_surface = main_font.render(rock_text, False, red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rock_click=True
        if paper_rect.collidepoint(mouse_pos):
            paper_surface = main_font.render(paper_text, False, red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    paper_click=True
        if scissors_rect.collidepoint(mouse_pos):
            scissors_surface = main_font.render(scissors_text, False, red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    scissors_click=True



        screen.fill(dark_gray)
        screen.blit(who_win_surface, who_win_rect)
        screen.blit(rock_surface, rock_rect)
        screen.blit(paper_surface, paper_rect)
        screen.blit(scissors_surface, scissors_rect)


        pygame.display.flip()
        clock.tick(60)

# MAIN GAME LOOP
def play_loop():
    running = True
    while running:
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
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
        rock_text = main_font.render("rock:", False, score_color("rock"))
        paper_text = main_font.render("paper:", False, score_color("paper"))
        scissors_text = main_font.render("scissors:", False, score_color("scissors"))
        
        rock_score = main_font.render(f"{totals['rock']:02}", False, score_color("rock"))
        paper_score = main_font.render(f"{totals['paper']:02}", False, score_color("paper"))
        scissors_score = main_font.render(f"{totals['scissors']:02}", False, score_color("scissors"))
        
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

        if len(characters) in [score for char, score in count_characters(characters).items()]:
            game_over()
        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)

# GAME OVER
def game_over():
    pygame_events = pygame.event.get()

    game_over_text = 'game over'
    play_again_text = 'play game'
    quit_text = 'quit'

    game_over_surface = large_font.render(game_over_text, False, white)
    game_over_rect = game_over_surface.get_rect(centerx=w//2, bottom=h//2)

    play_again_surface = main_font.render(play_again_text, False, white)
    play_again_rect = play_again_surface.get_rect(midtop=game_over_rect.midbottom)

    quit_surface = main_font.render(quit_text, False, white)
    quit_rect = quit_surface.get_rect(midtop=play_again_rect.midbottom)

    mouse_pos = pygame.mouse.get_pos()
    
    if play_again_rect.collidepoint(mouse_pos):
        play_again_surface = main_font.render(play_again_text, False, red)
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                characters.clear()
                make_characters()

    if quit_rect.collidepoint(mouse_pos):
        quit_surface = main_font.render(quit_text, False, red)
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
    
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(play_again_surface, play_again_rect)
    screen.blit(quit_surface, quit_rect)




def run():
    running = True
    while running:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        #GAME LOGIG
        start_screen()
        play_loop()
        
        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run()

