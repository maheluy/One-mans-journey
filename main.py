import pygame, sys
from pygame.locals import QUIT
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 525, 370
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Man's Journey")

FPS = 30
VEL = 7
BULLET_VEL = 20
step_count = 0
barrier_creation = 0
enemy_creation = 0
score = 0
kills = 0
game_on = False

PLAYER_HIT = pygame.USEREVENT +1
ENEMY_HIT = pygame.USEREVENT +2
PLAYER_GETS_HEALTH = pygame.USEREVENT +3

BACKGROUND = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('Menu-Background.jpg'), (WIDTH, HEIGHT))

SCORE_FONT = pygame.font.SysFont('roboto', 40)
MENU_FONT = pygame.font.SysFont('arial', 17)
SETTINGS_FONT = pygame.font.SysFont('times new roman', 11)

SOLDIER_WIDTH, SOLDIER_HEIGHT = 45,40
PLAYER_IMAGE = [pygame.image.load('soldado-1.png'), pygame.image.load('soldado-2.png'), pygame.image.load('soldado-3.png')]

BARRIER_WIDTH, BARRIER_HEIGHT = [21,45], [45,21]
all_barrier = []

bullets_player_up, bullets_player_down, bullets_player_left, bullets_player_right = [], [], [], []
bullets_enemy_up, bullets_enemy_down, bullets_enemy_left, bullets_enemy_right = [], [], [], []

health_packages = []

PLAYER_TOTAL_HEALTH = 100
player_health = 100  #variavel conforme hits
BULLET_DAMAGE = 10
add_health = 10
  
