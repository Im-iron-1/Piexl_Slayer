import pygame

pygame.init()

#화면 크기 설정
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width/2-35,screen_height/2-35,35,35)
        self.speed = 10
    def move(self,keys):
        if keys[pygame.K_LEFT]:
            if self.rect.x > self.speed:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.x < screen_width - self.speed - self.rect.width:
                self.rect.x += self.speed
        if keys[pygame.K_UP]:
            if self.rect.y > self.speed:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y < screen_height - self.speed - self.rect.height:
                self.rect.y += self.speed
    def draw(self):
        pygame.draw.rect(screen,(0,255,255),self.rect)

def main():
    running = True
    player = Player()
    while running:
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()