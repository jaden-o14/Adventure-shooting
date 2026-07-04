import pygame
from pygame import mixer
import os
import random  
import csv
import button
import math
import sqlite3




mixer.init()
pygame.init()

#screen dimentions 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Shooting")


# set framerate 
clock = pygame.time.Clock()
FPS = 60

# level infos
# Level configuration
level_info = {
    0: {"folder": "mountain_map", "name": "mountain", "bg_offset": 100},
    1: {"folder": "desert_map", "name": "desert", "bg_offset": -80},
    2: {"folder": "jungle_map", "name": "jungle", "bg_offset": 100},
    3: {"folder": "snow_map", "name": "snow", "bg_offset": 130}
}



#define game variables
fullscreen = False
GRAVITY = 0.45
GRENADE_GRAVITY = 0.75
ROWS = 20
COLS = 25
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 19
level = 0
img_list = []     
bg_images = []     
sky_img = None
cloud_scroll = 0     
world_data = []
start_game = "login"
start_intro = False
start_intro_timer = 0
intro_delay = 90
level_select = False
player = None
level_num = 0
char_selected = "mountain_adventurer"
current_level = 0
current_volume = 0.5
pygame.mixer.music.set_volume(current_volume)
score = 0
current_user = None
current_uid = None
user_text = ""
pass_text = ""
active_input = "user" # Switch between typing 'user' or 'pass'
new_total = 0
leaderboard_results = []
data_loaded = False
score_saved = False



#define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

