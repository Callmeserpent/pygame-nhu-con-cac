#setup
import pygame,sys,random
clock = pygame.time.Clock()
from pygame.locals import *
from pygame import mixer
pygame.init()
game_font = pygame.font.Font(r'C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\04B_19.ttf',40)

pygame.display.set_caption("Fappy Bird")
screen = pygame.display.set_mode((360, 640))
icon = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\favicon.ico")
pygame.display.set_icon(icon)

#game variables
floor_x_pos = 0
gravity = 0.25
bird_movement = 0
pipe_list = []
spawnpipe = pygame.USEREVENT
pipe_height = [250, 300, 360, 460]
game_active = True
bird_index = 0
birdflap = pygame.USEREVENT + 1
score = 0
high_score = 0
flap_sound = pygame.mixer.Sound(r'C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\audio\swoosh.ogg')

#background
bg_surface = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (360,640))
floor_surface = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (360, 140))


def draw_floor():
  screen.blit(floor_surface, (floor_x_pos, 510))
  screen.blit(floor_surface, (floor_x_pos + 360, 510))

def create_pipe():
  random_pipe_pos = random.choice(pipe_height)
  bottom_pipe = pipe_surface.get_rect(midtop = (400, random_pipe_pos)) 
  top_pipe = pipe_surface.get_rect(midbottom = (400, random_pipe_pos-200)) 
  return bottom_pipe, top_pipe

def move_pipes(pipes):
  for pipe in pipes:
    pipe.centerx -= 4
  return pipes  

def draw_pipes(pipes):
  for pipe in pipes:
    if pipe.bottom >= 640:
     screen.blit(pipe_surface, pipe)
    else:
     flip_pipe = pygame.transform.flip(pipe_surface, False, True)
     screen.blit(flip_pipe,pipe)

def check_collision(pipes):
  for pipe in pipes:
    if bird_rect.colliderect(pipe):
      return False

  if bird_rect.top <= -100 or bird_rect.bottom >= 510:
    return False

  return True  

def rotate_bird(bird):
  new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
  return new_bird

def bird_animation():
  new_bird = bird_frames[bird_index]
  new_bird_rect = new_bird.get_rect(center = (70, bird_rect.centery))
  return new_bird, new_bird_rect

def score_display(game_state):
  if game_state == 'main game':
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (180, 50))
    screen.blit(score_surface, score_rect)
  if game_state == 'game over':
    score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (180, 50))
    screen.blit(score_surface, score_rect)

    highscore_surface = game_font.render(f'High Score:{int(high_score)}', True, (255, 255, 255))
    highscore_rect = highscore_surface.get_rect(center = (180, 480))
    screen.blit(highscore_surface, highscore_rect)  

def update_score(score, high_score):
  if score > high_score:
    high_score =score
  return high_score  

#bird

#bird_surface = pygame.image.load(r'C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\yellowbird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale(bird_surface, (42,30))
#bird_rect = bird_surface.get_rect(center = (70, 290))

bird_downflap = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\yellowbird-downflap.png").convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (42, 30))
bird_midflap = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\yellowbird-midflap.png").convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (42,30))
bird_upflap = pygame.image.load(r"C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\yellowbird-upflap.png").convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (42, 30))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (70, 290))
pygame.time.set_timer(birdflap, 200)

#pipes
pipe_surface = pygame.image.load(r'C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (65, 400))
pygame.time.set_timer(spawnpipe,1200)

#details
game_over_surface = pygame.image.load(r'C:\Users\DELL\vscodeproject\pygamenhuconcac\Fapkochim\flappy-bird-assets-master\flappy-bird-assets-master\sprites\message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (180, 250))

#gameloop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_SPACE:
        bird_movement = 0
        bird_movement -= 5  

      if event.key == pygame.K_SPACE and game_active == False:
        game_active = True
        pipe_list.clear()
        bird_rect.center = (70, 290)
        bird_movement = 0
        score = 0

    if event.type == spawnpipe:
      pipe_list.extend(create_pipe())
    if event.type == birdflap:
      if bird_index < 2:
        bird_index += 1
      else:
        bird_index = 0
      
      bird_surface, bird_rect = bird_animation()

  screen.blit(bg_surface, (0, 0))
  
  if game_active:
#bird  
    bird_movement += gravity
    rotated_bird = rotate_bird(bird_surface)
    bird_rect.centery += bird_movement
    screen.blit(rotated_bird, bird_rect)
#pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)
#score
    score += 0.01
    score_display('main game')
  else:
    screen.blit(game_over_surface, game_over_rect)
    high_score = update_score(score, high_score)
    score_display('game over')  
#floor
  floor_x_pos -= 2
  draw_floor()
  if floor_x_pos <= -360:
    floor_x_pos = 0
#collision
  game_active = check_collision(pipe_list)

  clock.tick(60)
  pygame.display.update()  