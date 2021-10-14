import pygame
import random

class Collector:
    window_x = 1080
    window_y = 780

    def __init__(self):
        pygame.init()
        self.load_images()
        self.new_game()

        self.map_height = Collector.window_y
        self.map_width = Collector.window_x

        self.display = pygame.display.set_mode((self.map_width, self.map_height))
        pygame.display.set_caption("Collector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.init_enemies()
        self.init_coin()
        self.score = 0
        self.game_end = False

        self.right = False    #Robots movements
        self.left = False
        self.up = False
        self.down = False

        self.game_loop()
        

    def load_images(self):
        self.images = []
        for name in ["robo", "hirvio", "kolikko", "ovi"]:
            self.images.append(pygame.image.load(name + ".png"))        

    def init_enemies(self):
        self.enemies = []
        for i in range(4):
            self.enemies.append([0, 0]) 
        #initialise enemies' coordinates
        for i in range(4):
            self.enemies[i] = [350 * i + self.images[1].get_width(), self.images[1].get_height()]

    def update_enemies(self):
        speed = 3
        for enemy in self.enemies:
            if self.x > enemy[0]:
                enemy[0] += speed
            if self.x < enemy[0]:
                enemy[0] -= speed
            if self.y > enemy[1]:
                enemy[1] += speed
            if self.y < enemy[1]:
                enemy[1] -= speed

    def init_coin(self):
        #initialise coin coordinates so that it can't be out of bounds
        self.coin_x = random.randint(self.images[2].get_width(),
         Collector.window_x - self.images[2].get_width())
        self.coin_y = random.randint(self.images[2].get_height(),
         Collector.window_y - self.images[2].get_height())   

    def update_coin(self):
        if self.x <= self.coin_x <= self.x + self.images[0].get_width():
            if self.y <= self.coin_y <= self.y + self.images[1].get_height():
                self.init_coin()
                self.score += 1

    def update_robot(self):
        if self.game_end:
            return
        speed = 8
        #robot's movements
        if self.right and (self.x < self.map_width - self.images[0].get_width()):
            self.x += speed
        if self.left and (self.x > 0):
            self.x -= speed
        if self.up and (self.y > 0):
            self.y -= speed
        if self.down and (self.y < self.map_height - self.images[0].get_height()):
            self.y += speed


    def should_die(self):
        for enemy in self.enemies:
            if enemy[0] <= self.x <= enemy[0] + self.images[1].get_width():                
                if enemy[1] <= self.y <= enemy[1] + self.images[1].get_height():
                    self.game_over()

    def new_game(self):
        self.x = Collector.window_x // 2   #robot's x coordinate
        self.y = Collector.window_y // 2   #robot's y coordinate

    def game_over(self):
        self.game_end = True

    def restart(self):
        self.font = pygame.font.SysFont("Arial", 24)
        self.game_end = False
        self.new_game()
        self.init_enemies()
        self.score = 0

    def game_loop(self):
        while True:
            self.events()
            self.update_robot()
            self.update_coin()
            self.update_enemies()
            self.should_die()
            self.update_display()
            
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_r:
                    self.restart()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False
                if event.key == pygame.K_UP:
                    self.up = False
                if event.key == pygame.K_DOWN:
                    self.down = False


    def update_display(self):
        self.display.fill((109,232,104))

        self.display.blit(self.images[0], (self.x, self.y))  #draw robot

        for enemy in self.enemies:  #draw enemies
            self.display.blit(self.images[1], (enemy[0], enemy[1]))

        self.display.blit(self.images[2], (self.coin_x, self.coin_y))  #draw coin

        #draw score
        text = self.font.render("Pisteet: " + str(self.score), True, (255, 0, 0))
        self.display.blit(text, (self.map_width - 150, self.map_height - 35))
        self.display

        #game over messages
        if self.game_end:
            self.display.fill((109,232,104))
            self.font = pygame.font.SysFont("Arial", 50)
            text = self.font.render("You died!", True, (255, 0, 0))
            self.display.blit(text, (self.map_width //2 - 120, self.map_height//2 -100))
            text = self.font.render("Your score: " + str(self.score), True, (255, 0, 0))
            self.display.blit(text, (self.map_width //2 -120, self.map_height//2 -50))
            text = self.font.render("Restart with R" , True, (255, 0, 0))
            self.display.blit(text, (self.map_width //2 -120, self.map_height//2))

        pygame.display.flip()

        
if __name__ == "__main__":
    Collector()