#o nome enemys é dado como parametro, mas na chamada da função é usado enemy.enemys
def bullet_movement(player, enemys):   
  for bullet_up in bullets_player_up:      #DO JOGADOR PARA CIMA
    bullet_up.y -= BULLET_VEL
    for barrier in all_barrier:
      if bullet_up.colliderect(barrier):
        bullets_player_up.remove(bullet_up)
        break  #sempre ha apenas uma bala, evita colisão em sobrepostas, em caso de múltiplas balas, usar if para usar break quando a primeira colidir
    if bullet_up.y < -300:
      bullets_player_up.remove(bullet_up)
    for enemy in enemys:
      if bullet_up.colliderect(enemy.Rect):
        pygame.event.post(pygame.event.Event(ENEMY_HIT))
        loot_chance = random.randint(1,5)
        if loot_chance == 4:
          health_package_creation(enemy)
        enemys.remove(enemy)
        bullets_player_up.remove(bullet_up)
        break
  for bullet_down in bullets_player_down:     #DO JOGADOR PARA BAIXO
    bullet_down.y += BULLET_VEL
    for barrier in all_barrier:
      if bullet_down.colliderect(barrier):
        bullets_player_down.remove(bullet_down)
        break
    if bullet_down.y > HEIGHT + 300:
      bullets_player_down.remove(bullet_down)
    for enemy in enemys:
      if bullet_down.colliderect(enemy.Rect):
        pygame.event.post(pygame.event.Event(ENEMY_HIT))
        loot_chance = random.randint(1,5)
        if loot_chance == 4:
          health_package_creation(enemy)
        enemys.remove(enemy)
        bullets_player_down.remove(bullet_down)
        break
  for bullet_right in bullets_player_right:     #DO JOGADOR PARA DIREITA
    bullet_right.x += BULLET_VEL
    for barrier in all_barrier:
      if bullet_right.colliderect(barrier):
        bullets_player_right.remove(bullet_right)
        break
    if bullet_right.x > WIDTH + 300:
      bullets_player_right.remove(bullet_right)
    for enemy in enemys:
      if bullet_right.colliderect(enemy.Rect):
        pygame.event.post(pygame.event.Event(ENEMY_HIT))
        loot_chance = random.randint(1,5)
        if loot_chance == 4:
          health_package_creation(enemy)
        enemys.remove(enemy)
        bullets_player_right.remove(bullet_right)
        break
  for bullet_left in bullets_player_left:      #DO JOGADOR PARA ESQUERDA
    bullet_left.x -= BULLET_VEL
    for barrier in all_barrier:
      if bullet_left.colliderect(barrier):
        bullets_player_left.remove(bullet_left)
        break
    if bullet_left.x < -300:
      bullets_player_left.remove(bullet_left)
    for enemy in enemys:
      if bullet_left.colliderect(enemy.Rect):
        pygame.event.post(pygame.event.Event(ENEMY_HIT))
        loot_chance = random.randint(1,5)
        if loot_chance == 4:
          health_package_creation(enemy)
        enemys.remove(enemy)
        bullets_player_left.remove(bullet_left)
        break

  for bullet_up in bullets_enemy_up:    #DO INIMIGO PARA CIMA
    bullet_up.y -= BULLET_VEL
    for barrier in all_barrier:
      if bullet_up.colliderect(barrier):
        bullets_enemy_up.remove(bullet_up)
        break
    if bullet_up.y < -300:
      bullets_enemy_up.remove(bullet_up)
    if bullet_up.colliderect(player):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
      bullets_enemy_up.remove(bullet_up)
      break
  for bullet_down in bullets_enemy_down:   #DO INIMIGO PARA BAIXO
    bullet_down.y += BULLET_VEL
    for barrier in all_barrier:
      if bullet_down.colliderect(barrier):
        bullets_enemy_down.remove(bullet_down)
        break
    if bullet_down.y > HEIGHT+300:
      bullets_enemy_down.remove(bullet_down)
      break
    if bullet_down.colliderect(player):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
      bullets_enemy_down.remove(bullet_down)
  for bullet_right in bullets_enemy_right:   #DO INIMIGO PARA DIREITA
    bullet_right.x += BULLET_VEL
    for barrier in all_barrier:
      if bullet_right.colliderect(barrier):
        bullets_enemy_right.remove(bullet_right)
        break
    if bullet_right.x > WIDTH + 300:
      bullets_enemy_right.remove(bullet_right)
    if bullet_right.colliderect(player):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
      bullets_enemy_right.remove(bullet_right)
      break
  for bullet_left in bullets_enemy_left:      #DO INIMGO PARA ESQUERDA
    bullet_left.x -= BULLET_VEL
    for barrier in all_barrier:
      if bullet_left.colliderect(barrier):
        bullets_enemy_left.remove(bullet_left)
        break
    if bullet_left.x < -300:
      if (len(bullets_enemy_left) > 0):
        bullets_enemy_left.remove(bullet_left)
    if bullet_left.colliderect(player):
      pygame.event.post(pygame.event.Event(PLAYER_HIT))
      bullets_enemy_left.remove(bullet_left)
      break

def health_package_creation(enemy):
  health_package = pygame.Rect(enemy.Rect.x, enemy.Rect.y, 15,15)
  health_packages.append(health_package)
  
  
def barrier_position():
  barrier_idx = random.randint(0,1)
  barrier_y = random.randint(30,HEIGHT - 90)
  barrier = pygame.Rect(WIDTH + 100, barrier_y, BARRIER_WIDTH[barrier_idx], BARRIER_HEIGHT[barrier_idx])
  all_barrier.append(barrier)
  


