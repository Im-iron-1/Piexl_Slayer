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
        self.rect = pygame.Rect(screen_width/2-35,screen_height/2-35,70,70)
        self.speed = 6
    def move(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
    def draw(self):
        pygame.draw.rect(screen,(0,0,255),self.rect)

def main():
    running = True
    player = Player()
    while running:
        clock.tick(FPS)
        screen.fill((255,255,255))
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