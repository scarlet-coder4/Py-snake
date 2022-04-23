import pygame, random

# colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
green=(175, 215, 70)
darkgreen=(0,100,0)

class Snake:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.x_change = 0
        self.y_change = 0
        self.move_right()
        self.length=1
        self.list=[]

    def move_left(self):
        self.x_change = -10
        self.y_change = 0

    def move_right(self):
        self.x_change = 10
        self.y_change = 0

    def move_up(self):
        self.y_change = -10
        self.x_change = 0

    def move_down(self):
        self.y_change = 10
        self.x_change = 0

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def boundary(self):
        if self.x<30 or self.x>740 or self.y<30 or self.y>540:
            return True
        else:
            return False

class Apple:
    def __init__(self):
        self.img = pygame.image.load("apple.png")
        self.randomize()

    def randomize(self):
        self.x = random.randint(30, 708)
        self.y = random.randint(30, 508)

class Game:
    def __init__(self):
        pygame.init()
        self.snake=Snake()
        self.apple=Apple()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(" Snake Game")
        logo = pygame.image.load("logo.png")
        pygame.display.set_icon(logo)
        self.myfont = pygame.font.SysFont('msgothic', 30)
        self.clk = pygame.time.Clock()
        self.fps = 26
        self.sensitivity=20
        self.score=0

        with open("highscore.txt","r") as f:
            self.highscore=f.read()
            self.hscore=int(self.highscore)

    def write(self,text,color,x,y):
        text = self.myfont.render(text, True, color)
        self.screen.blit(text, (x,y))

    def draw_snake(self):
        for a,b in self.snake.list:
            pygame.draw.rect(self.screen, white, (a, b, 22, 22))

    def h_score(self):
        with open("highscore.txt","w") as f:
            self.highscore=str(self.hscore)
            f.write(self.highscore)

    def collision(self):
        if abs(self.snake.x-self.apple.x)<self.sensitivity and abs(self.snake.y-self.apple.y)<self.sensitivity:
            self.snake.length +=2
            self.apple.randomize()
            self.score +=10
            if self.score>self.hscore:
                self.hscore=self.score

    def run(self):
        running=True
        while running:

            self.screen.fill(darkgreen)
            pygame.draw.rect(self.screen,green,(30,30,740,540))
            self.write(f"Score: {self.score}",black,0,0)
            self.write(f"High Score: {self.hscore}", black, 500, 0)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                    if event.key == pygame.K_UP:
                        self.snake.move_up()
                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()

            self.snake.move()

            if self.snake.boundary():
                running=False

            self.collision()

            head=[]
            head.append(self.snake.x)
            head.append(self.snake.y)
            self.snake.list.append(head)

            if len(self.snake.list)>self.snake.length:
                self.snake.list.pop(0)

            if head in self.snake.list[:-1]:
                running=False

            self.draw_snake()
            self.screen.blit(self.apple.img,(self.apple.x,self.apple.y))
            pygame.display.update()
            self.clk.tick(self.fps)

if __name__ == "__main__":
    game=Game()
    game.run()
    game.h_score()