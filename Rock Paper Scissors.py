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
green = (15,255,15)

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
small_font = pygame.font.SysFont("Ariel", 35)

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
test = False
def make_characters():
    if not test:
        for _ in range(chars):
            characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
            characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height())))
            characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))

    # TEST
    else:
        r=1
        p=1
        s=1
        for _ in range(r):
            characters.append(Character(rock, randint(0, w-rock.get_width()), randint(0, h-rock.get_height())))
        for _ in range(p):
            characters.append(Character(paper, randint(0, w-paper.get_width()), randint(0, h-paper.get_height())))
        for _ in range(s):
            characters.append(Character(scissors, randint(0, w-scissors.get_width()), randint(0, h-scissors.get_height())))

make_characters()
# START SCREEN
def start_screen():
    running = True

    rock_click = False
    paper_click = False
    scissors_click = False

    def choice():
        if rock_click:
            return 'rock'
        elif paper_click:
            return 'paper'
        elif scissors_click:
            return 'scissors'
        return False

    while running:
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()

        who_win_text = "who will win?"
        who_win_surface = large_font.render(who_win_text, False, white)
        who_win_rect = who_win_surface.get_rect(centerx=w//2, bottom=h//3)

        rock_text = 'rock: press R'
        rock_surface = main_font.render(rock_text, False, green if rock_click else white)
        rock_rect = rock_surface.get_rect(midtop=who_win_rect.midbottom)
        
        paper_text = 'paper: press P'
        paper_surface = main_font.render(paper_text, False, green if paper_click else white)
        paper_rect = paper_surface.get_rect(midtop=rock_rect.midbottom)

        scissors_text = 'scissors: press S'
        scissors_surface = main_font.render(scissors_text, False, green if scissors_click else white)
        scissors_rect = scissors_surface.get_rect(midtop=paper_rect.midbottom)

        confirm_text = f'press SPACE to confirm: {choice()}'
        confirm_surface = main_font.render(confirm_text, False, white)
        confirm_rect = confirm_surface.get_rect(midbottom=(w//2, h-10))

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rock_click=True
                    paper_click=False
                    scissors_click=False
                if event.key == pygame.K_p:
                    rock_click=False
                    paper_click=True
                    scissors_click=False
                if event.key == pygame.K_s:
                    rock_click=False
                    paper_click=False
                    scissors_click=True

        if rock_rect.collidepoint(mouse_pos):
            rock_surface = main_font.render(rock_text, False, green if rock_click else red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rock_click=True
                    paper_click=False
                    scissors_click=False
        if paper_rect.collidepoint(mouse_pos):
            paper_surface = main_font.render(paper_text, False, green if paper_click else red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rock_click=False
                    paper_click=True
                    scissors_click=False
        if scissors_rect.collidepoint(mouse_pos):
            scissors_surface = main_font.render(scissors_text, False, green if scissors_click else red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    rock_click=False
                    paper_click=False
                    scissors_click=True
        



        screen.fill(dark_gray)
        screen.blit(who_win_surface, who_win_rect)
        screen.blit(rock_surface, rock_rect)
        screen.blit(paper_surface, paper_rect)
        screen.blit(scissors_surface, scissors_rect)
        if choice():
            screen.blit(confirm_surface, confirm_rect)
        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                
            



        pygame.display.flip()
        clock.tick(60)

    return choice()

# MAIN GAME LOOP
def play_loop(player_choice: str):
    running = True
    count_down = 20
    timer = 0
    while running:
        timer += 1/60
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
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

        player_choice_text = f'you chose: {player_choice}'
        player_choice_surface = small_font.render(player_choice_text, False, white)
        player_choice_rect = player_choice_surface.get_rect(right=w-10, top=10)

        timer_text = f'{timer:.2f}'

        second_text = 'sec'
        seconds_text = 'secs'
        minute_text = 'min'
        minutes_text = 'mins'
        hour_text = 'hour'
        hours_text = 'hours'

        timer_box1_num = ...

        timer_surface = small_font.render(timer_text, False, white)
        timer_rect = timer_surface.get_rect(left=10, top=10)
        
        
        # UPDATE CHARACTERS
        for i, character in enumerate(characters):
            for j in range(i+1, len(characters)):
                character.collide(characters[j])
        for character in characters:
            character.move()
        
        
        #DRAW ON SCREEN
        screen.fill(dark_gray)

        screen.blit(player_choice_surface, player_choice_rect)
        screen.blit(timer_surface, timer_rect)
        for character in characters:
            character.draw(screen)
        
        screen.blit(rock_text, (10, h-rock_text.get_height()-10))
        screen.blit(paper_text, (w/2-paper_text.get_width()/2-50, h-paper_text.get_height()-10))
        screen.blit(scissors_text, (w-scissors_text.get_width()-50-10, h-scissors_text.get_height()-10))

        screen.blit(rock_score, (rock_text.get_width()+ 10 + 10, h-rock_score.get_height()-10))
        screen.blit(paper_score, (w/2 + paper_score.get_width()/2, h-paper_score.get_height()-10))
        screen.blit(scissors_score, (w-scissors_score.get_width()-10, h-scissors_score.get_height()-10))


        if len(characters) in [score for char, score in count_characters(characters).items()]:
            count_down -= 1
        if count_down <= 0:
            running = False
            for char, score in totals.items():
                if len(characters) == score:
                    return char

        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)


# GAME OVER
def game_over(player_choice: str, winning_char: str):
    running = True
    while running:
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        game_over_text = 'game over'
        game_over_surface = large_font.render(game_over_text, False, white)
        game_over_rect = game_over_surface.get_rect(centerx=w//2, bottom=h//4)

        winning_char_text = f'{winning_char} wins'
        winning_char_surface = large_font.render(winning_char_text, False, white)
        winning_char_rect = winning_char_surface.get_rect(center=(w//2, h//4))
        if player_choice == winning_char:
            won_lost = 'won'
        else:
            won_lost = 'lost'

        won_lost_text = f'you {won_lost}'
        won_lost_surface = large_font.render(won_lost_text, False, green if won_lost == 'won' else red)
        won_lost_rect = won_lost_surface.get_rect(midtop=winning_char_rect.midbottom)
        
        # you_lost_text = 'you lost'
        # you_lost_surface = large_font.render(you_lost_text, False, red)
        # you_lost_rect = you_lost_surface.get_rect(midtop=game_over_rect.midbottom)
        
        # you_won_text = 'you won'
        # you_won_surface = large_font.render(you_won_text, False, green)
        # you_won_rect = you_won_surface.get_rect(centerx=w//2, bottom=h//4)


        play_again_text = 'new game: press N'
        play_again_surface = main_font.render(play_again_text, False, white)
        play_again_rect = play_again_surface.get_rect(midtop=won_lost_rect.midbottom)

        quit_text = 'quit: press Q'
        quit_surface = main_font.render(quit_text, False, white)
        quit_rect = quit_surface.get_rect(midtop=play_again_rect.midbottom)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    characters.clear()
                    make_characters()
                    running = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        
        if play_again_rect.collidepoint(mouse_pos):
            play_again_surface = main_font.render(play_again_text, False, red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    characters.clear()
                    make_characters()
                    running = False

        if quit_rect.collidepoint(mouse_pos):
            quit_surface = main_font.render(quit_text, False, red)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
        
        screen.blit(winning_char_surface, winning_char_rect)
        screen.blit(won_lost_surface, won_lost_rect)
        # screen.blit(game_over_surface, game_over_rect)
        screen.blit(play_again_surface, play_again_rect)
        screen.blit(quit_surface, quit_rect)
        
        pygame.display.flip()
        clock.tick(60)





def run():
    running = True
    while running:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        #GAME LOGIG
        player_choice = start_screen()
        winning_char = play_loop(player_choice)
        game_over(player_choice, winning_char)
        
        #UPDATE SCREEN
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    run()

