import pygame
import random

pygame.init()

#화면 크기 설정
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))

player_image = pygame.image.load("assets/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (60,60))
lives_image = pygame.image.load("assets/heart.png").convert_alpha()
lives_image = pygame.transform.scale(lives_image,(20,20))
heal_image = pygame.image.load("assets/heal.png").convert_alpha()
heal_image = pygame.transform.scale(heal_image,(40,40))
haste_image = pygame.image.load("assets/haste.png").convert_alpha()
haste_image = pygame.transform.scale(haste_image,(40,40))
shield_image = pygame.image.load("assets/shield.png").convert_alpha()
shield_image = pygame.transform.scale(shield_image,(40,40))
enemy_image = pygame.image.load("assets/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image,(30,30))

pygame.mixer.music.load("assets/bgm.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 60

BAR_X = 30
BAR_Y = 60
BAR_WIDTH = 200
BAR_HEIGHT = 15
BUFF_BAR_WIDTH = 120
BUFF_BAR_HEIGHT = 10
BAR_GAP = 8

SCORE_PER_KILL = 10
score_font = pygame.font.SysFont(None,30)
game_over_font = pygame.font.SysFont(None,60)

HEAL_DROP_RATE = 0.3
HEAL_DURATION = 10 * FPS
HEAL_SIZE = 20
HEAL_COLOR = (50,255,50)
MAX_LIVES = 15
SHIELD_DROP_RATE = 0.1
SHIELD_DURATION = 10 * FPS
SHIELD_SIZE = 15
SHIELD_COLOR = (255,100,100)
HASTE_DROP_RATE = 0.2
HASTE_DURATION = 10 * FPS
HASTE_SIZE = 20
HASTE_COLOR = (255, 255, 0)
MAX_HASTE = 3

class Player:
    def __init__(self):
        self.rect = player_image.get_rect(topleft = (screen_width/2-60, screen_height/2-60))
        self.speed = 10
        self.lives = 3
        self.attack_range = pygame.Rect(self.rect.x-60,self.rect.y-60,120,120)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.shield_timer = 0
        self.using_shield = False
        self.attack_cooldown_base = 3 * FPS
        self.attack_cooldown_max = self.attack_cooldown_base    
        self.haste_timer = 0
        
    def draw_bar(self, x,y,width,height,ratio,color):
        if ratio < 0:
            ratio = 0
        elif ratio > 1:
            ratio = 1
        pygame.draw.rect(screen,(60,60,60),(x,y,width,height))
        pygame.draw.rect(screen,color,(x,y,width*ratio,height))
        pygame.draw.rect(screen,(255,255,255),(x,y,width,height),2)
    
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
            self.attack_cooldown = self.attack_cooldown_max
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
        self.shield_timer = SHIELD_DURATION
        self.using_shield = True
        
    def haste(self):
        self.haste_timer = HASTE_DURATION
        self.attack_cooldown_max = self.attack_cooldown_base * 1/3
            
    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.haste_timer > 0:
            self.haste_timer -= 1
            if self.haste_timer <= 0:
                self.attack_cooldown_max = self.attack_cooldown_base
        if self.using_shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.using_shield = False
                
             
    def draw(self):
        screen.blit(player_image,self.rect)
        #if self.using_shield:
        #    pygame.draw.rect(screen,SHIELD_COLOR,self.rect)
        #else:
        #    pygame.draw.rect(screen,(0,255,255),self.rect)
        if self.attacking:
            pygame.draw.rect(screen,(255,100,100),self.attack_range,2)
        else:
            pygame.draw.rect(screen,(255,255,255),self.attack_range,1)
            
    def draw_hud(self):
        for n in range(self.lives):
            heart = lives_image.get_rect(topleft = (30+30*n,30))
            screen.blit(lives_image,heart)
            
        if self.attack_cooldown <= 0:
            color = (0,255,0)
        elif self.haste_timer > 0:
            color = (255,255,0)
        else:
            color = (255,150,0)
        ratio = 1 - self.attack_cooldown / self.attack_cooldown_max
        self.draw_bar(BAR_X,BAR_Y,BAR_WIDTH,BAR_HEIGHT,ratio,color)
        
        y = BAR_Y + BAR_HEIGHT + BAR_GAP
        if self.haste_timer > 0:
            self.draw_bar(BAR_X,y,BUFF_BAR_WIDTH,BUFF_BAR_HEIGHT,self.haste_timer/HASTE_DURATION,(255,255,0))
            y += BUFF_BAR_HEIGHT + BAR_GAP
        if self.shield_timer > 0:
            self.draw_bar(BAR_X,y,BUFF_BAR_WIDTH,BUFF_BAR_HEIGHT,self.shield_timer/SHIELD_DURATION,(100,200,255))
        
        
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
        screen.blit(enemy_image,self.rect)
        
class HEAL:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 10 * FPS
        
    def update(self):
        self.duration -= 1
        
    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        screen.blit(heal_image,self.rect)
        
class SHIELD:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,15)
        self.duration = 10 * FPS
    
    def update(self):
        self.duration -= 1
        
    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        screen.blit(shield_image,self.rect)

class Haste:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 5 * FPS

    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        screen.blit(haste_image,self.rect)

def draw_score(score):
    text = score_font.render("SCORE : "+str(score),True,(255,255,255))
    screen.blit(text,(screen_width - text.get_width()-30,30))
    
      
def main():
    running = True
    player = Player()
    enemies = [Enemy() for i in range(6)]
    heals = []
    shields = []
    hastes = []
    score = 0
    
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
                if r >= HEAL_DROP_RATE and r < HEAL_DROP_RATE + HASTE_DROP_RATE:
                    hastes.append(Haste(e.rect.centerx - HASTE_SIZE // 2,
                                       e.rect.centery - HEAL_SIZE // 2))
                score += SCORE_PER_KILL
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy())
            enemy_spawn_timer = 0
            
        for i in enemies:
            i.move_towards(player)
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                if player.shield_timer <= 0:
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
                shields.remove(s)
            elif player.rect.colliderect(s.rect):
                player.shield()
                shields.remove(s)
                
        for hs in hastes[:]:
            hs.update()
            if hs.is_expired():
                hastes.remove(hs)
            elif player.rect.colliderect(hs.rect):
                player.haste()
                hastes.remove(hs)
                
        player.update()
        player.draw()
        player.draw_hud()
        
        for e in enemies:
            e.draw()
        
        for heal in heals:
            heal.draw()
            
        for shield in shields:
            shield.draw()
        
        for hs in hastes:
            hs.draw()
        
        score += 0.05
        draw_score(int(score))
        
        if player.lives <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            running = False
            
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()
    
    