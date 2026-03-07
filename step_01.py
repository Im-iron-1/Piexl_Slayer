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
    def draw(self):
        pygame.draw.rect(screen,(0,0,255),self.rect)

def main():
    running = True
    player = Player()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player.draw()
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()