import pygame
import random
import sys
import os
from pygame import gfxdraw

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Runner")


GROUND_HEIGHT = HEIGHT - 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BABY_BLUE_TOP = (173, 216, 230)
BABY_BLUE_BOTTOM = (135, 206, 250)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 223, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = -10
FPS = 60

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
SHOP = 3
ARENA_SELECT = 4

# load sounds 
def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        class DummySound:
            def play(self): pass
        return DummySound()

try:
    jump_sound = load_sound("jump.wav")
    coin_sound = load_sound("coin.wav")
    lose_sound = load_sound("lose.wav")
    high_score_sound = load_sound("high_score.wav")
    background_music = load_sound("background.wav")
    background_music.play(-1)  # Loop background music
except:
    pass

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
shop_title_font = pygame.font.Font(None, 48)


# loading
def load_data():
    try:
        with open("gamedata.txt", "r") as file:
            data = file.read().split(',')
            highscore = int(data[0])
            coins = int(data[1])
            owned_characters = set(data[2:])
            if "default" not in owned_characters:
                owned_characters.add("default")
            return highscore, coins, owned_characters
    except (FileNotFoundError, IndexError, ValueError):
        return 0, 0, {"default"}

def save_data(highscore, coins, owned_characters):
    with open("gamedata.txt", "w") as file:
        owned_string = ",".join(owned_characters)
        file.write(f"{highscore},{coins},{owned_string}")

highscore, total_coins, owned_characters = load_data()

