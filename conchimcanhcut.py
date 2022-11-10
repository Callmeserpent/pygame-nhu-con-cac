import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((40,40))
		self.image.fill((200,30,30))
		self.rect = self.image.get_rect(center = (250,250))
		self.current_health = 200
		self.target_health = 500
		self.max_health = 1000
		self.health_bar_length = 250
		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5

	def get_damage(self,amount):
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0

	def get_health(self,amount):
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health

	def update(self):
		#self.basic_health()
		self.advanced_health()
		
	def basic_health(self):
		pygame.draw.rect(screen,(255,0,0),(10,10,self.target_health / self.health_ratio,10))
		pygame.draw.rect(screen,(255,255,255),(10,10,self.health_bar_length,10),2)

	def advanced_health(self):
		transition_width = 0
		transition_color = (255,0,0)

		if self.current_health < self.target_health:
			self.current_health += self.health_change_speed
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (0,255,0)

		if self.current_health > self.target_health:
			self.current_health -= self.health_change_speed 
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (255,255,0)

		health_bar_width = int(self.current_health / self.health_ratio)
		health_bar = pygame.Rect(10,10,health_bar_width,10)
		transition_bar = pygame.Rect(health_bar.right,10,transition_width,10)
		
		pygame.draw.rect(screen,(255,0,0),health_bar)
		pygame.draw.rect(screen,transition_color,transition_bar)	
		pygame.draw.rect(screen,(255,255,255),(10,10,self.health_bar_length,10),4)	

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Health bar-DarkSoul type')
screen = pygame.display.set_mode((500, 500), 0, 32)
player = pygame.sprite.GroupSingle(Player())

while True:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_UP:
        player.sprite.get_health(100)
      if event.key == pygame.K_DOWN:
        player.sprite.get_damage(100)  
  
  screen.fill((30, 30, 30))
  player.draw(screen)
  player.update()
  clock.tick(60)        
  pygame.display.update()