#load music and sound effects
pygame.mixer.music.load(r"Adventure_shooting_assets/audio/main_menu_music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound(r"Adventure_shooting_assets/audio/jump.wav")
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound(r"Adventure_shooting_assets/audio\sniper_shot.wav")
shot_fx.set_volume(0.1)
enemy_shot_fx = pygame.mixer.Sound(r"Adventure_shooting_assets/audio\shot.wav")
enemy_shot_fx.set_volume(0.3)
grenade_fx = pygame.mixer.Sound(r"Adventure_shooting_assets/audio/grenade.wav")
grenade_fx.set_volume(0.7)
bot_damaged_fx = pygame.mixer.Sound(r"Adventure_shooting_assets/audio\bot_damaged.wav")
bot_damaged_fx.set_volume(0.2)
player_damaged_fx = pygame.mixer.Sound(r"Adventure_shooting_assets\audio\player_damaged.flac")
player_damaged_fx.set_volume(0.2)
bot_life_lost_fx = pygame.mixer.Sound(r"Adventure_shooting_assets\audio\bot_life_lost.wav")
bot_life_lost_fx.set_volume(0.3)
player_life_lost_fx = pygame.mixer.Sound(r"Adventure_shooting_assets\audio\player_life_lost.wav")
player_life_lost_fx.set_volume(0.3)

#load image 
#store tiles in list
mountain_img_list = []
for x in range (TILE_TYPES):
    mountain_img = pygame.image.load(f"Adventure_shooting_assets\img\mountain_map\{x}.png").convert_alpha()
    mountain_img = pygame.transform.scale(mountain_img, (TILE_SIZE, TILE_SIZE))
    mountain_img_list.append(mountain_img)
heart_img = pygame.image.load("Adventure_shooting_assets\img\icons\heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img,(20,20))
#bullet
bullet_img = pygame.image.load("Adventure_shooting_assets\img\icons/bullet.png").convert_alpha()
#grenade
grenade_img = pygame.image.load("Adventure_shooting_assets\img\grenade.png").convert_alpha()
#pick up perk boxes
ammo_box_img = pygame.image.load("Adventure_shooting_assets\img/ammo_box.png").convert_alpha()
grenade_box_img = pygame.image.load("Adventure_shooting_assets\img\grenade_box.png").convert_alpha()
item_boxes = {"Ammo" : ammo_box_img,
              "Grenade": grenade_box_img}
menu_img = pygame.image.load("Adventure_shooting_assets/img/icons/main_menu_bg.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
# hit icon image
hit_img = pygame.image.load("Adventure_shooting_assets\img\icons\hit.png").convert_alpha()
#button images
play_img = pygame.image.load("Adventure_shooting_assets\img\icons\play_btn.png").convert_alpha()
leaderboard_img = pygame.image.load("Adventure_shooting_assets\img\icons\leaderboard_btn.png").convert_alpha()
settings_img = pygame.image.load("Adventure_shooting_assets\img\icons\settings_btn.png").convert_alpha()
play_again_img = pygame.image.load("Adventure_shooting_assets\img\icons\play_again_btn.png").convert_alpha()
mtn_img = pygame.image.load("Adventure_shooting_assets\img\icons\mtn_btn.png").convert_alpha()
desert_img = pygame.image.load("Adventure_shooting_assets\img\icons\desert_btn.png").convert_alpha()
jungle_img = pygame.image.load("Adventure_shooting_assets\img\icons\jungle_btn.png").convert_alpha()
snow_img = pygame.image.load("Adventure_shooting_assets\img\icons\snow_btn.png").convert_alpha()
char1_img = pygame.image.load("Adventure_shooting_assets\img\mountain_adventurer\idle/0.png")
char2_img = pygame.image.load("Adventure_shooting_assets\img\desert_adventurer\idle/0.png")
char3_img = pygame.image.load("Adventure_shooting_assets\img\jungle_adventurer\idle/0.png")
char4_img = pygame.image.load("Adventure_shooting_assets\img\snow_adventurer\idle/0.png")
dust_images = []
for i in range(9):
    img = pygame.image.load(f"Adventure_shooting_assets\img\dust_cloud\{i}.png")
    img = pygame.transform.scale(img,(69,20))
    dust_images.append(img)
main_menu_img = pygame.image.load("Adventure_shooting_assets\img\icons\main_menu_btn.png").convert_alpha()
exit_icon_img = pygame.image.load("Adventure_shooting_assets\img\icons\exit_btn.png").convert_alpha()
minus_img = pygame.image.load("Adventure_shooting_assets\img\icons\minus_btn.png").convert_alpha()
plus_img = pygame.image.load("Adventure_shooting_assets\img\icons\plus_btn.png").convert_alpha()
back_img = pygame.image.load("Adventure_shooting_assets\img\icons/back_btn.png").convert_alpha()
#define colours
BG = (50, 50, 240)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
GREEN = (144, 201, 120)
GOLD = (218, 165, 32)
BROWN = (101, 67, 33)   
ORANGE = (255, 165, 0)




#font

font = pygame.font.SysFont('joystix', 30)
game_over_font = pygame.font.SysFont('Bloody Terror', 50)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)



#player class called Adventurer and all attributes are defined below
class Adventurer(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale,speed, ammo, grenades ):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.lives = 5
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0 
        self.grenades = grenades
        self.direction = 1
        self.knockback_timer = 0
        self.knockback_dir = 0
        self.knockback_dx = 0
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables

        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0


        #load all images for the players
        animation_types = ['idle', "running", "jumping", ]
        for animation in animation_types:
            #resets the temporary list of images
            temp_list = []
            #counts the number of files in the folder
            num_of_frames = len(os.listdir(fr"Adventure_shooting_assets\img\{self.char_type}\{animation}"))

            for i in range(num_of_frames):
                img = pygame.image.load(fr"Adventure_shooting_assets\img\{self.char_type}\{animation}\{i}.png").convert_alpha() 
                img = pygame.transform.scale (img, (int(img.get_width()* scale),int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        #custom-sized rectangle
        self.width = 24   # Adjust based on your character's body width
        self.height = 60  # Adjust based on your character's body height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
    
    def update(self):
        self.update_animation()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    #move method or function so that the player is able to move
    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        hit_wall = False



        # horizontal movement
        if self.knockback_timer > 0:
            self.update_knockback()
        else:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

        # vertical movement (Jump/Gravity)
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y


        #collision with the level
        for tile in world.obstacle_list:
            # Check for collision in X direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                hit_wall = True
                # If the ai hits a wall, tell it to turn around
                if self.char_type == 'mountain_enemy':
                    self.direction *= -1
                    self.move_counter = 0

            # check for collision in Y direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                # check if jumping (hitting head on ceiling)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if falling (hitting feet on floor)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
            


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        return hit_wall
                                

            
    #shooting method or function that allows the player to shoot bullets with a limit
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo :
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self)
            bullet_group.add(bullet)  
            #reduce ammo
            self.ammo -= 1  
            shot_fx.play()

             

    #this is the function for the AI to chase the player and jump over obstacles and shoot when in range shoot the player
    def ai(self,player):
        if self.alive and player.alive:
           
            #checking coordinates and distance from the player to the enemy
            dist_x = player.rect.centerx - self.rect.centerx
            dist_y = player.rect.centery - self.rect.centery
            
            dx = 0
            dy = 0
            hit_wall = False



            #movement logic for the AI
            if self.knockback_timer > 0:
                dx = self.knockback_dir * 10
                self.knockback_timer -= 1
            else:
                # Keeps chasing even in the air to make sure that they are able to make forward jumps
                if abs(dist_x) > 100: # reduced buffer so AI gets closer to ledges
                    if dist_x > 0:
                        dx = self.speed
                        self.flip = False
                        self.direction = 1
                    elif dist_x < 0:
                        dx = -self.speed
                        self.flip = True
                        self.direction = -1

            # vertival physics
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            
            # Wall detection
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    hit_wall = True


            # ledge/gap detection
            check_x = self.rect.centerx + (self.direction * 35) # Looking slightly further ahead
            check_y = self.rect.bottom + 1
            is_ground_ahead = False
            for tile in world.obstacle_list:
                if tile[1].collidepoint(check_x, check_y):
                    is_ground_ahead = True
                    break

            #trigger for forward jumping
            # If hitting a wall or a gap is detected the ai jumps
            if (hit_wall or not is_ground_ahead) and not self.in_air:
                if self.knockback_timer == 0:
                    self.vel_y = -12 
                    self.in_air = True
                    self.rect.y -= 2 
            
            # If hit_wall is true but we AREN'T jumping then it should stop horizontal movement
            if hit_wall and not self.in_air:
                dx = 0

            # checking for collsions 
            # Vertical Collision
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.direction *= -1

            # updates the ai's position
            self.rect.x += dx
            self.rect.y += dy

            # animation and shooting logic for the AI
            if self.in_air:
                self.update_action(2) # Jump animation
            elif self.knockback_timer == 0:
                # Only stop to shoot if on the ground
                if abs(dist_x) < 400 and abs(dist_y) < TILE_SIZE:
                    self.update_action(0) # Idle
                    self.shoot()
                    dx = 0 # Stop moving while shooting
                else:
                    self.update_action(1) # Run

                # this is a method in the adventurer class that makes sure the ai respawns if the player gets too far away from them so that they don't just camp in one spot and wait for the player to come to them
    def respawn(self, valid_points):
        if valid_points:
            # pick a random spot from the floor tiles that was found in process_data
            spawn_pos = random.choice(valid_points)
            self.rect.x = spawn_pos[0]
            self.rect.y = spawn_pos[1]
            
            # reset their stats so they are "new" again
            self.alive = True
            self.lives = 5 
            self.ammo = self.start_ammo
            self.vel_y = 0

    #this is a method used to update the animation depending on where the character is moving or what action they are doing
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
            #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index= len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0
    
    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    def apply_knockback(self, bullet_x):
        # determine if bullet is left of player and knock player right
        if bullet_x < self.rect.centerx:
            self.knockback_dx = 15  # Power of the push
        else:
            self.knockback_dx = -15
        
        # how long the stun lasts in frames
        self.knockback_timer = 12 
        # A small vertical hop 
        if not self.in_air:
            self.vel_y = -5
            self.in_air = True

    def update_knockback(self):
        if self.knockback_timer > 0:
            # apply the current knockback velocity
            self.rect.x += self.knockback_dx
            self.knockback_timer -= 1
            #slow down the slide gradually
            self.knockback_dx *= 0.9


    def respawn_randomly(self, valid_points, player):
        # 1. Define a 'Safe Zone' (e.g., 500 pixels away)
        safe_distance = 500
        
        # 2. Filter for points that are NOT right next to the player
        # We also check the player's direction to try and spawn BEHIND them
        potential_points = []
        for p in valid_points:
            dist = abs(p[0] - player.rect.x)
            
            # If player faces right (direction 1), prefer points to the left
            # If player faces left (direction -1), prefer points to the right
            is_behind = (player.direction == 1 and p[0] < player.rect.x) or \
                        (player.direction == -1 and p[0] > player.rect.x)
            
            if dist > safe_distance or is_behind:
                potential_points.append(p)

        # 3. If we found safe spots, pick one. Otherwise, pick the furthest possible spot.
        if potential_points:
            target = random.choice(potential_points)
        else:
            # Emergency: Sort by distance and pick the furthest one
            target = max(valid_points, key=lambda p: abs(p[0] - player.rect.x))

        self.rect.topleft = target
        self.lives = 5
        self.alive = True
        self.vel_y = 0



            
    
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip, False) ,self.rect)

        if self.knockback_timer > 0:
            # draw the hit icon 
            screen.blit(hit_img, (self.rect.centerx - (hit_img.get_width()//2), self.rect.y - 30))

# Create a specialized 'child' class
class Enemy(Adventurer): 
    def __init__(self, x, y, scale, speed, ammo, grenades, valid_points):
        # This line tells it to copy everything from the Adventurer class
        super().__init__('enemy', x, y, scale, speed, ammo, grenades)
        self.valid_points = valid_points

    def update_enemy(self, player):
        # Only put the logic here that is DIFFERENT from the player
        if self.lives <= 0:
            self.respawn_randomly(self.valid_points, player)

class HitMarker(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        #get actual numbers for width and heights
        width = hit_img.get_width()
        height = hit_img.get_height()
        
        # scale the image using integers
        self.image = pygame.transform.scale(hit_img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 10 # this is the countdown

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill() # this removes it from all groups

class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction 

    def update(self):
        self.vel_y += GRENADE_GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        #check collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed  

            if tile[1].colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                    # check if jumping (hitting head on ceiling)
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    # check if falling (hitting feet on floor)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom          





         #update grenade position
        self.rect.x += dx
        self.rect.y += dy
            

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y,0.5)
            explosion_group.add(explosion)
            #damage to anyone nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.apply_knockback(self.rect.centerx)
          

            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.apply_knockback(self.rect.centerx)



        if player.rect.top > SCREEN_HEIGHT:
            player.lives -= 1 # subtract a life if player falls off screen
            #reset player position
            player.rect.center = (100,200)





class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1,6):
            img = pygame.image.load(fr"Adventure_shooting_assets\img\explosion\exp{num}.png").convert_alpha() 
            img = pygame.transform.scale(img, (int(img.get_width() * 2),int( img.get_height() * 2)))
            self.images.append(img) 
            self.frame_index = 0
            self.image = self.images[self.frame_index] 
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


class Dust(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = dust_images
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        # position at the player's feet
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        dust_speed = 3.5 # animation speed for teh dust cloud
        self.counter += 1
        if self.counter >= dust_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill() # delete when animation finishes
            else:
                self.image = self.images[self.frame_index]



class ScreenFade():
    def __init__(self, direction, colour,speed ):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0


    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#whole screen fade
            pygame.draw.rect(screen, self.colour,(0 - self.fade_counter, 0,SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,(0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,(0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:#vertical screen fade down
            pygame.draw.rect(screen, self.colour,(0,0,SCREEN_WIDTH,0 + self.fade_counter))
        if self.fade_counter >= SCREEN_HEIGHT:
            fade_complete = True
        return fade_complete

#create screen fades 
intro_fade = ScreenFade(1, BG, 4)
death_fade = ScreenFade(2, PINK, 4)


class World ():
    def __init__(self):
        self.obstacle_list = []
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])


    def process_data(self, data, level_num):
        player = None
        # create a list of all floor tiles during level generation
        self.valid_spawn_points = []
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                    self.valid_spawn_points.append((x * TILE_SIZE, (y - 1) * TILE_SIZE))
                    current_tile_img = img_list[tile] 
                    img_rect = current_tile_img.get_rect()
                    img_rect.x = x * TILE_SIZE 
                    img_rect.y = y * TILE_SIZE 
                    tile_data = (current_tile_img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                        if tile == 1:
                            self.valid_spawn_points.append((x * TILE_SIZE, y * TILE_SIZE - TILE_SIZE))
                    elif tile >= 9 and tile <= 10:
                        water = Water(img_list[tile], x * TILE_SIZE,y * TILE_SIZE, )     
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img_list[tile], x * TILE_SIZE, y * TILE_SIZE, )     
                        decoration_group.add(decoration)                              
                    elif tile == 15:#player
                        print(f"player found at {x}, {y}")
                        player = Adventurer(char_selected,x * TILE_SIZE,y * TILE_SIZE,1.65, 4,20,5)
                    elif tile == 16:# enemy
                        if level_num == 0:
                            enemy_type = "mountain_enemy"
                        if level_num == 1:
                            enemy_type = "desert_enemy"
                        if level_num == 2:
                            enemy_type = "jungle_enemy"
                        if level_num == 3:
                            enemy_type = "snow_enemy"                            
                        enemy = Adventurer(enemy_type,x * TILE_SIZE ,y * TILE_SIZE,1.65, 4,20,0)
                        enemy_group.add(enemy)                    
                    elif tile == 17:
                        item_box = ItemBox(x * TILE_SIZE,y * TILE_SIZE, "Ammo")     
                        item_box_group.add(item_box)  
                    elif tile == 18:
                        item_box = ItemBox(x * TILE_SIZE,y * TILE_SIZE, "Grenade")     
                        item_box_group.add(item_box)    
        return player


    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)         

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)        



class ItemBox(pygame.sprite.Sprite):
    def __init__(self,x,y,item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2  ,y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        #check if player collides with the box
        if pygame.sprite.collide_rect(self, player):
            #check what type of box it is
            if self.item_type == "Ammo":
                player.ammo += 15
            if self.item_type == "Grenade":
                player.grenades += 3
            #delete the item box
            self.kill()




class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,shooter):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.shooter = shooter  
    
    def update(self):
        # Move bullet
        self.rect.x += (self.speed * self.direction)
        
        # checks if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # checks collision with ALL enemies
        for enemy in enemy_group:
            if pygame.sprite.collide_rect(self, enemy):
                self.kill() # destroys the bullet

                # apply knockback logic
                enemy.knockback_timer = 20
                if self.rect.centerx < enemy.rect.centerx:
                    enemy.knockback_dir = 1
                    bot_damaged_fx.play()
                else:
                    enemy.knockback_dir = -1
                    bot_damaged_fx.play()
                

                if enemy.lives <= 0:
                        enemy.respawn_randomly(world.valid_spawn_points)
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        


# create buttons
play_button = button.Button(SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2 - 200, play_img, 0.75)
leaderboard_button = button.Button(SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2 - 100, leaderboard_img, 0.75)
settings_button = button.Button(SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2 , settings_img, 0.75)
play_again_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, play_again_img, 0.75)
main_menu_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,main_menu_img, 0.75)
back_button = button.Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 150,back_img, 0.45)
exit_icon_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150,exit_icon_img, 0.75)
button_spacing = 150
mountain_button = button.Button(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 , mtn_img, 1.5)
desert_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 , desert_img, 0.5)
jungle_button = button.Button(SCREEN_WIDTH // 2 + 100 , SCREEN_HEIGHT // 2 , jungle_img, 0.5)
snow_button = button.Button(SCREEN_WIDTH // 2 + 300  , SCREEN_HEIGHT // 2 , snow_img, 0.5)
minus_button = button.Button(SCREEN_WIDTH // 2 - 235, SCREEN_HEIGHT // 2 + 360, minus_img, 0.1)
plus_button = button.Button(SCREEN_WIDTH // 2 + 235, SCREEN_HEIGHT // 2 + 360, plus_img, 0.1)
#character buttons
char1_button = button.Button(SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2, char1_img, 2)
char2_button = button.Button(SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2, char2_img, 2)
char3_button = button.Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, char3_img, 2)
char4_button = button.Button(SCREEN_WIDTH // 2 + 125, SCREEN_HEIGHT // 2, char4_img, 2)



pygame.draw.rect(char1_button.image, PINK, char1_button.image.get_rect(), 2    )
pygame.draw.rect(char2_button.image, PINK, char2_button.image.get_rect(), 2    )
pygame.draw.rect(char3_button.image, PINK, char3_button.image.get_rect(), 2    )
pygame.draw.rect(char4_button.image, PINK, char4_button.image.get_rect(), 2    )



#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
dust_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
hit_marker_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
           





#create empty tile list
world_data = []
for row in range (ROWS):
    r = [-1] * COLS
    world_data.append(r)




def draw_lives(lives):
    for i in range(lives):
        screen.blit(heart_img, (110 + (i * 35), 80))

def load_level_assets(level_index):
    global img_list, bg_images, sky_img
    
    info = level_info.get(level_index)
    folder = info["folder"]
    folder_path = fr"c:\pyhton_nea\Adventure_shooting_assets\img\{folder}"
    
    # load tiles for this Biome
    img_list = []
    for x in range(TILE_TYPES):
        tile_path = os.path.join(folder_path, f"{x}.png")
        tile_img = pygame.image.load(tile_path).convert_alpha()
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        img_list.append(tile_img)

    # load scrolling sky (The clouds layer)
    sky_path = os.path.join(folder_path, "sky.png")
    sky_img = pygame.image.load(sky_path).convert_alpha()
    sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, int(SCREEN_HEIGHT)))

    # 3. load background layers (Mountains/Pines)
    bg_images = []
    i = 0
    while os.path.exists(os.path.join(folder_path, f"bg{i}.png")):
        bg_path = os.path.join(folder_path, f"bg{i}.png")
        img = pygame.image.load(bg_path).convert_alpha()
        
        # proportional Scaling
        w, h = img.get_width(), img.get_height()
        ratio = SCREEN_WIDTH / w
        

        scale_factor = 1.8 if i == 0 else 1.2 
        new_height = int(h * ratio * scale_factor)
        
        img = pygame.transform.scale(img, (SCREEN_WIDTH, new_height))
        bg_images.append(img)
        i += 1
def draw_bg():
    global cloud_scroll
    # fill background color as a fallback
    screen.fill(BG)
    
    # draws the sky with cloud drift
    if sky_img:
        screen.blit(sky_img, (int(cloud_scroll), 0))
        screen.blit(sky_img, (int(cloud_scroll + SCREEN_WIDTH), 0))
        cloud_scroll -= 0.5 # Drift speed
        if abs(cloud_scroll) >= SCREEN_WIDTH:
            cloud_scroll = 0
    
    #  draw background layers (Mountains then Pines)
    for i, img in enumerate(bg_images):
        # lift mountains  higher than pines (i=1)
        if i == 0:
            y_offset = level_info[level]["bg_offset"]
        else:
            y_offset = 0 

        y_pos = SCREEN_HEIGHT - img.get_height() - y_offset
        screen.blit(img, (0, y_pos))



def reset_level():
    # Clear all sprite groups
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    hit_marker_group.empty()

    global score 
    score = 0

    # Create empty tile list to clear the old map
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

def load_and_start_level(level_num):
    global world, player, start_game, world_data
    
    # reset everything
    world_data = reset_level()
    
    # load the specific CSV
    folder = level_info[level_num]["folder"]
    name = level_info[level_num]["name"]
    csv_path = fr"c:\pyhton_nea\Adventure_shooting_assets\img\{folder}\{name}_level{level_num}.csv"
    
    with open(csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row_index, row in enumerate(reader):
            for col_index, tile in enumerate(row):
                world_data[row_index][col_index] = int(tile)
    
    # load the map and spawn player
    load_level_assets(level_num)
    world = World()
    player = world.process_data(world_data, level_num)
    
    # start the gameplay loop
    start_game = True
    return player



def draw_player_hud():
    #  defines the Box dimensions and position (Bottom Left)
    box_width = 250
    box_height = 110
    box_x = 20
    box_y = SCREEN_HEIGHT - box_height - 20

    #  Draws the white border and dark background box
    pygame.draw.rect(screen, WHITE, (box_x - 2, box_y - 2, box_width + 4, box_height + 4)) # Border
    pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_width, box_height)) # Main Box

    # draws the text labels
    # positions them relative to the box_x and box_y
    draw_text(f"SCORE: {new_total}", font, GOLD, box_x, box_y - 40)
    draw_text("AMMO:", font, WHITE, box_x + 10, box_y + 10)
    draw_text("GRENADES:", font, WHITE, box_x + 10, box_y + 40)
    draw_text("LIVES:", font, WHITE, box_x + 10, box_y + 70)

    #  draw the icons (ammo)
    for x in range(player.ammo):
        #  capping the ammo dots so they don't leave the box
        if x < 100: 
            screen.blit(bullet_img, (box_x + 80 + (x * 7), box_y + 15))

    # draws the Icons (Grenades)
    for x in range(player.grenades):
        if x < 10:
            screen.blit(grenade_img, (box_x + 130 + (x * 12), box_y + 45))

    # Draw the Hearts (Lives)
    for x in range(player.lives):
        screen.blit(heart_img, (box_x + 80 + (x * 30), box_y + 72))

def draw_enemy_hud():
    # define Position (Bottom Right)
    box_width = 250
    box_height = 80 # slightly shorter since enemies don't usually need ammo display
    box_x = SCREEN_WIDTH - box_width - 20
    box_y = SCREEN_HEIGHT - box_height - 20

    # draw the Box (White border, dark background)
    pygame.draw.rect(screen, WHITE, (box_x - 2, box_y - 2, box_width + 4, box_height + 4))
    pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_width, box_height))

    # draw Enemy Label
    draw_text("BOT 1", font, RED, box_x + 10, box_y + 10)
    draw_text("LIVES:", font, WHITE, box_x + 10, box_y + 40)
    draw_text("AMMO:", font, WHITE, box_x + 10, box_y + 60)

    # draw enemy stocks
    # we grab the first enemy from your group
    if len(enemy_group) > 0:
        main_enemy = enemy_group.sprites()[0]
        for x in range(main_enemy.lives):
            # using small circles for a distinct "Bot" look
            pygame.draw.circle(screen, RED, (box_x + 90 + (x * 25), box_y + 52), 8)
            pygame.draw.circle(screen, WHITE, (box_x + 90 + (x * 25), box_y + 52), 8, 2) # Outline

    else:
        draw_text("ELIMINATED", font, RED, box_x + 90, box_y + 40)

