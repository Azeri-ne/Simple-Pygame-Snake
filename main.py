import pygame as pg
import random

pg.init()
pg.display.set_caption("Snake")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_running = True

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Text:
	def __init__(self, text, x, y):
		self.text = text
		self.font = pg.font.Font("freesansbold.ttf", 36)
		self.color = (220, 220, 220)
		self.update_display()
		self.x = x
		self.y = y

	def update_display(self):
		self.display = self.font.render(f"{self.text}", True, self.color)

	def draw(self, screen):
		screen.blit(self.display, (self.x, self.y))

	def add_point(self):
		self.text = int(self.text) + 10
		self.update_display()

class Border:
	def __init__(self, width, height):
		self.width = width 
		self.height = height
		self.color = (220, 220, 220)

		self.borders = {
			"top" : pg.Rect((0, height - (height - 40), width, 10)),
			"bottom" : pg.Rect((0, height - 10, width, 10)),
			"left" : pg.Rect((0, height - (height - 40), 10, height - 40)),
			"right" : pg.Rect((width - 10, height - (height - 40), 10, height - 40))
		}

	def draw(self, screen):
		for part in self.borders:
			pg.draw.rect(screen, (self.color), self.borders.get(part))

	def get_collision(self):
		return self.borders

class Snake:
	def __init__(self, x, y, speed, length):
		self.width = 10
		self.height = 10
		self.length = length
		self.body = []
		self.color = (220, 220, 220)
		self.head_color = (40, 250, 50)
		self.speed = speed

		for segment in range(self.length):
			self.body.append(pg.Rect((x - segment * self.width), y, self.width, self.height))

		self.up = False
		self.down = False
		self.left = False
		self.right = True

	def draw(self, screen):
		for segment in self.body:
			if segment == self.body[0]:
				pg.draw.rect(screen, self.head_color, segment)

			else:
				pg.draw.rect(screen, self.color, segment)

	def get_movement(self, event):
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_w and not self.up and not self.down:
				self.up = True
				self.down = False
				self.left = False
				self.right = False

			if event.key == pg.K_s and not self.down and not self.up:
				self.up = False
				self.down = True
				self.left = False
				self.right = False

			if event.key == pg.K_a and not self.left and not self.right:
				self.up = False
				self.down = False
				self.left = True
				self.right = False

			if event.key == pg.K_d and not self.right and not self.left:
				self.up = False
				self.down = False
				self.left = False
				self.right = True


	def detect_collision(self, borders):
		head = self.body[0]

		for part in borders:
			if head.colliderect(borders.get(part)):
				return True

		for segment in self.body[1:]:
			if head.colliderect(segment):
				return True

	def detect_food(self, fruit):
		head = self.body[0]

		if head.colliderect(fruit):
			return True

	def move(self):
		head = self.body[0].copy()

		if self.up:
			head.y -= self.speed

		if self.down:
			head.y += self.speed

		if self.left:
			head.x -= self.speed

		if self.right:
			head.x += self.speed

		self.body.insert(0, head)
		if len(self.body) > self.length:
			self.body.pop()

	def add_segment(self):
		self.length += 1

class Fruit:
	def __init__(self, x_grid, y_grid):
		self.color = (240, 75, 75)

		self.x_grid = x_grid 
		self.y_grid = y_grid
		self.spawn() 

	def spawn(self):
		self.x = random.randint(2, self.x_grid - 2) * 10
		self.y = random.randint(5, self.y_grid - 4) * 10
		self.body = pg.Rect(self.x, self.y, 10, 10) 

	def respawn(self):
		self.spawn()

	def draw(self, screen):
		pg.draw.rect(screen, (self.color), self.body)

	def get_collision(self):
		return self.body


border = Border(SCREEN_WIDTH, SCREEN_HEIGHT)
score_bar = Text("Score:", SCREEN_WIDTH - (SCREEN_WIDTH - 20), SCREEN_HEIGHT - (SCREEN_HEIGHT - 5))
score = Text(0, SCREEN_WIDTH - (SCREEN_WIDTH - 140), SCREEN_HEIGHT - (SCREEN_HEIGHT - 5))
game_over = Text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20)

snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 4)
fruit = Fruit(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10)


while game_running:
	screen.fill((4, 0, 10))
	border.draw(screen)
	score_bar.draw(screen)
	score.draw(screen)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_running = False

		snake.get_movement(event)

	fruit.draw(screen)

	snake.draw(screen)
	snake.move()

	if snake.detect_food(fruit.get_collision()):
		fruit.respawn()
		snake.add_segment()
		score.add_point()

	if snake.detect_collision(border.get_collision()):
		game_over.draw(screen)
		pg.display.update()

		pg.time.wait(1000)
		game_running = False

	pg.display.update()
	pg.time.Clock().tick(30)

pg.quit()