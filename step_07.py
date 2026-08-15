import pygame
import random

pygame.init()

#화면 크기 설정
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

HEAL_DROP_RATE = 0.3
HEAL_DURATION = 10 * FPS
HEAL_SIZE = 20
HEAL_COLOR = (50,255,50)
MAX_LIVES = 5
SHIELD_DROP_RATE = 0.1
SHIELD_DURATION = 10 * FPS
SHIELD_SIZE = 15
SHIELD_COLOR = (255,255,0)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width/2-30,screen_height/2-30,30,30)
        self.speed = 10
        self.lives = 3
        self.attack_range = pygame.Rect(self.rect.x - 30, self.rect.y-30,100,100)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.shield_duration = 0
        self.using_shield = False
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
        self.attack_range.topleft = (self.rect.x -30, self.rect.y - 30)
        
    def attack(self,enemies):
        killed = []
        if not self.attacking and self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 15
            self.attack_cooldown = 60
            new_enemies = []
            for e in enemies:
                if self.attack_range.colliderect(e.rect):
                    killed.append(e)
                else:
                    new_enemies.append(e)
            enemies[:] = new_enemies
        return killed
    
    def heal(self):
        self.lives = min(self.lives + 1,MAX_LIVES)
        
    def shield(self):
        self.shield_duration = 300
        self.using_shield = True
            
    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.using_shield:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                self.using_shield = False
                
             
    def draw(self):
        if self.using_shield:
            pygame.draw.rect(screen,SHIELD_COLOR,self.rect)
        else:
            pygame.draw.rect(screen,(0,255,255),self.rect)
        if self.attacking:
            pygame.draw.rect(screen,(255,100,100),self.attack_range,2)
        else:
            pygame.draw.rect(screen,(255,255,255),self.attack_range,1)
        for n in range(self.lives):
            pygame.draw.rect(screen,(255,0,0),(30+30*n,30,20,20))
        
        
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0,screen_width-30),random.randint(0,screen_height-30),30,30)
        self.speed = 1
    def move_towards(self,target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed
    def draw(self):
        pygame.draw.rect(screen,(255,0,0),self.rect)
        
class HEAL:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 10 * FPS
        
    def update(self):
        self.duration -= 1
        
    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        pygame.draw.rect(screen,HEAL_COLOR,self.rect)
        
class SHIELD:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,15)
        self.duration = 10 * FPS
    
    def update(self):
        self.duration -= 1
        
    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        pygame.draw.rect(screen,SHIELD_COLOR,self.rect)
      
def main():
    running = True
    player = Player()
    enemies = [Enemy() for i in range(6)]
    heals = []
    shields = []
    
    enemy_spawn_timer = 0
    enemy_spawn_interval = 70
    
    while running:
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]:
            killed = player.attack(enemies)
            for e in killed:
                r = random.random()
                if r<HEAL_DROP_RATE:
                    heals.append(HEAL(e.rect.centerx - HEAL_SIZE//2,
                                      e.rect.centery - HEAL_SIZE//2))
                if r>1-SHIELD_DROP_RATE:
                    shields.append(SHIELD(e.rect.centerx - SHIELD_SIZE//2,
                                          e.rect.centery - SHIELD_SIZE//2))
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy())
            enemy_spawn_timer = 0
            
        for i in enemies:
            i.move_towards(player)
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                if player.shield_duration <= 0:
                    player.lives -=1
                    enemies.remove(enemy)
                
        for h in heals[:]:
            h.update()
            if h.is_expired():
                heals.remove(h)
            elif player.rect.colliderect(h.rect):
                player.heal()
                heals.remove(h)
        
        for s in shields[:]:
            s.update()
            if s.is_expired():
                shields.remove(h)
            elif player.rect.colliderect(s.rect):
                player.shield()
                shields.remove(s)
                
        player.update()
        player.draw()
        
        for e in enemies:
            e.draw()
        
        for heal in heals:
            heal.draw()
            
        for shield in shields:
            shield.draw()
        
        
        if player.lives <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            running = False
            
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()