def login_user(username, password):
    try:
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        # Search for a matching username and password
        cursor.execute("SELECT * FROM userList WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            print(f"Login successful,welcome back: ", {username})
            return result[0]
        return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
def register_user(username, password):
    try:
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        # Insert new user with a starting score of 0
        cursor.execute("INSERT INTO userList (Username, Password) VALUES (?, ?)", (username, password))
        new_id = cursor.lastrowid  # gets the ID of the new user
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Registration error: {e}")
        return False
    
def add_to_db_score(user_id, points_earned):
    if user_id is not None:
        try:
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            
            # 1. Get the current total from the LEADERBOARD table using uID
            cursor.execute("SELECT Score FROM leaderboard WHERE uID = ?", (user_id,))
            result = cursor.fetchone()
            
            current_total = result[0] if result and result[0] is not None else 0
            
            # 2. Calculate the new total
            global new_total
            new_total = current_total + points_earned
            
            # 3. Update the LEADERBOARD table (or INSERT if it's their first score)
            if result:
                cursor.execute("UPDATE leaderboard SET Score = ? WHERE uID = ?", (new_total, user_id))
            else:
                cursor.execute("INSERT INTO leaderboard (uID, Score) VALUES (?, ?)", (user_id, new_total))
                
            conn.commit()
            conn.close()
            print(f"Total updated! New Total: {new_total}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

def save_high_score(user_id, score):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    
    # This puts the score into the linked table
    cursor.execute("INSERT INTO leaderboard (uID, Score) VALUES (?, ?)", (user_id, score))
    
    conn.commit()
    conn.close()

def get_leaderboard_data():
    conn = sqlite3.connect("user.db") # Use the name from image_c02a3d.png
    cursor = conn.cursor()
    
    # Updated table name to 'leaderboard'
    query = """
    SELECT userList.Username, leaderboard.Score 
    FROM leaderboard 
    JOIN userList ON leaderboard.uID = userList.uID 
    ORDER BY leaderboard.Score DESC 
    LIMIT 10
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def draw_leaderboard(screen, font, leaderboard_data):
    screen.blit(menu_img, (0,0))    
    # 1. Colors from your image
    ORANGE_BG = (255, 165, 0) # Adjust to match your specific orange
    LINE_COLOR = (0, 0, 0)
    TEXT_COLOR = (0, 0, 0)

    # 2. Table Dimensions and Position
    table_width = 400
    table_height = 400
    start_x = (SCREEN_WIDTH // 2) - (table_width // 2)
    start_y = 250
    row_height = 50
    col_split = start_x + (table_width // 2)

    # 3. Draw Title
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    draw_text("Leader board", title_font, TEXT_COLOR, SCREEN_WIDTH // 2 - 140, 80)

    # 4. Draw Table Background and Grid Lines
    # Main Box
    pygame.draw.rect(screen, (255, 200, 100), (start_x, start_y, table_width, table_height))
    pygame.draw.rect(screen, LINE_COLOR, (start_x, start_y, table_width, table_height), 2)
    
    # Vertical Center Line
    pygame.draw.line(screen, LINE_COLOR, (col_split, start_y), (col_split, start_y + table_height), 2)

    # 5. Draw Headers
    draw_text("Name", font, TEXT_COLOR, start_x + 60, start_y + 10)
    draw_text("High Score", font, TEXT_COLOR, col_split + 60, start_y + 10)
    pygame.draw.line(screen, LINE_COLOR, (start_x, start_y + row_height), (start_x + table_width, start_y + row_height), 2)

    # 6. Draw Data Rows
    for i, (name, score) in enumerate(leaderboard_data):
        y_pos = start_y + ((i + 1) * row_height)
        
        # Horizontal row line
        pygame.draw.line(screen, LINE_COLOR, (start_x, y_pos + row_height), (start_x + table_width, y_pos + row_height), 2)
        
        # Text alignment
        draw_text(str(name), font, TEXT_COLOR, start_x + 40, y_pos + 10)
        draw_text(str(score), font, TEXT_COLOR, col_split + 70, y_pos + 10)
        
        if i >= 6: break # Only show top 7 to fit the table




def reset_game():
    global player, score 
    enemy_group.empty()
    bullet_group.empty()
    dust_group.empty()
    
    score = 0
    player = load_and_start_level(level_num) 
    player.lives = 5
    player.alive = True



run = True
while run:

    clock.tick(FPS) 


    if start_game == False:
        #draw menu
        screen.blit(menu_img, (0,0))


        draw_text(f"SCORE: {new_total}", font, WHITE, SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT// 2 - 300)


        #add buttons
        if play_button.draw(screen):
            intro_fade.fade_counter = 0
            start_game = "char_menu"
            start_intro = True
            pygame.time.delay(200) 

        if leaderboard_button.draw(screen):
            print("leaderboard clicked")
            intro_fade.fade_counter = 0
            start_game = "leaderboard"
            data_loaded = False

        settings_button = button.Button(SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2 , settings_img, 0.75)
        if settings_button.draw(screen):
            print("settings clicked")
            intro_fade.fade_counter = 0
            start_game = "settings"
            pygame.time.delay(200)

        if exit_icon_button.draw(screen):
            run = False
        
        intro_fade.fade()
    


    elif start_game == "settings":
        screen.fill(BG)
  
        #draw the banner panel (The Background)
        panel_width, panel_height = 600, 520
        px = SCREEN_WIDTH // 2 - panel_width // 2
        py = SCREEN_HEIGHT // 2 - panel_height // 2
        
        # gold border & brown background
        pygame.draw.rect(screen, (218, 165, 32), (px - 5, py - 5, panel_width + 10, panel_height + 10), border_radius=15)
        pygame.draw.rect(screen, (101, 67, 33), (px, py, panel_width, panel_height), border_radius=10)
        
        
        draw_text("SCREEN:", font, WHITE, px + 50, py + 420)
        draw_text("OPTIONS", font, (255, 215, 0), px + 220, py + 20)

        #drawing the controls
        draw_text("CONTROLS:", font, WHITE, px + 50, py + 80)
        draw_text("- A : MOVE LEFT", font, WHITE, px + 80, py + 130)
        draw_text("- D: MOVE RIGHT", font, WHITE, px + 80, py + 180)
        draw_text("- W: JUMP", font, WHITE, px + 80, py + 230)
        draw_text("- T: SHOOT", font, WHITE, px + 80, py + 280)
        draw_text("- Y: GRENADE", font, WHITE, px + 80, py + 330)

        # volume section
        draw_text("VOLUME", font, WHITE, px + 50, py + 360)
        
        # position volume buttons on either side of the bar
        minus_button.rect.topleft = (px + 180, py + 355)
        plus_button.rect.topleft = (px + 450, py + 355)

        # draw the black Bar Background
        pygame.draw.rect(screen, (0, 0, 0), (px + 235, py + 360, 200, 25))
        # draw the green volume Level
        pygame.draw.rect(screen, (0, 255, 0), (px + 235, py + 360, 200 * current_volume, 25))

        # volume Logic
        if minus_button.draw(screen):
            current_volume = max(0, current_volume - 0.1)
            pygame.mixer.music.set_volume(current_volume)
            jump_fx.set_volume(current_volume) # Correct method
            pygame.time.delay(150)

        if plus_button.draw(screen):
            current_volume = min(1.0, current_volume + 0.1)
            pygame.mixer.music.set_volume(current_volume)
            jump_fx.set_volume(current_volume) # Correct method
            pygame.time.delay(150)

        # main menu button (At the bottom)
        main_menu_button.rect.topleft = (px + 220, py + 430)
        if main_menu_button.draw(screen):
            start_game = False # Go back to main menu
            pygame.time.delay(200)

        intro_fade.fade()

    elif start_game == "leaderboard":
        screen.fill((ORANGE)) # Fill with a solid color to clear the menu
        
        
        # Fetch data ONCE
        if not data_loaded:
            leaderboard_results = get_leaderboard_data()
            data_loaded = True
        
        # Draw the actual list
        draw_leaderboard(screen, font, leaderboard_results)

        intro_fade.fade()
        
        # Back Button to return to menu
        main_menu_button = button.Button(SCREEN_WIDTH // 2 + 150, 0, main_menu_img, 0.75)
        if main_menu_button.draw(screen):
            intro_fade.fade_counter = 0
            start_game = False
            data_loaded = False # reset for next time
            score_saved = False # reset score saved flag for next time

    elif start_game == "login":
        screen.fill(BG)
        screen.blit(menu_img, (0,0))        
        
        # Draw the Login Panel
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(screen, (101, 67, 33), panel_rect, border_radius=10) # Brown panel
        pygame.draw.rect(screen, GOLD, panel_rect, 5, border_radius=10)      # Gold border
        
        draw_text("LOGIN / REGISTER", font, GOLD, panel_rect.x + 50, panel_rect.y + 20)
        
        # Username Input Box
        color_u = WHITE if active_input == "user" else (150, 150, 150)
        draw_text("Username:", font, WHITE, panel_rect.x + 20, panel_rect.y + 80)
        pygame.draw.rect(screen, color_u, (panel_rect.x + 20, panel_rect.y + 110, 360, 40), 2)
        draw_text(user_text, font, WHITE, panel_rect.x + 30, panel_rect.y + 115)
        
        # Password Input Box
        color_p = WHITE if active_input == "pass" else (150, 150, 150)
        draw_text("Password:", font, WHITE, panel_rect.x + 20, panel_rect.y + 170)
        pygame.draw.rect(screen, color_p, (panel_rect.x + 20, panel_rect.y + 200, 360, 40), 2)
        # Display asterisks for password
        draw_text("*" * len(pass_text), font, WHITE, panel_rect.x + 30, panel_rect.y + 205)
        
        draw_text("TAB to switch | ENTER to Play", font, WHITE, panel_rect.x + 20, panel_rect.y + 260)

    elif start_game == False: # Main Menu follows login
        screen.blit(menu_img, (0,0))
        intro_fade.fade()


    elif start_game == "char_menu":
        screen.fill(BG)
        draw_text("CHOOSE YOUR ADVENTURER", font, WHITE, SCREEN_WIDTH // 2 - 100, 50)

        if char1_button.draw(screen):
            char_selected = "mountain_adventurer"
            start_game = "level_menu" # now it goes to level selection
            pygame.time.delay(200)

        if char2_button.draw(screen):
            char_selected = "desert_adventurer" 
            start_game = "level_menu"
            pygame.time.delay(200)

        if char3_button.draw(screen):
            char_selected = "jungle_adventurer"
            start_game = "level_menu" 
            pygame.time.delay(200)
            
        if char4_button.draw(screen):
            char_selected = "snow_adventurer" 
            start_game = "level_menu"
            pygame.time.delay(200)

        if back_button.draw(screen):
            start_game = False # back to main menu
            pygame.time.delay(200)
        
    elif start_game == "level_menu":
        screen.fill(BG)
        draw_text("SELECT THE BIOME!!!", font, WHITE, SCREEN_WIDTH // 2 - 100, 50)
 

        if mountain_button.draw(screen):
            level_num = 0
            load_and_start_level(0) 
            start_intro = True
            GRAVITY = 0.25
            pygame.mixer.music.stop() 
 
        if desert_button.draw(screen):
            level_num = 1
            load_and_start_level(1)
            if start_intro == True:
                pygame.mixer.music.stop()
 
                                                
        if jungle_button.draw(screen):
            level_num = 2
            load_and_start_level(2)
            start_intro = True 
            player.lives = 7 
            pygame.mixer.music.stop()                                   
            #this is for the snow map selection which loads the snow level
        
        if snow_button.draw(screen):
            level_num = 3
            load_and_start_level(3)
            start_intro = True
            player.lives = 10
            #this stops the main menu music when the player enters a game. 
            pygame.mixer.music.stop()

        if back_button.draw(screen):
            start_game = "char_menu"
            pygame.time.delay(200)

    
    elif start_game == "victory":
        if not score_saved :

            add_to_db_score(current_uid, score) # Add this level's score to the total
            score_saved = True
            score = 0 # Reset score for the next game       
            #  draw a dark  overlay over the game
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))


       # draw the main Panel 
        panel_width, panel_height = 400, 450
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2            
        # gold Border
        pygame.draw.rect(screen, (218, 165, 32), (panel_x - 5, panel_y - 5, panel_width + 10, panel_height + 10), border_radius=15)            # wood-colored Background
        pygame.draw.rect(screen, (101, 67, 33), (panel_x, panel_y, panel_width, panel_height), border_radius=10)

            
        # header Text
        draw_text("VICTORY", font, (255, 215, 0), panel_x + 125, panel_y + 10)
                #  shows the score on the victory menu
        draw_text(f"TOTAL SCORE: {new_total}", font, (255, 215, 0), panel_x + 125, panel_y + 50)
            
        # buttons (Positioned inside the panel)
        if play_again_button.draw(screen):
            load_and_start_level(level_num) # Reload the current level
            start_game = True # Back to action
            pygame.time.delay(200)

        if main_menu_button.draw(screen):
            reset_game()
            start_game = False # Back to title
            pygame.time.delay(200)
            

        settings_button = button.Button(SCREEN_WIDTH // 2 - 105, SCREEN_HEIGHT // 2 - 130 , settings_img, 0.75)
        if settings_button.draw(screen):
            start_game = "settings"
            pygame.time.delay(200)

        # Draw a small "X" exit button at the bottom of the panel 
        if exit_icon_button.draw(screen):
            run = False # Close game  
                                    
    elif start_game == "GAME OVER":
        if death_fade.fade(): # Only save score once when the game over screen first appears
            add_to_db_score(current_uid, score) # Add this level's score to the total
            score = 0 # Reset score for the next game       
        #  draw a dark  overlay over the game
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))


        # draw the main Panel 
        panel_width, panel_height = 400, 450
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
            
        # gold Border
        pygame.draw.rect(screen, (RED), (panel_x - 5, panel_y - 5, panel_width + 10, panel_height + 10), border_radius=15)
        # wood-colored Background
        pygame.draw.rect(screen, (PINK), (panel_x, panel_y, panel_width, panel_height), border_radius=10)

            
        # header Text
        draw_text("GAME OVER", game_over_font, (RED), panel_x + 50, panel_y - 100 )
        #  shows the score on the victory menu
        draw_text(f"TOTAL SCORE: {new_total}", font, (255, 215, 0), panel_x + 125, panel_y + 50)
            
        # buttons (Positioned inside the panel)
        if play_again_button.draw(screen):
            death_fade.fade_counter = 0 # Reset the fade for next time
            load_and_start_level(level_num) # Reload the current level
            start_game = True # Back to action
            pygame.time.delay(200)

        if main_menu_button.draw(screen):
            death_fade.fade_counter = 0 # Reset the fade for next time
            reset_game()
            start_game = False # Back to title
            pygame.time.delay(200)

        settings_button = button.Button(SCREEN_WIDTH // 2 - 105, SCREEN_HEIGHT // 2 - 130 , settings_img, 0.75)    
        if settings_button.draw(screen):
            start_game = "settings"
            pygame.time.delay(200)

        # Draw a small "X" exit button at the bottom of the panel 
        if exit_icon_button.draw(screen):
            run = False # Close game  
                                    
    elif start_game == True:
        draw_bg()

        # update and draw sprite groups
        decoration_group.update()
        decoration_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)    
        water_group.update()
        water_group.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)
        grenade_group.update()
        grenade_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        hit_marker_group.update()
        hit_marker_group.draw(screen)
        dust_group.update()
        dust_group.draw(screen)

        world.draw()
        draw_player_hud() # calls the hud finction 
        draw_enemy_hud() # calls the enemy hud function




        if player.alive:


            # hit detection
            for bullet in bullet_group:
                if pygame.sprite.collide_rect(player, bullet):
                    if bullet.shooter != player :
                        marker = HitMarker(bullet.rect.centerx, bullet.rect.centery, 0.5)
                        hit_marker_group.add(marker)
                        player.apply_knockback(bullet.rect.centerx)
                        player_damaged_fx.play()
                        bullet.kill()



            hits = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True)
            for enemy in hits:
                if enemy.alive:
                    bullet_list = hits[enemy]
                    for bullet in bullet_list:
                        marker = HitMarker(bullet.rect.centerx, bullet.rect.centery, 0.4)
                        hit_marker_group.add(marker)
                        bot_damaged_fx.play()
                        enemy.apply_knockback(bullet.rect.centerx)

            
            if player.rect.top > SCREEN_HEIGHT or pygame.sprite.spritecollide(player, water_group, False): 
                player.lives -= 1
                player_life_lost_fx.play()
                if player.lives > 0:
                    player.rect.center = (200, 200)
                    player.vel_y = 0
                    player.knockback_timer = 0
                else:
                    player.alive = False # STOPS the loop here so lives don't go to -260
            
            
            # action logic
            if shoot:
                player.shoot()
            elif grenade and grenade_thrown == False and player.grenades > 0:
                p_grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), 
                                    player.rect.top, player.direction)
                grenade_group.add(p_grenade)
                player.grenades -= 1            
                grenade_thrown = True

            # updates player state for animation
            if player.in_air:
                player.update_action(2) 
            elif moving_left or moving_right:
                player.update_action(1) 
            else:        
                player.update_action(0) 

            # move and draw player
            player.move(moving_left, moving_right)
            player.update()
            player.draw()

            for enemy in enemy_group:
                if start_intro == False:
                    enemy.ai(player)

                enemy.update()
                enemy.draw()
                
                # fall logic
                if enemy.rect.top > SCREEN_HEIGHT:
                    enemy.lives -= 1  # Subtract a life
                    
                    if enemy.lives > 0:
                        # Respawns enemys to a safe height
                        enemy.rect.y = 200 
                        enemy.vel_y = 0
                        enemy.knockback_timer = 0
                    else:
                        # only kill them if they are out of lives
                        enemy.kill()
                                    #show intro
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0
            
            if len(enemy_group) == 0 and start_intro == False and player.alive:
                def update_database_score(username, new_score):
                    conn = sqlite3.connect("user.db")
                    cursor = conn.cursor()
                    # Update the score for the specific logged-in user
                    cursor.execute("UPDATE userList SET Score = Score + ? WHERE Username = ?", (new_score, username))
                    conn.commit()
                    conn.close()
                if start_game != "victory":
                    if level_num == 0:
                        score += 500
                    elif level_num == 1:
                        score += 750
                    elif level_num == 2:
                        score += 1000
                    elif level_num == 3:
                        score += 1250

                    print(f"Level {level_num} Complete! Current Score: {score}")
                
                start_game = "victory"

        else:
            if death_fade.fade():
                start_game = "GAME OVER"





# event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #login logic so them the user can type in a username and a password
        if start_game == "login":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == "user":
                        user_text = user_text[:-1]
                    else:
                        pass_text = pass_text[:-1]
                elif event.key == pygame.K_TAB:
                    active_input = "pass" if active_input == "user" else "user"
                elif event.key == pygame.K_RETURN:
                    if len(user_text) > 12:
                        # Clear fields if username is too long
                        user_text = ""
                        pass_text = ""
                    else:
                        # Capture the uID returned by your function
                        logged_in_id = login_user(user_text, pass_text)
                        
                        if logged_in_id is not None:
                            current_user = user_text
                            current_uid = logged_in_id  # This stores the "link" to the leaderboard
                            start_game = False  # SUCCESS: Goes to Main Menu

                   
                        else:
                            # Auto-register if login fails
                            register_user(user_text, pass_text)
                            new_uid = register_user(user_text, pass_text)
                            if new_uid:
                                current_user = user_text
                                current_uid = new_uid
                                start_game = False

                else:
                    # Capture the actual character the user typed
                    if active_input == "user":
                        if len(user_text) < 12:  # Limit username length    
                            user_text += event.unicode
                    else:
                        if len(pass_text) < 12:  # Limit password length
                            pass_text += event.unicode

        #gameplay controls
        if event.type == pygame.KEYDOWN:
            if player: # Check if player exists to prevent errors
                if event.key == pygame.K_a:
                    moving_left = True
                    if not player.in_air:
                        new_dust = Dust(player.rect.centerx, player.rect.bottom)
                        dust_group.add(new_dust) 
                if event.key == pygame.K_d:
                    moving_right = True
                    if not player.in_air:
                        new_dust = Dust(player.rect.centerx, player.rect.bottom)
                        dust_group.add(new_dust) 
                if event.key == pygame.K_t: 
                    shoot = True
                if event.key == pygame.K_y: 
                    grenade = True                                           
                if event.key == pygame.K_w and player.alive:
                    player.jump = True 
                    jump_fx.play()
            
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: moving_left = False 
            if event.key == pygame.K_d: moving_right = False
            if event.key == pygame.K_t: shoot = False
            if event.key == pygame.K_y:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()