# Cartoon Character Class
class CartoonCharacter:
    def __init__(self, x=100, y=GROUND_HEIGHT - 40):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.velocity_y = 0
        self.on_ground = True
        self.jump_count = 0
        self.max_jumps = 2
        self.character_type = "default"
        self.run_animation_frame = 0
        self.run_animation_speed = 0.2
        self.shield_active = False
        self.shield_timer = 0
        self.double_jump = False
        
    def reset(self):
        self.x = 100 
        self.y = GROUND_HEIGHT - 40
        self.velocity_y = 0
        self.on_ground = True
        self.jump_count = 0
        self.run_animation_frame = 0
        self.shield_active = False
        self.shield_timer = 0
        self.double_jump = False
        
    def jump(self):
        if self.character_type == "alien":
            self.velocity_y = JUMP_STRENGTH * 0.7
        elif self.character_type == "superhero" and not self.on_ground and self.double_jump:
            self.velocity_y = JUMP_STRENGTH * 1.2
            self.double_jump = False
            jump_sound.play()
        elif self.jump_count < self.max_jumps:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.jump_count += 1
            jump_sound.play()
    
    def update(self):
        if self.character_type == "alien":
            self.velocity_y += GRAVITY * 0.3
        else:
            self.velocity_y += GRAVITY
            
        self.y += self.velocity_y
        
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True
            self.jump_count = 0
            if self.character_type == "superhero":
                self.double_jump = True
                
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        if self.on_ground:
            self.run_animation_frame = (self.run_animation_frame + self.run_animation_speed) % 4
    
    def draw(self, screen):
        if self.character_type == "default":
            self.draw_default_character(screen)
        elif self.character_type == "ninja":
            self.draw_ninja_character(screen)
        elif self.character_type == "robot":
            self.draw_robot_character(screen)
        elif self.character_type == "alien":
            self.draw_alien_character(screen)
        elif self.character_type == "superhero":
            self.draw_superhero_character(screen)
        elif self.character_type == "flash":
            self.draw_flash_character(screen)
        elif self.character_type == "wizard":
            self.draw_wizard_character(screen)
        elif self.character_type == "spy":
            self.draw_spy_character(screen)
        elif self.character_type == "pirate":
            self.draw_pirate_character(screen)
        elif self.character_type == "zombie":
            self.draw_zombie_character(screen)
            
        # Draw shield if active
        if self.shield_active:
            pygame.draw.circle(screen, (100, 200, 255, 100), 
                             (self.x + self.width//2, self.y + self.height//2), 
                             self.width + 15, 2)
    
    def draw_default_character(self, screen):
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)
        
        # Body
        pygame.draw.rect(screen, (65, 105, 225), (self.x - 10, self.y - 15, 20, 25))
        
        # Legs (animated running)
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, BLACK, (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 3)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 10), (self.x, self.y + 30), 3)
        elif leg_frame == 1:
            pygame.draw.line(screen, BLACK, (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 3)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 3)
        elif leg_frame == 2:
            pygame.draw.line(screen, BLACK, (self.x - 5, self.y + 10), (self.x, self.y + 30), 3)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 3)
        else:
            pygame.draw.line(screen, BLACK, (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 3)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 3)
        
        # Arms
        pygame.draw.line(screen, BLACK, (self.x - 10, self.y - 5), (self.x - 20, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x + 10, self.y - 5), (self.x + 20, self.y), 3)
        
        # Eyes
        pygame.draw.circle(screen, WHITE, (self.x - 5, self.y - 28), 3)
        pygame.draw.circle(screen, WHITE, (self.x + 5, self.y - 28), 3)
        pygame.draw.circle(screen, BLACK, (self.x - 5, self.y - 28), 1)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y - 28), 1)
        
        # Smile
        pygame.draw.arc(screen, BLACK, (self.x - 8, self.y - 22, 16, 10), 0.2, 2.9, 2)
    
    def draw_ninja_character(self, screen):
        # Head (with mask)
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y - 25), 12)
        
        # Body
        pygame.draw.rect(screen, (30, 30, 30), (self.x - 10, self.y - 15, 20, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Eyes
        pygame.draw.rect(screen, (200, 0, 0), (self.x - 8, self.y - 30, 16, 4))
        
        # Sword on back
        pygame.draw.line(screen, (150, 150, 150), (self.x + 15, self.y - 10), (self.x + 15, self.y + 5), 3)
    
    def draw_robot_character(self, screen):
        # Head
        pygame.draw.rect(screen, (200, 200, 200), (self.x - 10, self.y - 35, 20, 15))
        
        # Body
        pygame.draw.rect(screen, (150, 150, 150), (self.x - 12, self.y - 15, 24, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 12, self.y + 10, 8, 20))
            pygame.draw.rect(screen, (100, 100, 100), (self.x + 4, self.y + 10, 8, 20))
        elif leg_frame == 1:
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 15, self.y + 10, 8, 15))
            pygame.draw.rect(screen, (100, 100, 100), (self.x + 4, self.y + 10, 8, 20))
        elif leg_frame == 2:
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 12, self.y + 10, 8, 20))
            pygame.draw.rect(screen, (100, 100, 100), (self.x + 7, self.y + 10, 8, 20))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 12, self.y + 10, 8, 20))
            pygame.draw.rect(screen, (100, 100, 100), (self.x + 4, self.y + 10, 8, 15))
        
        # Arms
        pygame.draw.rect(screen, (120, 120, 120), (self.x - 20, self.y - 10, 8, 20))
        pygame.draw.rect(screen, (120, 120, 120), (self.x + 12, self.y - 10, 8, 20))
        
        # Eyes
        pygame.draw.rect(screen, (0, 200, 200), (self.x - 6, self.y - 30, 4, 4))
        pygame.draw.rect(screen, (0, 200, 200), (self.x + 2, self.y - 30, 4, 4))
    
    def draw_alien_character(self, screen):
        # Head
        pygame.draw.ellipse(screen, (0, 200, 0), (self.x - 12, self.y - 35, 24, 30))
        
        # Body
        pygame.draw.rect(screen, (0, 180, 0), (self.x - 10, self.y - 15, 20, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (0, 160, 0), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (0, 160, 0), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (0, 160, 0), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (0, 160, 0), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (0, 160, 0), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (0, 160, 0), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (0, 160, 0), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (0, 160, 0), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Eyes
        pygame.draw.circle(screen, (255, 0, 0), (self.x - 5, self.y - 28), 4)
        pygame.draw.circle(screen, (255, 0, 0), (self.x + 5, self.y - 28), 4)
        pygame.draw.circle(screen, BLACK, (self.x - 5, self.y - 28), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y - 28), 2)
        
        # Antenna
        pygame.draw.line(screen, (0, 200, 0), (self.x - 8, self.y - 35), (self.x - 15, self.y - 50), 2)
        pygame.draw.line(screen, (0, 200, 0), (self.x + 8, self.y - 35), (self.x + 15, self.y - 50), 2)
        pygame.draw.circle(screen, (255, 0, 0), (self.x - 15, self.y - 50), 3)
        pygame.draw.circle(screen, (255, 0, 0), (self.x + 15, self.y - 50), 3)
    
    def draw_superhero_character(self, screen):
        # Cape
        pygame.draw.polygon(screen, (200, 0, 0), 
                          [(self.x - 15, self.y - 10), (self.x - 20, self.y + 20), 
                           (self.x, self.y + 10), (self.x + 20, self.y + 20), 
                           (self.x + 15, self.y - 10)])
        
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)
        
        # Body
        pygame.draw.rect(screen, (0, 0, 200), (self.x - 10, self.y - 15, 20, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (0, 0, 150), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (0, 0, 150), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (0, 0, 150), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (0, 0, 150), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (0, 0, 150), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (0, 0, 150), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (0, 0, 150), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (0, 0, 150), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Mask
        pygame.draw.rect(screen, (0, 0, 150), (self.x - 12, self.y - 35, 24, 15))
        pygame.draw.circle(screen, (0, 0, 150), (self.x, self.y - 20), 12)
        
        # Eyes
        pygame.draw.circle(screen, WHITE, (self.x - 5, self.y - 28), 4)
        pygame.draw.circle(screen, WHITE, (self.x + 5, self.y - 28), 4)
    
    def draw_flash_character(self, screen):
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)
        
        # Body
        pygame.draw.rect(screen, (200, 0, 0), (self.x - 10, self.y - 15, 20, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (150, 0, 0), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (150, 0, 0), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (150, 0, 0), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (150, 0, 0), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (150, 0, 0), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (150, 0, 0), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (150, 0, 0), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (150, 0, 0), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Lightning bolt symbol
        pygame.draw.polygon(screen, YELLOW, 
                          [(self.x, self.y - 10), (self.x - 5, self.y - 5), 
                           (self.x + 5, self.y + 5), (self.x, self.y), 
                           (self.x + 5, self.y - 5), (self.x - 5, self.y + 5)])
    
    def draw_wizard_character(self, screen):
        # Hat
        pygame.draw.polygon(screen, (100, 0, 100), 
                          [(self.x - 15, self.y - 25), (self.x + 15, self.y - 25), 
                           (self.x, self.y - 50)])
        
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)
        
        # Robe
        pygame.draw.rect(screen, (70, 0, 70), (self.x - 12, self.y - 15, 24, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (50, 0, 50), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (50, 0, 50), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (50, 0, 50), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (50, 0, 50), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (50, 0, 50), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (50, 0, 50), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (50, 0, 50), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (50, 0, 50), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Staff
        pygame.draw.line(screen, BROWN, (self.x + 20, self.y - 40), (self.x + 20, self.y + 20), 3)
        pygame.draw.circle(screen, (200, 200, 0), (self.x + 20, self.y - 40), 8)
        
        # Beard
        pygame.draw.arc(screen, (150, 150, 150), (self.x - 10, self.y - 15, 20, 20), 0, 3.14, 2)
    
    def draw_spy_character(self, screen):
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)
        
        # Sunglasses
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 12, self.y - 28, 24, 8))
        pygame.draw.line(screen, (100, 100, 100), (self.x - 5, self.y - 28), (self.x + 5, self.y - 28), 2)
        
        # Trench coat
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 15, self.y - 15, 30, 25))
        
        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame == 0:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 15, self.y + 25), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 5, self.y + 30), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (20, 20, 20), (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, (20, 20, 20), (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)
        
        # Briefcase
        pygame.draw.rect(screen, (50, 50, 50), (self.x + 15, self.y, 15, 10))
        pygame.draw.line(screen, (70, 70, 70), (self.x + 15, self.y + 2), (self.x + 30, self.y + 2), 1)

    def draw_pirate_character(self, screen):
        # Head
        pygame.draw.circle(screen, (255, 218, 185), (self.x, self.y - 25), 12)

        # Pirate Hat
        pygame.draw.rect(screen, BLACK, (self.x - 15, self.y - 40, 30, 8))
        pygame.draw.rect(screen, BLACK, (self.x - 8, self.y - 45, 16, 10))

        # Eyepatch
        pygame.draw.rect(screen, BLACK, (self.x + 2, self.y - 30, 8, 6))
        pygame.draw.line(screen, BLACK, (self.x - 10, self.y-35), (self.x + 10, self.y-25), 1)

        # Body (Vest)
        pygame.draw.rect(screen, (139, 0, 0), (self.x - 10, self.y - 15, 20, 25)) # Red vest
        pygame.draw.rect(screen, WHITE, (self.x - 5, self.y - 15, 10, 20)) # White shirt

        # Legs
        leg_frame = int(self.run_animation_frame)
        if leg_frame % 2 == 0:
            pygame.draw.line(screen, (50, 50, 50), (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, (50, 50, 50), (self.x + 5, self.y + 10), (self.x, self.y + 30), 4)
        else:
            pygame.draw.line(screen, (50, 50, 50), (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, (50, 50, 50), (self.x + 5, self.y + 10), (self.x + 10, self.y + 30), 4)
        
        # Cutlass at side
        pygame.draw.line(screen, (100,100,100), (self.x + 15, self.y - 5), (self.x + 25, self.y + 10), 3)
        pygame.draw.rect(screen, BROWN, (self.x + 12, self.y - 8, 5, 5))

    def draw_zombie_character(self, screen):
        # Head (Greenish skin)
        pygame.draw.circle(screen, (150, 200, 150), (self.x, self.y - 25), 12)

        # Eyes (dull)
        pygame.draw.circle(screen, WHITE, (self.x - 5, self.y - 28), 3)
        pygame.draw.circle(screen, WHITE, (self.x + 5, self.y - 28), 3)

        # Body (tattered clothes)
        pygame.draw.rect(screen, (101, 67, 33), (self.x - 10, self.y - 15, 20, 25)) # Brown shirt
        pygame.draw.polygon(screen, (101, 67, 33), [(self.x - 10, self.y + 10), (self.x - 12, self.y + 15), (self.x-5, self.y+10)]) # Jagged edge

        # Legs (tattered pants)
        leg_frame = int(self.run_animation_frame)
        zombie_blue = (0, 50, 100)
        # Shambling animation
        if leg_frame == 0:
            pygame.draw.line(screen, zombie_blue, (self.x - 5, self.y + 10), (self.x - 10, self.y + 30), 4)
            pygame.draw.line(screen, zombie_blue, (self.x + 5, self.y + 10), (self.x, self.y + 25), 4)
        elif leg_frame == 1:
            pygame.draw.line(screen, zombie_blue, (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, zombie_blue, (self.x + 5, self.y + 10), (self.x + 5, self.y + 25), 4)
        elif leg_frame == 2:
            pygame.draw.line(screen, zombie_blue, (self.x - 5, self.y + 10), (self.x, self.y + 30), 4)
            pygame.draw.line(screen, zombie_blue, (self.x + 5, self.y + 10), (self.x + 10, self.y + 25), 4)
        else:
            pygame.draw.line(screen, zombie_blue, (self.x - 5, self.y + 10), (self.x - 5, self.y + 30), 4)
            pygame.draw.line(screen, zombie_blue, (self.x + 5, self.y + 10), (self.x + 15, self.y + 25), 4)

        # Arms
        pygame.draw.line(screen, (150, 200, 150), (self.x - 10, self.y - 5), (self.x - 20, self.y), 3)
        pygame.draw.line(screen, (150, 200, 150), (self.x + 10, self.y - 5), (self.x + 20, self.y), 3)


#  city-themed obstacles class
class Obstacle:
    def __init__(self, last_obstacle_time, arena_type="giza"):
        self.width = random.randint(25, 45)
        self.height = random.randint(35, 55)
        self.x = WIDTH
        self.y = GROUND_HEIGHT - self.height
        self.type = random.choice(["car", "trashcan", "bench", "box", "cone", "barrier"])
        self.passed = False
        self.arena_type = arena_type

        if random.random() < 0.3 and self.height > 40:  
            self.y -= random.randint(10, 20)
    
    def update(self):
        self.x -= SPEED
    
    def draw(self, screen):
        if self.arena_type == "giza":
            self.draw_giza_obstacle(screen)
        elif self.arena_type == "london":
            self.draw_london_obstacle(screen)
        elif self.arena_type == "paris":
            self.draw_paris_obstacle(screen)
        elif self.arena_type == "rome":
            self.draw_rome_obstacle(screen)
        elif self.arena_type == "newyork":
            self.draw_newyork_obstacle(screen)
    
    def draw_giza_obstacle(self, screen):
        if self.type == "car":
            # Draw taxi
            pygame.draw.rect(screen, (200, 200, 0), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 5, self.width - 10, 10))
            # Windows
            pygame.draw.rect(screen, (150, 200, 255), (self.x + 5, self.y + 15, 10, 10))
            pygame.draw.rect(screen, (150, 200, 255), (self.x + self.width - 15, self.y + 15, 10, 10))
            # Wheels
            pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + self.height - 5), 5)
            pygame.draw.circle(screen, BLACK, (self.x + self.width - 10, self.y + self.height - 5), 5)
        elif self.type == "trashcan":
            # Draw trash can
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (150, 150, 150), (self.x + 2, self.y + 2, self.width - 4, 5))
            # Lid
            pygame.draw.ellipse(screen, (80, 80, 80), (self.x, self.y - 5, self.width, 10))
        elif self.type == "bench":
            # Draw bench
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, 10))
            # Legs
            pygame.draw.rect(screen, BROWN, (self.x, self.y + 10, 5, 20))
            pygame.draw.rect(screen, BROWN, (self.x + self.width - 5, self.y + 10, 5, 20))
        else:  # cone
            # Draw traffic cone
            pygame.draw.polygon(screen, ORANGE, 
                              [(self.x + self.width//2, self.y), 
                               (self.x, self.y + self.height), 
                               (self.x + self.width, self.y + self.height)])
            pygame.draw.lines(screen, WHITE, False, 
                            [(self.x + self.width//2, self.y + 5), 
                             (self.x + 5, self.y + self.height - 5), 
                             (self.x + self.width - 5, self.y + self.height - 5)], 2)
    
    def draw_london_obstacle(self, screen):
        if self.type == "car":
            # Draw black cab
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
            # Windows
            pygame.draw.rect(screen, (150, 200, 255), (self.x + 5, self.y + 5, 10, 10))
            pygame.draw.rect(screen, (150, 200, 255), (self.x + self.width - 15, self.y + 5, 10, 10))
            # Wheels
            pygame.draw.circle(screen, (50, 50, 50), (self.x + 10, self.y + self.height - 5), 5)
            pygame.draw.circle(screen, (50, 50, 50), (self.x + self.width - 10, self.y + self.height - 5), 5)
        elif self.type == "trashcan":
            # Draw UK-style trash can
            pygame.draw.rect(screen, (0, 100, 0), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (0, 150, 0), (self.x + 2, self.y + 2, self.width - 4, 5))
        elif self.type == "bench":
            # Draw park bench
            pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, 10))
            # Back
            pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y - 20, 5, 20))
            pygame.draw.rect(screen, (139, 69, 19), (self.x + self.width - 5, self.y - 20, 5, 20))
            pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y - 20, self.width, 5))
        else:  # barrier
            # Draw police barrier
            pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, 15))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, 5))
            pygame.draw.rect(screen, WHITE, (self.x, self.y + 10, self.width, 5))
    
    def draw_paris_obstacle(self, screen):
        if self.type == "car":
            # Draw small European car
            pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))
            # Windows
            pygame.draw.rect(screen, (150, 200, 255), (self.x + 5, self.y + 5, 10, 10))
            pygame.draw.rect(screen, (150, 200, 255), (self.x + self.width - 15, self.y + 5, 10, 10))
            # Wheels
            pygame.draw.circle(screen, (50, 50, 50), (self.x + 10, self.y + self.height - 5), 5)
            pygame.draw.circle(screen, (50, 50, 50), (self.x + self.width - 10, self.y + self.height - 5), 5)
        elif self.type == "trashcan":
            # Draw Parisian trash can
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, self.height))
            # Green top
            pygame.draw.rect(screen, (0, 100, 0), (self.x, self.y, self.width, 5))
        elif self.type == "bench":
            # Draw ornate bench
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, 10))
            # Ornate legs
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y + 10, 5, 20))
            pygame.draw.rect(screen, (150, 150, 150), (self.x + self.width - 5, self.y + 10, 5, 20))
            # Decorative elements
            pygame.draw.circle(screen, (200, 200, 200), (self.x + self.width//2, self.y + 5), 3)
        else:  # cafe table
            # Draw small cafe table
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, 5))
            # Leg
            pygame.draw.rect(screen, BROWN, (self.x + self.width//2 - 2, self.y + 5, 4, 20))
    
    def draw_rome_obstacle(self, screen):
        if self.type == "car":
            # Draw small Italian car
            pygame.draw.rect(screen, (0, 0, 200), (self.x, self.y, self.width, self.height))
            # Windows
            pygame.draw.rect(screen, (150, 200, 255), (self.x + 5, self.y + 5, 10, 10))
            pygame.draw.rect(screen, (150, 200, 255), (self.x + self.width - 15, self.y + 5, 10, 10))
            # Wheels
            pygame.draw.circle(screen, (50, 50, 50), (self.x + 10, self.y + self.height - 5), 5)
            pygame.draw.circle(screen, (50, 50, 50), (self.x + self.width - 10, self.y + self.height - 5), 5)
        elif self.type == "trashcan":
            # Draw Roman trash can
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
            # Decorative stripes
            pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, 3))
            pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y + self.height - 3, self.width, 3))
        elif self.type == "bench":
            # Draw stone bench
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, 15))
            # Carved details
            pygame.draw.line(screen, (100, 100, 100), (self.x + 5, self.y + 5, self.x + self.width - 5, self.y + 5), 2)
        else:  # column
            # Draw broken column piece
            pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))
            # Carved lines
            for i in range(3):
                pygame.draw.line(screen, (150, 150, 150), 
                               (self.x, self.y + 5 + i*10), 
                               (self.x + self.width, self.y + 5 + i*10), 2)
    
    def draw_newyork_obstacle(self, screen):
        if self.type == "car":
            # Draw yellow taxi
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 5, self.width - 10, 10))
            # Windows
            pygame.draw.rect(screen, (150, 200, 255), (self.x + 5, self.y + 15, 10, 10))
            pygame.draw.rect(screen, (150, 200, 255), (self.x + self.width - 15, self.y + 15, 10, 10))
            # Wheels
            pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + self.height - 5), 5)
            pygame.draw.circle(screen, BLACK, (self.x + self.width - 10, self.y + self.height - 5), 5)
        elif self.type == "trashcan":
            # Draw NYC trash can
            pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
            # Green lid
            pygame.draw.rect(screen, (0, 100, 0), (self.x, self.y, self.width, 5))
        elif self.type == "bench":
            # Draw park bench
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, 10))
            # Legs
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y + 10, 5, 20))
            pygame.draw.rect(screen, (150, 150, 150), (self.x + self.width - 5, self.y + 10, 5, 20))
        else:  # hydrant
            # Draw fire hydrant
            pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, 15, 25))
            # Top
            pygame.draw.rect(screen, (150, 150, 150), (self.x - 5, self.y, 25, 5))
    
    def off_screen(self):
        return self.x + self.width < 0
    
    def collide(self, character):
        if character.shield_active:
            return False
            
        return (self.x < character.x + character.width and 
                self.x + self.width > character.x and
                self.y < character.y + character.height and 
                self.y + self.height > character.y)

