#---coding:utf-8----

# Skier program 游戏时间到了 哈哈哈哈

import pygame,sys,random

skier_images = ["skier_down.png","skier_right1.png",
                "skier_right2.png","skier_left2.png",
                "skier_left1.png"]
#创建滑雪者
class SkierClass (pygame.sprite.Sprite):
    def __init__(self): #注意，一定注意两边是两个_ 成为__（更长点）
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320,100]#注意是中括号，不是小括号
        self.angle = 0
#滑雪者转向
    def turn(self,direction):
        self.angle = self.angle + direction
        if self.angle < -2: self.angle = -2
        if self.angle >  2: self.angle =  2
        center = self.rect.center
        self.image = pygame.image.load (skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle)*2]
        return speed
        
       
#滑雪者左右移动
    def move(self,speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20: self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620
#创建树和小旗
class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self,image_file,location,type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False
#让场景上滚
    def update(self):
        global speed
        self.rect.centery -= speed[1]
    #删除屏幕上方滚下的障碍物
        if self.rect.centery < -32:
            self.kill()
#创建一个窗口，包含随随机的数和小旗
            
def create_map():
    global obstacles
    locations = []
    for i in range(10):
        row = random.randint(0,9)
        col = random.randint(0,9)
        location = [col * 64 +32, row * 64 + 32 +640]#书中代码是 +20 ,而下载的代码是+32
        if not (location in locations):
            locations.append(location)
            type = random.choice(["tree","flag"])
            if type == "tree": img = "skier_tree.png"
            elif type == "flag": img = "skier_flag.png"#注意:
            obstacle = ObstacleClass(img,location,type)
            obstacles.add(obstacle)
#重新绘制屏幕
def animate():
    screen.fill([255,255,255])
    obstacles.draw(screen)
    screen.blit(skier.image,skier.rect)
    screen.blit(score_text,[10,10])
    pygame.display.flip()
#做好准备
pygame.init()
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
speed = [0,6]
obstacles = pygame.sprite.Group()
skier = SkierClass()
map_position = 0
points = 0
create_map()
font = pygame.font.Font(None,50)

#开始循环
running = True
#检查按钮或者窗口是否关闭
while running:
    clock.tick(30) #每秒更新30次图形
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)
    skier.move(speed) #移动滑雪者
    
    map_position += speed[1] #滚动场景
    
#创建一个新窗口，包含场景
    if map_position >=640:
        create_map()
        map_position = 0
        
    hit = pygame.sprite.spritecollide(skier,obstacles,False)
    if hit:
        #检查是否碰到数或者得到旗
        if hit[0].type == "tree" and not hit[0].passed:
            points = points - 100
            skier.imagge = pygame.image.load("skier_crash.png")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("skier_down.png")
            skier.angle = 0
            speed = [0,6]
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:
            points += 10
            hit[0].kill()
            
    obstacles.update()
    score_text = font.render("Score:" +str(points),1,(0,0,0)) #显示得分
    animate()
    
pygame.quit()
    