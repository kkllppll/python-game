import pygame
import random
import sys
from pygame.constants import K_DOWN, K_UP, K_LEFT, K_RIGHT

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Elina Game")

        self.FPS = pygame.time.Clock()
        self.FONT = pygame.font.SysFont('Verdana', 26, bold=True)

        self.HEIGHT = 600
        self.WIDTH = 1000
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_RED = (255, 0, 0)

        self.start_screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.start_bg = pygame.transform.scale(pygame.image.load('start_screen.png'), (self.WIDTH, self.HEIGHT))

        self.main_display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.bg = pygame.transform.scale(pygame.image.load('background.png'), (self.WIDTH, self.HEIGHT))

        self.bg_X1 = 0
        self.bg_X2 = self.bg.get_width()
        self.bg_move = 2

        self.player_size = (100, 100)
        self.player = pygame.image.load('player.png').convert_alpha()
        self.player = pygame.transform.scale(self.player, self.player_size)

        self.player_rect = self.player.get_rect()
        self.player_rect_center = self.main_display.get_rect().center

        self.player_move_down = [0, 4]
        self.player_move_right = [4, 0]
        self.player_move_up = [0, -4]
        self.player_move_left = [-4, 0]

       

        self.CREATE_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.CREATE_ENEMY, 1500)

        self.CREATE_BONUS = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CREATE_BONUS, 1000)

        self.bonuses = []
        self.enemies = []

        self.score = 0
        self.max_score = 5
        self.lives = 3

        self.waiting_for_start = True
        self.waiting_for_end = True  
        self.is_game_over = True 

    def show_start_screen(self):
        while self.waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_s:
                        self.waiting_for_start = False

            self.start_screen.blit(self.start_bg, (0, 0))

            text = "HELLO! COLLECT 5 BONUSES TO WIN.\nYOU HAVE 3 LIVES\nTO START THE GAME PRESS - s,\nTO LEAVE - esc, TO PAUSE - p.\nGOOD LUCK, HEHE!"
            
            text_lines = text.splitlines()
            text_bg_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 2 - 15, self.WIDTH // 2, 150)

            pygame.draw.rect(self.main_display, self.COLOR_WHITE, text_bg_rect)

            line_spacing = 30
            for i, line in enumerate(text_lines):
                line_text = self.FONT.render(line, True, self.COLOR_BLACK)
                self.start_screen.blit(line_text, (self.WIDTH // 2 - line_text.get_width() // 2, self.HEIGHT // 2 - line_text.get_height() // 2 + i * line_spacing))

            pygame.display.flip()

    def create_enemy(self):
        enemy_size = (200, 100)
        enemy = pygame.image.load('enemy.png').convert_alpha()
        enemy_rect = pygame.Rect(self.WIDTH, random.randint(0, self.HEIGHT - enemy.get_height()), enemy_size[0], enemy_size[1])
        enemy = pygame.transform.scale(enemy, enemy_size)
        enemy_move = [random.randint(-6, -3), 0]

        return [enemy, enemy_rect, enemy_move]

    def create_bonus(self):
        bonus_size = (200, 200)
        bonus = pygame.image.load('bonus.png').convert_alpha()
        # Randomly choose the horizontal position of the bonus, ensuring it stays within the screen boundaries
        # by subtracting the width of the bonus from the range of possible positions.
        bonus_rect = pygame.Rect(random.randint(bonus.get_width(), self.WIDTH - bonus.get_width()), 
                                 -bonus.get_height(), # Set the initial vertical position above the visible screen
                                 bonus_size[0], bonus_size[1]) # Set the size of the bonus.
        
        bonus = pygame.transform.scale(bonus, bonus_size)
        bonus_move = [0, random.randint(3, 6)]

        return [bonus, bonus_rect, bonus_move]

    def main_game_loop(self):
        playing = True
        paused = False

        while playing:
            self.FPS.tick(120)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

                if event.type == self.CREATE_ENEMY:
                    if not paused:
                        self.create_enemy()
                        self.enemies.append(self.create_enemy())

                if event.type == self.CREATE_BONUS:
                    if not paused:
                        self.create_bonus()
                        self.bonuses.append(self.create_bonus())

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        playing = False

            if self.score >= self.max_score:
                playing = False
                win_text = self.FONT.render("YOU WON! CONGRATULATIONS!", True, self.COLOR_BLUE)
                self.main_display.blit(win_text, (self.WIDTH // 2 - win_text.get_width() // 2, self.HEIGHT // 2 - win_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)

            self.bg_X1 -= self.bg_move
            self.bg_X2 -= self.bg_move

            if self.bg_X1 < -self.bg.get_width():
                self.bg_X1 = self.bg.get_width()

            if self.bg_X2 < -self.bg.get_width():
                self.bg_X2 = self.bg.get_width()

            if not paused:
                self.main_display.blit(self.bg, (self.bg_X1, 0))
                self.main_display.blit(self.bg, (self.bg_X2, 0))

                keys = pygame.key.get_pressed()

                if keys[K_DOWN] and self.player_rect.bottom < self.HEIGHT:
                    self.player_rect = self.player_rect.move(self.player_move_down)

                if keys[K_RIGHT] and self.player_rect.right < self.WIDTH:
                    self.player_rect = self.player_rect.move(self.player_move_right)

                if keys[K_UP] and self.player_rect.top > 0:
                    self.player_rect = self.player_rect.move(self.player_move_up)

                if keys[K_LEFT] and self.player_rect.left > 0:
                    self.player_rect = self.player_rect.move(self.player_move_left)

                for enemy in self.enemies:
                    enemy[1] = enemy[1].move(enemy[2])
                    self.main_display.blit(enemy[0], enemy[1])

                    if self.player_rect.colliderect(enemy[1]):
                        self.lives -= 1
                        if self.lives <= 0:
                            playing = False
                            loss_text = self.FONT.render("YOU LOST! TRY AGAIN!", True, self.COLOR_BLUE)
                            self.main_display.blit(loss_text, (self.WIDTH // 2 - loss_text.get_width() // 2, self.HEIGHT // 2 - loss_text.get_height() // 2))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            break
                        else:
                            lives_text = self.FONT.render(f"Lost a life! Lives left: {self.lives}", True, self.COLOR_RED)
                            self.main_display.blit(lives_text, (self.WIDTH // 2 - lives_text.get_width() // 2, self.HEIGHT // 2 - lives_text.get_height() // 2))
                            pygame.display.flip()
                            pygame.time.delay(1000)
                        self.enemies.remove(enemy)

                for bonus in self.bonuses:
                    bonus[1] = bonus[1].move(bonus[2])
                    self.main_display.blit(bonus[0], bonus[1])

                    if self.player_rect.colliderect(bonus[1]):
                        self.score += 1
                        self.bonuses.pop(self.bonuses.index(bonus))

                self.main_display.blit(self.FONT.render(str(self.score), True, self.COLOR_BLACK), (self.WIDTH-50, 20))
                self.main_display.blit(self.player, self.player_rect)

            pygame.display.flip()

            for enemy in self.enemies:
                if enemy[1].right < 0:
                    self.enemies.pop(self.enemies.index(enemy))

            for bonus in self.bonuses:
                if bonus[1].top > self.HEIGHT:
                    self.bonuses.pop(self.bonuses.index(bonus))

            if paused:
                paused_text = self.FONT.render("PAUSE (Press p to resume!)", True, self.COLOR_BLACK)
                self.main_display.blit(paused_text, (self.WIDTH // 2 - paused_text.get_width() // 2, self.HEIGHT // 2 - paused_text.get_height() // 2))

            if self.score >= self.max_score or self.lives <= 0:

                self.is_game_over = True
    def reset_game(self):
        self.enemies = []
        self.bonuses = []
        self.score = 0
        self.lives = 3
        self.player_rect = self.player.get_rect()
        self.player_rect_center = self.main_display.get_rect().center
        self.waiting_for_start = True
        self.waiting_for_end = True 
        self.show_start_screen()
        



    def show_end_screen(self):
        self.start_screen.blit(self.start_bg, (0, 0))
        end_text = self.FONT.render("THE END! TO TRY AGAIN - a, TO LEAVE - esc. SEE YOU NEXT TIME!", True, self.COLOR_BLACK)  
        self.main_display.blit(end_text, (self.WIDTH // 2 - end_text.get_width() // 2, self.HEIGHT // 2 - end_text.get_height() // 2))
        pygame.display.flip()

        while self.waiting_for_end:
            for event in pygame.event.get():
                pygame.event.pump()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_a:
                        self.waiting_for_end = False
                        self.run()
        
   

    def start_game(self):
        self.show_start_screen()
        self.main_game_loop()
        self.show_end_screen()  
        
    def run(self):
        while True:
            self.reset_game()
            start_new_game = self.start_game()  
            self.show_end_screen()
            if not start_new_game:
                break  

if __name__ == "__main__":
    game = Game()
    game.run()
    