# Coin Class
class Coin:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(100, GROUND_HEIGHT - 30)
        self.width = 15
        self.height = 15
        self.collected = False
        self.animation_frame = 0
        self.animation_speed = 0.2
        
    def update(self):
        self.x -= SPEED
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 8:  
            self.animation_frame = 0
    
    def draw(self, screen):
        if self.collected:
            return
            
        frame = int(self.animation_frame)
        if frame < 4:
            pygame.draw.ellipse(screen, GOLD, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.circle(screen, GOLD, (self.x + self.width//2, self.y + self.height//2), self.width//2)

        pygame.draw.ellipse(screen, YELLOW, (self.x + 3, self.y + 3, 5, 5))
    
    def off_screen(self):
        return self.x + self.width < 0
    
    def collide(self, character):
        if self.collected:
            return False
            
        if character.character_type == "ninja" and random.random() < 0.1:        
            character.shield_active = True
            character.shield_timer = 180   
            
        return (self.x < character.x + character.width and 
                self.x + self.width > character.x and
                self.y < character.y + character.height and 
                self.y + self.height > character.y)

#  Class decoration
class Cloud:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(50, 150)
        self.width = random.randint(50, 100)
        self.speed = random.uniform(1, 3)
    
    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.width, 30))
        pygame.draw.ellipse(screen, WHITE, (self.x + 20, self.y - 15, self.width - 20, 40))
    
    def off_screen(self):
        return self.x + self.width < 0

def draw_flag(nation):
    flag_w, flag_h = 90, 60
    flag_x, flag_y = WIDTH - flag_w - 20, 20
    
    if nation == "egypt":
        # Red, White, Black horizontal stripes
        pygame.draw.rect(screen, (206, 17, 38), (flag_x, flag_y, flag_w, flag_h//3))
        pygame.draw.rect(screen, WHITE, (flag_x, flag_y + flag_h//3, flag_w, flag_h//3))
        pygame.draw.rect(screen, BLACK, (flag_x, flag_y + 2*flag_h//3, flag_w, flag_h//3))
        # Simplified Eagle of Saladin
        pygame.draw.circle(screen, (192, 147, 0), (int(flag_x + flag_w/2), int(flag_y + flag_h/2)), 5)
    
    elif nation == "uk":
        # Blue field
        pygame.draw.rect(screen, (1, 33, 105), (flag_x, flag_y, flag_w, flag_h))
        # White diagonals (St. Andrew's Saltire)
        pygame.draw.line(screen, WHITE, (flag_x, flag_y), (flag_x + flag_w, flag_y + flag_h), 12)
        pygame.draw.line(screen, WHITE, (flag_x, flag_y + flag_h), (flag_x + flag_w, flag_y), 12)
        # Red diagonals (St. Patrick's Saltire)
        pygame.draw.line(screen, (206, 17, 38), (flag_x, flag_y), (flag_x + flag_w, flag_y + flag_h), 6)
        pygame.draw.line(screen, (206, 17, 38), (flag_x, flag_y + flag_h), (flag_x + flag_w, flag_y), 6)
        # White cross
        pygame.draw.rect(screen, WHITE, (flag_x, flag_y + flag_h//2 - 10, flag_w, 20))
        pygame.draw.rect(screen, WHITE, (flag_x + flag_w//2 - 10, flag_y, 20, flag_h))
        # Red cross (St. George's Cross)
        pygame.draw.rect(screen, (206, 17, 38), (flag_x, flag_y + flag_h//2 - 5, flag_w, 10))
        pygame.draw.rect(screen, (206, 17, 38), (flag_x + flag_w//2 - 5, flag_y, 10, flag_h))

    elif nation == "france":
        # Blue, White, Red vertical stripes
        pygame.draw.rect(screen, (0, 85, 164), (flag_x, flag_y, flag_w//3, flag_h))
        pygame.draw.rect(screen, WHITE, (flag_x + flag_w//3, flag_y, flag_w//3, flag_h))
        pygame.draw.rect(screen, (239, 65, 53), (flag_x + 2*flag_w//3, flag_y, flag_w//3, flag_h))

    elif nation == "italy":
        # Green, White, Red vertical stripes
        pygame.draw.rect(screen, (0, 146, 70), (flag_x, flag_y, flag_w//3, flag_h))
        pygame.draw.rect(screen, WHITE, (flag_x + flag_w//3, flag_y, flag_w//3, flag_h))
        pygame.draw.rect(screen, (206, 43, 55), (flag_x + 2*flag_w//3, flag_y, flag_w//3, flag_h))

    elif nation == "usa":
        # Red and white stripes
        stripe_h = flag_h / 13
        for i in range(13):
            color = (210, 16, 52) if i % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (flag_x, flag_y + i * stripe_h, flag_w, stripe_h))
        # Blue canton
        pygame.draw.rect(screen, (60, 59, 110), (flag_x, flag_y, flag_w * 2//5, flag_h * 7//13))
        # Simplified stars
        for i in range(3):
            for j in range(3):
                pygame.draw.circle(screen, WHITE, (flag_x + 10 + i*10, flag_y + 8 + j * 8), 1)

# Function to draw different city backgrounds
def draw_background(arena_type="giza"):
    if arena_type == "giza":
        draw_giza_background()
    elif arena_type == "london":
        draw_london_background()
    elif arena_type == "paris":
        draw_paris_background()
    elif arena_type == "rome":
        draw_rome_background()
    elif arena_type == "newyork":
        draw_newyork_background()

def draw_giza_background():
    # Sky gradient
    for y in range(HEIGHT):
        color = (
            int(BABY_BLUE_TOP[0] * (1 - y / HEIGHT) + BABY_BLUE_BOTTOM[0] * (y / HEIGHT)),
            int(BABY_BLUE_TOP[1] * (1 - y / HEIGHT) + BABY_BLUE_BOTTOM[1] * (y / HEIGHT)),
            int(BABY_BLUE_TOP[2] * (1 - y / HEIGHT) + BABY_BLUE_BOTTOM[2] * (y / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    draw_flag("egypt")
    
    # Sun
    pygame.draw.circle(screen, YELLOW, (WIDTH - 180, 80), 40)
    
    # Pyramids in distance
    pygame.draw.polygon(screen, (218, 165, 32), [(50, GROUND_HEIGHT), (200, GROUND_HEIGHT - 200), (350, GROUND_HEIGHT)])
    pygame.draw.polygon(screen, (184, 134, 11), [(250, GROUND_HEIGHT), (400, GROUND_HEIGHT - 220), (550, GROUND_HEIGHT)])
    pygame.draw.polygon(screen, (218, 165, 32), [(450, GROUND_HEIGHT), (550, GROUND_HEIGHT - 150), (650, GROUND_HEIGHT)])

    
    # Ground (sand)
    pygame.draw.rect(screen, (194, 178, 128), (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
    
    # Sphinx
    pygame.draw.rect(screen, (184, 134, 11), (WIDTH - 200, GROUND_HEIGHT - 50, 100, 50))
    pygame.draw.circle(screen, (184, 134, 11), (WIDTH - 200, GROUND_HEIGHT - 25), 25)

def draw_london_background():
    # Overcast sky gradient
    sky_top = (170, 180, 190)
    sky_bottom = (200, 210, 220)
    for y in range(HEIGHT):
        color = (
            int(sky_top[0] * (1 - y / HEIGHT) + sky_bottom[0] * (y / HEIGHT)),
            int(sky_top[1] * (1 - y / HEIGHT) + sky_bottom[1] * (y / HEIGHT)),
            int(sky_top[2] * (1 - y / HEIGHT) + sky_bottom[2] * (y / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    draw_flag("uk")

    # The Shard Silhouette
    shard_color = (100, 105, 110)
    pygame.draw.polygon(screen, shard_color, [(WIDTH-250, GROUND_HEIGHT), (WIDTH-220, GROUND_HEIGHT-300), (WIDTH-190, GROUND_HEIGHT)])
    
    # Big Ben in distance
    pygame.draw.rect(screen, (150, 150, 100), (WIDTH - 450, GROUND_HEIGHT - 200, 40, 200))
    pygame.draw.rect(screen, (200, 200, 150), (WIDTH - 450, GROUND_HEIGHT - 220, 40, 20))
    
    # Tower Bridge
    bridge_color = (160, 140, 120)
    pygame.draw.rect(screen, bridge_color, (100, GROUND_HEIGHT - 150, 60, 150))
    pygame.draw.rect(screen, bridge_color, (240, GROUND_HEIGHT - 150, 60, 150))
    pygame.draw.rect(screen, bridge_color, (100, GROUND_HEIGHT - 180, 200, 30))
    
    # Double-decker bus decoration
    pygame.draw.rect(screen, (200,0,0), (WIDTH - 600, GROUND_HEIGHT - 40, 80, 40))
    pygame.draw.rect(screen, (150,0,0), (WIDTH - 600, GROUND_HEIGHT - 25, 80, 15))

    # Ground (street)
    pygame.draw.rect(screen, (100, 100, 100), (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
    pygame.draw.line(screen, YELLOW, (0, GROUND_HEIGHT + 20), (WIDTH, GROUND_HEIGHT + 20), 2)

def draw_paris_background():
    # Dusky sky gradient
    sky_top = (70, 80, 120)
    sky_bottom = (230, 140, 160)
    for y in range(HEIGHT):
        color = (
            int(sky_top[0] * (1 - y / HEIGHT) + sky_bottom[0] * (y / HEIGHT)),
            int(sky_top[1] * (1 - y / HEIGHT) + sky_bottom[1] * (y / HEIGHT)),
            int(sky_top[2] * (1 - y / HEIGHT) + sky_bottom[2] * (y / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    draw_flag("france")

    # Notre Dame
    cathedral_color = (60, 60, 80)
    pygame.draw.rect(screen, cathedral_color, (100, GROUND_HEIGHT - 180, 80, 180))
    pygame.draw.rect(screen, cathedral_color, (110, GROUND_HEIGHT - 220, 20, 40))
    pygame.draw.rect(screen, cathedral_color, (150, GROUND_HEIGHT - 220, 20, 40))
    
    # Eiffel Tower in distance
    eiffel_color = (50, 50, 70)
    pygame.draw.rect(screen, eiffel_color, (WIDTH - 150, GROUND_HEIGHT - 250, 10, 250))
    pygame.draw.polygon(screen, eiffel_color, [(WIDTH - 170, GROUND_HEIGHT - 50), (WIDTH - 145, GROUND_HEIGHT - 250), (WIDTH - 120, GROUND_HEIGHT - 50)])
    pygame.draw.rect(screen, eiffel_color, (WIDTH - 170, GROUND_HEIGHT - 150, 50, 10))
    
    # Louvre Museum
    louvre_color = (80, 80, 100)
    pygame.draw.rect(screen, louvre_color, (300, GROUND_HEIGHT - 120, 250, 120))

    # River Seine
    pygame.draw.rect(screen, (100, 120, 150), (0, GROUND_HEIGHT-20, WIDTH, 40))

    # Ground (street)
    pygame.draw.rect(screen, (60, 60, 60), (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))

def draw_rome_background():
    # Golden hour sky
    sky_top = (255, 180, 80)
    sky_bottom = (255, 120, 100)
    for y in range(HEIGHT):
        color = (
            int(sky_top[0] * (1 - y / HEIGHT) + sky_bottom[0] * (y / HEIGHT)),
            int(sky_top[1] * (1 - y / HEIGHT) + sky_bottom[1] * (y / HEIGHT)),
            int(sky_top[2] * (1 - y / HEIGHT) + sky_bottom[2] * (y / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    draw_flag("italy")
    
    # Pantheon Dome
    pantheon_color = (160, 150, 130)
    pygame.draw.ellipse(screen, pantheon_color, (100, GROUND_HEIGHT-150, 200, 150))
    pygame.draw.rect(screen, pantheon_color, (100, GROUND_HEIGHT-75, 200, 75))


    # Colosseum in distance
    colosseum_color = (180, 160, 140)
    pygame.draw.ellipse(screen, colosseum_color, (WIDTH - 300, GROUND_HEIGHT - 120, 180, 120))
    pygame.draw.ellipse(screen, (0,0,0,50), (WIDTH - 300, GROUND_HEIGHT - 120, 180, 120), 10)

    # Cypress Trees
    tree_color = (40, 80, 40)
    pygame.draw.polygon(screen, tree_color, [(WIDTH-450, GROUND_HEIGHT), (WIDTH-420, GROUND_HEIGHT-150), (WIDTH-390, GROUND_HEIGHT)])
    pygame.draw.polygon(screen, tree_color, [(WIDTH-520, GROUND_HEIGHT), (WIDTH-490, GROUND_HEIGHT-120), (WIDTH-460, GROUND_HEIGHT)])

    # Ground (cobblestone)
    pygame.draw.rect(screen, (110, 110, 110), (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
    for i in range(0, WIDTH, 20):
        for j in range(GROUND_HEIGHT, HEIGHT, 20):
            pygame.draw.rect(screen, (90,90,90), (i+random.randint(-2,2), j+random.randint(-2,2), 15, 15))


def draw_newyork_background():
    # Sky gradient (bright blue)
    for y in range(HEIGHT):
        color = (
            int(100 * (1 - y / HEIGHT) + 135 * (y / HEIGHT)),
            int(149 * (1 - y / HEIGHT) + 206 * (y / HEIGHT)),
            int(237 * (1 - y / HEIGHT) + 250 * (y / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    draw_flag("usa")
    
    # Skyscrapers
    pygame.draw.rect(screen, (100, 100, 100), (WIDTH - 200, GROUND_HEIGHT - 250, 40, 250))
    pygame.draw.rect(screen, (120, 120, 120), (WIDTH - 300, GROUND_HEIGHT - 300, 30, 300))
    pygame.draw.rect(screen, (80, 80, 80), (WIDTH - 400, GROUND_HEIGHT - 200, 25, 200))
    
    # Windows
    for i in range(5):
        for j in range(10):
            if random.random() > 0.3:  
                pygame.draw.rect(screen, YELLOW, (WIDTH - 195 + i*8, GROUND_HEIGHT - 240 + j*25, 5, 15))
                pygame.draw.rect(screen, YELLOW, (WIDTH - 295 + i*6, GROUND_HEIGHT - 290 + j*30, 4, 15))
                pygame.draw.rect(screen, YELLOW, (WIDTH - 395 + i*5, GROUND_HEIGHT - 190 + j*20, 4, 10))
    
    # Statue of Liberty
    pygame.draw.rect(screen, (50, 150, 50), (WIDTH - 500, GROUND_HEIGHT - 150, 20, 150))
    pygame.draw.circle(screen, (50, 150, 50), (WIDTH - 490, GROUND_HEIGHT - 160), 25)
    
    # Ground (street)
    pygame.draw.rect(screen, (50, 50, 50), (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
    pygame.draw.line(screen, WHITE, (0, GROUND_HEIGHT + 20), (WIDTH, GROUND_HEIGHT + 20), 2)

# Main Menu
def main_menu(total_coins):
    button_height = 50
    button_width = 300
    button_margin = 20
    button_y_start = HEIGHT // 2 - 100
    
    buttons = [
        {"text": "Start Game", "action": PLAYING, "y": button_y_start},
        {"text": "City Select", "action": ARENA_SELECT, "y": button_y_start + button_height + button_margin},
        {"text": "Character Shop", "action": SHOP, "y": button_y_start + 2*(button_height + button_margin)},
        {"text": "Quit Game", "action": "quit", "y": button_y_start + 3*(button_height + button_margin)}
    ]
    
    while True:
        screen.fill(WHITE)
        draw_background()
        
        title = font.render("CITY RUNNER", True, BLACK)
        controls = small_font.render("Controls: SPACE to Jump, P to Pause", True, BLACK)
        coins_text = small_font.render(f"Total Coins: {total_coins}", True, GOLD)
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 4 + 40))
        screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 4 + 70))
        
        # Draw buttons
        for button in buttons:
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
            pygame.draw.rect(screen, (200, 200, 200), button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 2)  # Border
            
            text = font.render(button["text"], True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button["y"] + button_height // 2 - text.get_height() // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        if button["action"] == "quit":
                            pygame.quit()
                            sys.exit()
                        return button["action"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return PLAYING
                elif event.key == pygame.K_s:
                    return SHOP
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# City Selection Screen
def arena_select_screen():
    cities = [
        {"name": "Giza", "type": "giza", "unlocked": True},
        {"name": "London", "type": "london", "unlocked": True},
        {"name": "Paris", "type": "paris", "unlocked": True},
        {"name": "Rome", "type": "rome", "unlocked": True},
        {"name": "New York", "type": "newyork", "unlocked": True}
    ]
    
    selected_index = 0
    button_height = 60
    button_width = 250
    button_margin = 20
    button_y_start = HEIGHT // 2 - 120
    
    while True:
        screen.fill(WHITE)
        # preview 
        draw_background(cities[selected_index]["type"])
        
        title = font.render("SELECT CITY", True, BLACK)
        back_text = font.render("Press B to Go Back", True, BLACK)
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))

        for i, city in enumerate(cities):
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button_y_start + i*(button_height + button_margin), button_width, button_height)
            
            if i == selected_index:
                pygame.draw.rect(screen, (200, 200, 0), button_rect)
            else:
                pygame.draw.rect(screen, (200, 200, 200, 180), button_rect)
            
            pygame.draw.rect(screen, BLACK, button_rect, 2)  
            
            text = font.render(city["name"], True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button_y_start + i*(button_height + button_margin) + button_height // 2 - text.get_height() // 2))
            
            if not city["unlocked"]:
                lock_text = small_font.render("LOCKED", True, (200, 0, 0))
                screen.blit(lock_text, (WIDTH // 2 - lock_text.get_width() // 2, button_y_start + i*(button_height + button_margin) + button_height - 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return MENU, "giza"  
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(cities)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(cities)
                elif event.key == pygame.K_RETURN:
                    selected_city = cities[selected_index]
                    if selected_city["unlocked"]:
                        return PLAYING, selected_city["type"]
    
    return MENU, "giza"

# Shop Screen with character preview
def shop_screen(total_coins, current_character, owned_characters):
    characters = [
        {"name": "Default", "type": "default", "cost": 0, "desc": "The basic runner."},
        {"name": "Ninja", "type": "ninja", "cost": 100, "desc": "Chance to gain a shield."},
        {"name": "Robot", "type": "robot", "cost": 200, "desc": "Heavy but strong."},
        {"name": "Alien", "type": "alien", "cost": 300, "desc": "Jumps with low gravity."},
        {"name": "Superhero", "type": "superhero", "cost": 400, "desc": "Can perform a double jump."},
        {"name": "Flash", "type": "flash", "cost": 500, "desc": "A very fast runner."},
        {"name": "Wizard", "type": "wizard", "cost": 600, "desc": "A magical runner."},
        {"name": "Spy", "type": "spy", "cost": 700, "desc": "A stealthy agent."},
        {"name": "Pirate", "type": "pirate", "cost": 800, "desc": "A swashbuckling adventurer."},
        {"name": "Zombie", "type": "zombie", "cost": 900, "desc": "A spooky, shambling runner."},
    ]

    selected_index = 0
    
    list_w, list_h = 400, 500
    list_x, list_y = 50, 150
    list_item_h = 50

    preview_x, preview_y = 650, 350
    preview_char = CartoonCharacter(x=preview_x, y=preview_y)
    preview_char.on_ground = False 

    while True:
        screen.fill(WHITE)
        draw_background() 
        
        title = shop_title_font.render("CHARACTER SHOP", True, BLACK)
        coins_text = font.render(f"Coins: {total_coins}", True, GOLD)
        back_text = font.render("Press B to Go Back", True, BLACK)
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, 80))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
        
        for i, char in enumerate(characters):
            button_rect = pygame.Rect(list_x, list_y + i * list_item_h, list_w, list_item_h)
            
            if i == selected_index:
                pygame.draw.rect(screen, (200, 200, 0), button_rect)
            else:
                pygame.draw.rect(screen, (200, 200, 200, 200), button_rect)
            
            pygame.draw.rect(screen, BLACK, button_rect, 2)
            
            name_text = font.render(char["name"], True, BLACK)
            screen.blit(name_text, (list_x + 15, list_y + i * list_item_h + 10))
        
        selected_char_data = characters[selected_index]
        preview_char.character_type = selected_char_data["type"]
        
        pedestal_w, pedestal_h = 150, 20
        pedestal_x, pedestal_y = preview_x - pedestal_w//2, preview_y + 20
        pygame.draw.ellipse(screen, (150,150,150), (pedestal_x, pedestal_y, pedestal_w, pedestal_h))
        
        preview_char.draw(screen)

        desc_text = small_font.render(selected_char_data["desc"], True, BLACK)
        screen.blit(desc_text, (preview_x - desc_text.get_width()//2, preview_y + 80))

        if selected_char_data["type"] in owned_characters:
            if selected_char_data["type"] == current_character:
                status_text = font.render("EQUIPPED", True, GREEN)
            else:
                status_text = font.render("OWNED", True, BLACK)
        else:
            status_text = font.render(f"Cost: {selected_char_data['cost']} coins", True, BLACK)
        
        screen.blit(status_text, (preview_x - status_text.get_width()//2, preview_y + 120))


        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return MENU, current_character, total_coins, owned_characters
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(characters)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    selected_char = characters[selected_index]
                    if selected_char["type"] not in owned_characters:
                        if total_coins >= selected_char["cost"]:
                            total_coins -= selected_char["cost"]
                            owned_characters.add(selected_char["type"])
                            current_character = selected_char["type"]
                    else:
                        current_character = selected_char["type"]
    
    return MENU, current_character, total_coins, owned_characters

# Pause Menu
def pause_menu(current_coins):
    paused = True
    button_height = 50
    button_width = 300
    button_margin = 20
    button_y_start = HEIGHT // 2 - 50
    
    buttons = [
        {"text": "Resume Game", "action": "resume", "y": button_y_start},
        {"text": "Quit to Menu", "action": "menu", "y": button_y_start + button_height + button_margin}
    ]
    
    while paused:
        pause_text = font.render("PAUSED", True, BLACK)
        coins_text = font.render(f"Coins Collected: {current_coins}", True, GOLD)
        
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
        screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 3 + 40))
        
        for button in buttons:
            button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
            pygame.draw.rect(screen, (200, 200, 200), button_rect)
            pygame.draw.rect(screen, BLACK, button_rect, 2)
            
            text = font.render(button["text"], True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button["y"] + button_height // 2 - text.get_height() // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        if button["action"] == "resume":
                            paused = False
                        elif button["action"] == "menu":
                            return MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    
    return PLAYING

# High Score Celebration Screen
def high_score_screen(score):
    high_score_sound.play()
    screen.fill(WHITE)
    draw_background()
    
    text = font.render("CONGRATULATIONS!", True, BLACK)
    score_text = font.render(f"New High Score: {score}", True, BLACK)
    continue_text = font.render("Press SPACE to Continue", True, BLACK)
    
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Game Over Screen
def game_over_screen(score, coins_collected, total_coins, owned_characters):
    global highscore
    new_high_score = False
    
    if score > highscore:
        new_high_score = True
        highscore = score
    
    total_coins += coins_collected
    save_data(highscore, total_coins, owned_characters)
    
    lose_sound.play()
    screen.fill(WHITE)
    draw_background()
    
    button_height = 50
    button_width = 300
    button_margin = 20
    button_y_start = HEIGHT // 2 + 50
    
    buttons = [
        {"text": "Play Again", "action": PLAYING, "y": button_y_start},
        {"text": "Main Menu", "action": MENU, "y": button_y_start + button_height + button_margin}
    ]
    
    game_over_text = font.render("GAME OVER", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {highscore}", True, BLACK)
    coins_text = font.render(f"Coins Collected: {coins_collected}", True, GOLD)
    total_coins_text = font.render(f"Total Coins: {total_coins}", True, GOLD)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 40))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 4 + 80))
    screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 4 + 120))
    screen.blit(total_coins_text, (WIDTH // 2 - total_coins_text.get_width() // 2, HEIGHT // 4 + 160))
    
    for button in buttons:
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
        pygame.draw.rect(screen, (200, 200, 200), button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        text = font.render(button["text"], True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button["y"] + button_height // 2 - text.get_height() // 2))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, button["y"], button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        return button["action"], total_coins
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return PLAYING, total_coins
                elif event.key == pygame.K_m:
                    return MENU, total_coins
    
    return MENU, total_coins


def main():
    global highscore, total_coins, owned_characters, SPEED
    
    game_state = MENU
    current_character = "default"
    current_city = "giza"
    
    while True:
        if game_state == MENU:
            game_state = main_menu(total_coins)
        
        elif game_state == ARENA_SELECT:
            game_state, current_city = arena_select_screen()
        
        elif game_state == SHOP:
            game_state, current_character, total_coins, owned_characters = shop_screen(total_coins, current_character, owned_characters)
            save_data(highscore, total_coins, owned_characters) 
        elif game_state == PLAYING:
            SPEED = 5
            
            character = CartoonCharacter()
            character.character_type = current_character
            character.reset()

            obstacles = []
            coins = []
            clouds = []
            score = 0
            coins_collected = 0
            game_time = 0
            obstacle_timer = 0
            coin_timer = 0
            cloud_timer = 0
            running = True
            paused = False
            
            next_obstacle_time = random.randint(60, 180)
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save_data(highscore, total_coins, owned_characters)
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            character.jump()
                        elif event.key == pygame.K_p:
                            paused = True
                            game_state = pause_menu(coins_collected)
                            if game_state != PLAYING:
                                running = False
                            else:
                                paused = False
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            game_state = MENU
                
                if paused:
                    continue
                
                game_time += 1
                
                obstacle_timer += 1
                if obstacle_timer >= next_obstacle_time:
                    obstacles.append(Obstacle(game_time, current_city))
                    obstacle_timer = 0
                    min_interval = max(30, 90 - score // 5)
                    max_interval = max(60, 180 - score // 2)
                    next_obstacle_time = random.randint(min_interval, max_interval)
                
                coin_timer += 1
                if coin_timer >= 30 and random.random() < 0.1:
                    coins.append(Coin())
                    coin_timer = 0
                
                cloud_timer += 1
                if cloud_timer >= 100:
                    clouds.append(Cloud())
                    cloud_timer = 0
                
                character.update()
                
                for obstacle in obstacles[:]:
                    obstacle.update()
                    if obstacle.off_screen():
                        obstacles.remove(obstacle)
                        if not obstacle.passed:
                            score += 1
                            obstacle.passed = True
                    elif obstacle.collide(character):
                        running = False
                
                for coin in coins[:]:
                    coin.update()
                    if coin.off_screen():
                        coins.remove(coin)
                    elif coin.collide(character):
                        coins_collected += 1
                        coin.collected = True
                        coin_sound.play()
                        coins.remove(coin)
                
                for cloud in clouds[:]:
                    cloud.update()
                    if cloud.off_screen():
                        clouds.remove(cloud)
                
                if game_time % 500 == 0:
                    SPEED += 0.25
                
                draw_background(current_city)
                
                for cloud in clouds:
                    cloud.draw(screen)
                
                character.draw(screen)
                
                for obstacle in obstacles:
                    obstacle.draw(screen)
                
                for coin in coins:
                    coin.draw(screen)
                
                score_text = font.render(f"Score: {score}", True, BLACK)
                high_score_text = small_font.render(f"High Score: {highscore}", True, BLACK)
                coins_text = font.render(f"Coins: {coins_collected}", True, GOLD)
                
                screen.blit(score_text, (10, 10))
                screen.blit(high_score_text, (10, 40))
                screen.blit(coins_text, (10, 70))
                
                if character.shield_active:
                    shield_text = small_font.render("SHIELD ACTIVE!", True, (0, 100, 255))
                    screen.blit(shield_text, (WIDTH - 140, 10))
                
                pygame.display.flip()
                clock.tick(FPS)
            
            if game_state == PLAYING: 
                if score > highscore:
                    high_score_screen(score)
                game_state, total_coins = game_over_screen(score, coins_collected, total_coins, owned_characters)
        
        else:
            game_state = MENU

if __name__ == "__main__":
    main()