class enemy():
  enemys = []

  def __init__(self):
    self.Rect = pygame.Rect(WIDTH + 200, random.randint(30,285), SOLDIER_WIDTH, SOLDIER_HEIGHT)
    self.step_count = 0
    enemy.enemys.append(self)
    self.movement_time = 0

  def position():
    self = enemy()
    return self

  def movement(self):
    direction_value = random.randint(0,3)
    if direction_value == 0 and self.Rect.y - VEL > 30: #CIMA
      self.Rect.y -= VEL
      self.step_count +=1
      for j in all_barrier:
        if self.Rect.colliderect(j):
          self.Rect.y +=VEL
          self.step_count-=1
    if direction_value == 1 and self.Rect.y + VEL < WIDTH - 140 - SOLDIER_HEIGHT*2: #BAIXO
      self.Rect.y += VEL
      self.step_count +=1
      for j in all_barrier:
        if self.Rect.colliderect(j):
          self.Rect.y -=VEL
          self.step_count-=1
    if direction_value == 2: #DIREITA
      self.Rect.x += VEL
      self.step_count +=1
      for j in all_barrier:
        if self.Rect.colliderect(j):
          self.Rect.x -=VEL
          self.step_count-=1
    if direction_value == 3: #ESQUERDA
      self.Rect.x -= VEL
      self.step_count +=1
      for j in all_barrier:
        if self.Rect.colliderect(j):
          self.Rect.x +=VEL
          self.step_count-=1
          

  def shoot(self, player):        
    if 0 < self.Rect.x - player.x < 400 and (self.Rect.y <= player.y <= self.Rect.y+self.Rect.height or self.Rect.y <= player.y+player.height <= self.Rect.y+self.Rect.height) and len(bullets_enemy_up)+len(bullets_enemy_down)+ len(bullets_enemy_right)+ len(bullets_enemy_left) < 1:  
      bullet = pygame.Rect(self.Rect.x, self.Rect.y + self.Rect.height//2 -2, 10, 5)
      bullets_enemy_left.append(bullet)   #LEFT
      
    if 0 > self.Rect.x - player.x > -400 and (self.Rect.y <= player.y <= self.Rect.y+self.Rect.height or self.Rect.y <= player.y+player.height <= self.Rect.y+self.Rect.height) and len(bullets_enemy_up)+len(bullets_enemy_down)+ len(bullets_enemy_right)+ len(bullets_enemy_left) < 1:
      bullet = pygame.Rect(self.Rect.x + self.Rect.width, self.Rect.y + self.Rect.height//2 -2, 10, 5)
      bullets_enemy_right.append(bullet)  #RIGHT
      
    if 0 < self.Rect.y - player.y < 200 and (self.Rect.x <= player.x <= self.Rect.x+self.Rect.width or self.Rect.x <= player.x+player.width <= self.Rect.x+self.Rect.width) and len(bullets_enemy_up)+len(bullets_enemy_down)+ len(bullets_enemy_right)+ len(bullets_enemy_left) < 1: 
      bullet = pygame.Rect(self.Rect.x + self.Rect.width//2 -2, self.Rect.y, 5, 10)
      bullets_enemy_up.append(bullet)     #UP
      
    if 0 > self.Rect.y - player.y > -200 and (self.Rect.x <= player.x <= self.Rect.x+self.Rect.width or self.Rect.x <= player.x+player.width <= self.Rect.x+self.Rect.width) and len(bullets_enemy_up)+len(bullets_enemy_down)+ len(bullets_enemy_right)+ len(bullets_enemy_left) < 1:
      bullet = pygame.Rect(self.Rect.x + self.Rect.width//2 -2, self.Rect.y + self.Rect.height, 5, 10)
      bullets_enemy_down.append(bullet)    #DOWN
      

  

def draw_window(player):
  global step_count
  WINDOW.blit(BACKGROUND, (0,0))
  score_text = SCORE_FONT.render("Score: " + str(int(score)), 1, (0,0,0))
  WINDOW.blit(score_text, (10, 10))
  kills_text = SCORE_FONT.render("Kills: " + str(int(kills)), 1, (0,0,0))
  WINDOW.blit(kills_text, (10,340))
  #pygame.draw.rect(WINDOW, (255,0,0), (player.x, player.y, player.width, player.height))  

  if step_count +1 > 9 or step_count -1 < 0:
    step_count = 0
  WINDOW.blit(pygame.transform.scale(PLAYER_IMAGE[step_count//3], (SOLDIER_WIDTH, SOLDIER_HEIGHT)), (player.x, player.y)) #Jogador

  for i in range(len(all_barrier)-1):
    pygame.draw.rect(WINDOW, (60,60,60), (all_barrier[i].x, all_barrier[i].y, all_barrier[i].width, all_barrier[i].height))    #barreira

  for bullet in bullets_player_up+bullets_player_down+bullets_player_right+bullets_player_left+bullets_enemy_up+bullets_enemy_down+bullets_enemy_right+bullets_enemy_left:
    pygame.draw.rect(WINDOW, (255,255,0), bullet)    #balas

  for each_enemy in enemy.enemys:              #inimigos
    if each_enemy.step_count +1 > 9 or each_enemy.step_count -1 < 0:
      each_enemy.step_count = 0
    WINDOW.blit(pygame.transform.flip(pygame.transform.scale(PLAYER_IMAGE[each_enemy.step_count//3], (SOLDIER_WIDTH, SOLDIER_HEIGHT)), True, False), (each_enemy.Rect.x, each_enemy.Rect.y))

  health_total_rect = pygame.Rect(HEIGHT - 10, 15, PLAYER_TOTAL_HEALTH, 10)
  health_rect = pygame.Rect(HEIGHT-10, 15, player_health, 10)
  pygame.draw.rect(WINDOW, (255,0,0), health_total_rect)
  pygame.draw.rect(WINDOW, (0,255,0), health_rect)
  
  for health_pack in health_packages:
    pygame.draw.rect(WINDOW, (0,255,0), health_pack)
  
  pygame.display.update()


def player_movement(key_pressed, player):
  global step_count
  global score
  global enemys
  if key_pressed[pygame.K_w] and player.y -VEL  >30:  #CIMA
    player.y -= VEL
    step_count+=1
    for j in all_barrier:
      if player.colliderect(j):
        player.y +=VEL
        step_count-=1
    for health in health_packages:
      if health.colliderect(player):
        pygame.event.post(pygame.event.Event(PLAYER_GETS_HEALTH))
        health_packages.remove(health)
  if key_pressed[pygame.K_s] and player.y +VEL  < WIDTH - 140 - SOLDIER_HEIGHT*2:  #BAIXO
    player.y += VEL
    step_count+=1
    for j in all_barrier:
      if player.colliderect(j):
        player.y -=VEL
        step_count-=1
    for health in health_packages:
      if health.colliderect(player):
        pygame.event.post(pygame.event.Event(PLAYER_GETS_HEALTH))
        health_packages.remove(health)
        
  if key_pressed[pygame.K_d]:    #DIREITA
    for i in range(len(all_barrier)-1):
      all_barrier[i].x -=VEL
      if player.colliderect(all_barrier[i]):
        for j in all_barrier:
          j.x +=VEL
        step_count-=1
        score-=0.05
        for e in enemy.enemys:
          e.Rect.x+=VEL
        for health in health_packages:
          health.x+=VEL
    step_count+=1
    score +=0.05
    for e in enemy.enemys:
      e.Rect.x -= VEL
    for health in health_packages:
      health.x -= VEL
      if health.colliderect(player):
        pygame.event.post(pygame.event.Event(PLAYER_GETS_HEALTH))
        health_packages.remove(health)

  if key_pressed[pygame.K_a]:     #ESQUERDA
    for i in range(len(all_barrier)-1):
      all_barrier[i].x +=VEL
      if player.colliderect(all_barrier[i]):
        for j in all_barrier:
          j.x -=VEL
        step_count-=1
        score+=0.05
        for e in enemy.enemys:
          e.Rect.x-=VEL
        for health in health_packages:
          health.x-=VEL
    step_count+=1
    score -=0.05
    for e in enemy.enemys:
      e.Rect.x += VEL
    for health in health_packages:
      health.x += VEL
      if health.colliderect(player):
        pygame.event.post(pygame.event.Event(PLAYER_GETS_HEALTH))
        health_packages.remove(health)



def draw_menu():
  WINDOW.blit(MENU_BACKGROUND, (0,0))
  title_text = SCORE_FONT.render("One Man's Journey", 1, (39,64,139))
  pygame.draw.rect(WINDOW,(255,239,219), (5,5,265,35))
  WINDOW.blit(title_text, (10,10))

  play_text = SCORE_FONT.render("Pressione ESPAÇO para Jogar", 1, (0,0,0))
  WINDOW.blit(play_text, (50,315))

  how_to_play_text = MENU_FONT.render("COMO JOGAR:", 1, (39,64,149))
  w_text = MENU_FONT.render('W: Mover para Cima', 1, (39,64,149))
  a_text = MENU_FONT.render('A: Mover para Esquerda', 1, (39,64,149))
  s_text = MENU_FONT.render('S: Mover para Baixo', 1, (39,64,149))
  d_text = MENU_FONT.render('D: Mover para Direita', 1, (39,64,149))
  arrow_up_text = MENU_FONT.render('^: Atirar para Cima', 1, (39,64,149))
  arrow_left_text = MENU_FONT.render('<: Atirar para Esquerda', 1, (39,64,149))
  arrow_down_text = MENU_FONT.render('v: Atirar para Baixo', 1, (39,64,149))
  arrow_right_text = MENU_FONT.render('>: Atirar para Direita', 1, (39,64,149))
  pygame.draw.rect(WINDOW, (156,102,31), (315, 5, 210, 210))
  pygame.draw.rect(WINDOW, (250,235,215), (320, 10, 200, 200))
  WINDOW.blit(how_to_play_text, (360, 15))
  WINDOW.blit(w_text, (330, 37))
  WINDOW.blit(a_text, (330, 59))
  WINDOW.blit(s_text, (330, 81))
  WINDOW.blit(d_text, (330, 103))
  WINDOW.blit(arrow_up_text, (330, 125))
  WINDOW.blit(arrow_left_text, (330, 147))
  WINDOW.blit(arrow_down_text, (330, 169))
  WINDOW.blit(arrow_right_text, (330, 191))


  settings_text = SETTINGS_FONT.render('Selecione Dificuldade', 1, (39,64,139))
  facil_text = SETTINGS_FONT.render('Fácil     ^', 1, (39,64,139))
  medio_text = SETTINGS_FONT.render('Médio', 1, (39,64,139))
  dificil_text = SETTINGS_FONT.render('Difícil    v', 1, (39,64,139))
  WINDOW.blit(settings_text, (7,45))
  WINDOW.blit(facil_text, (7,57))
  WINDOW.blit(medio_text, (7,69))
  WINDOW.blit(dificil_text, (7,81))
  
  pygame.display.update()
  

def main():
  global barrier_creation, enemy_creation, player_health, kills, score, game_on
  global bullets_player_up, bullets_player_down, bullets_player_left, bullets_player_right 
  global bullets_enemy_up, bullets_enemy_down, bullets_enemy_left, bullets_enemy_right
  
  player = pygame.Rect(50, 140, SOLDIER_WIDTH, SOLDIER_HEIGHT)
  difficulty_text = pygame.Rect(45,74,5,5)
  
  clock = pygame.time.Clock()  
  run = True
  while run:
    key_pressed = pygame.key.get_pressed()
    clock.tick(FPS)

    if game_on == False:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            barrier_creation, enemy_creation, player_health, kills, score, player.y = 0,0,100,0,0,140     #Reseta variaveis e listas
            while len(all_barrier) > 2: all_barrier.remove(all_barrier[len(all_barrier)-1])
            while len(enemy.enemys) > 0: enemy.enemys.remove(enemy.enemys[len(enemy.enemys)-1])
            bullets_player_up, bullets_player_down, bullets_player_left, bullets_player_right = [], [], [], []
            bullets_enemy_up, bullets_enemy_down, bullets_enemy_left, bullets_enemy_right = [], [], [], []
            while len(health_packages) > 0: health_packages.remove(health_packages[len(health_packages)-1])
            game_on = True
          
          if event.key == pygame.K_UP:
            difficulty_text.y -= 11
          if event.key == pygame.K_DOWN:
            difficulty_text.y += 11           # difficulty_text; 63=Facil, 74=Medio, 85=Dificil
          if difficulty_text.y > 85: difficulty_text.y = 74
          if difficulty_text.y < 63: difficulty_text.y = 74

        if difficulty_text.y == 63:
          difficulty_damage = -5
          enemy_created = 25
        if difficulty_text.y == 74:
          difficulty_damage = 0
          enemy_created = 20
        if difficulty_text.y == 85:
          difficulty_damage = 15
          enemy_created = 15
          
      draw_menu()
      pygame.draw.rect(WINDOW, (255,239,219), difficulty_text)
      pygame.display.update()
    
    if game_on == True:
      for event in pygame.event.get():
        if event.type == QUIT:
          run = False
          pygame.quit()
          sys.exit()
          
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP and len(bullets_player_up)+len(bullets_player_down)+len(bullets_player_right)+len(bullets_player_left) <= 0:         
            bullet = pygame.Rect(player.x + player.width//2, player.y, 5, 10)
            bullets_player_up.append(bullet)
          if event.key == pygame.K_DOWN and len(bullets_player_up)+len(bullets_player_down)+len(bullets_player_right)+len(bullets_player_left) <= 0:         
            bullet = pygame.Rect(player.x + player.width//2, player.y + player.height, 5, 10)
            bullets_player_down.append(bullet)
          if event.key == pygame.K_RIGHT and len(bullets_player_up)+len(bullets_player_down)+len(bullets_player_right)+len(bullets_player_left) <= 0:         
            bullet = pygame.Rect(player.x + player.width, player.y +player.height//2 -2, 10, 5)
            bullets_player_right.append(bullet)
          if event.key == pygame.K_LEFT and len(bullets_player_up)+len(bullets_player_down)+len(bullets_player_right)+len(bullets_player_left) <= 0:
            bullet = pygame.Rect(player.x, player.y + player.height//2 - 2, 10, 5)
            bullets_player_left.append(bullet)
  
        if event.type == PLAYER_HIT:
          player_health -= BULLET_DAMAGE + difficulty_damage
        if event.type == ENEMY_HIT:
          kills += 1
        if event.type == PLAYER_GETS_HEALTH:
          player_health += add_health
  
        if player_health > PLAYER_TOTAL_HEALTH:
          player_health = PLAYER_TOTAL_HEALTH

        if player_health <= 0:
          death_text = SCORE_FONT.render("DEAD", 1, (255,0,0))
          draw_window(player)
          WINDOW.blit(death_text, (200,100))
          pygame.display.update()
          pygame.time.delay(7000)
          game_on = False
       
      bullet_movement(player, enemy.enemys)
      player_movement(key_pressed, player)
  
      
      for enem in enemy.enemys:
        if enem.movement_time > 3:
          enem.movement_time = 0
        if enem.movement_time == 3:
          enem.movement()
          enemy.shoot(enem, player)
        enem.movement_time +=1
  
      if step_count == 9:
        barrier_creation +=1
      if barrier_creation == 6:
        barrier_position()
        barrier_creation = 0
  
      if step_count == 9:
        enemy_creation +=1
      if enemy_creation == enemy_created:   #enemy_created dependente da dificuldade
        enemy.position()
        enemy_creation = 0
        
      draw_window(player)
      
      if len(all_barrier) >35:
        all_barrier.remove(all_barrier[0])

    

if __name__ == "__main__":
  main()
