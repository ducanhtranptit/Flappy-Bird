import pygame
import sys
import random

#hàm tạo back
def create_background():
        background = pygame.image.load(r'assets\background-night.png').convert()#chọn ảnh làm nền 
        background = pygame.transform.scale2x(background)#chọn kích thước cho ảnh để vừa với màn hình
        return background

#hàm tạo sàn 
def draw_floor(screen, floor, floor_x_pos):
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos + 432,600))
 
# hàm thêm sàn
def create_floor():
    floor = pygame.image.load(r'assets\floor.png')
    floor = pygame.transform.scale2x(floor)
    floor_x_pos = 0
    return floor, floor_x_pos

#hàm tạo ống
def create_new_pipe():
    pipe_surface = pygame.image.load(r'assets\pipe-green.png').convert() 
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []
    pipe_height = [270,300,400,500] #các chiều cao của cột có thể xuất hiện
    spawnpipe = pygame.USEREVENT
    pygame.time.set_timer(spawnpipe , 1200) #sau 1,2 giây thì tạo ra một ống mới   
    return pipe_surface, pipe_list, pipe_height, spawnpipe 
    
#hàm random chiều cao ống
def random_height_pipe(pipe_surface, pipe_height):
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos - 680))
    return bottom_pipe, top_pipe

#hàm di chuyển ống
def move_pipe(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 2
    return pipe_list

#hàm thêm ống 
def draw_pipe(pipe_list, screen, pipe_surface):
    for pipe in pipe_list:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface,pipe)
            
        #xoay ngược ống với những ống ở trên
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

#hàm tạo chim
def create_bird():
    bird = pygame.image.load(r'assets\yellowbird-midflap.png').convert_alpha()
    bird = pygame.transform.scale2x(bird)
    bird_rect = bird.get_rect(center = (100,200))
    return bird, bird_rect

#xoay chim
def rotate_bird(bird,bird_movement):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3,1)
    return new_bird

#hàm tạo màn hình kết thúc
def game_over_screen():
    game_over_surface =  pygame.image.load(r'assets\message.png').convert_alpha()
    game_over_rect =  game_over_surface.get_rect(center = (216,384))
    return game_over_surface, game_over_rect

#hàm xử lý va chạm
def check_collision(pipe_list, bird_rect, high_score):
    for pipe in pipe_list:
        
        #nếu như ô vuông chứa con chim chạm vào ống thì trả về false
        if bird_rect.colliderect(pipe):
            return False
        
    #nếu như chim lên trên cao quá khung hình 75 đơn vị hoặc xuống chạm với sàn thì trả về false
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    
    #nếu không thuộc 2 trường hợp trên thì trả về True
    return True

#hàm tính điểm
def score_display(game_font,screen,score, game_stay, high_score):
    if game_stay == 'main game':
        
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (432/2,100))
        screen.blit(score_surface,score_rect)
    
    if game_stay == 'game over':
        
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (432/2,100))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (432/2,550))
        screen.blit(high_score_surface,high_score_rect)

#hàm tính điểm cao nhất
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#hàm set các hằng số
def const():
    gravity = 0.18 
    bird_movement = 0
    game_active = True
    score = 0
    high_score = 0
    screen = pygame.display.set_mode((432,768))#đặt một popup có kích thước 432x768
    clock = pygame.time.Clock()#set biến để đặt fps
    game_font = pygame.font.Font('04B_19.TTF',40)
    return gravity, bird_movement, game_active, score, high_score, screen, clock, game_font 

if __name__ == "__main__":
    #thiết lập chung
    pygame.init()
    gravity, bird_movement, game_active, score, high_score, screen, clock, game_font = const()
    background = create_background()
    floor, floor_x_pos = create_floor()
    bird, bird_rect = create_bird()
    pipe_surface, pipe_list, pipe_height, spawnpipe = create_new_pipe()
    game_over_surface, game_over_rect = game_over_screen()
    
    print("\n#START GAME !!!")


    #vòng while để cho chương trình hiện lên liên tục
    while True:

        #set update màn hình theo 120fps    
        clock.tick(120)
        pygame.display.update()
          
        #thêm back
        screen.blit(background,(0,0))
        
        #nếu như game_active còn đúng thì kích hoạt tính năng của ống và chim
        if game_active:
            #thêm ống
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list, screen, pipe_surface)
            
            #thêm chim
            rotated_bird = rotate_bird(bird,bird_movement)
            screen.blit(rotated_bird,bird_rect)
            game_active = check_collision(pipe_list,bird_rect, high_score)
            
            #tính điểm
            score += 0.005 #sau một khoảng thời gian nhất định thì điểm sẽ được cộng
            high_score = update_high_score(score, high_score)
            score_display(game_font,screen,score, 'main game', high_score) #hiển thị điểm của màn chơi
       
        else:
            
            screen.blit(game_over_surface, game_over_rect) #hiển thị màn hình kết thúc
            score_display(game_font,screen,score, 'game over', high_score) #hiển thị điểm cao nhất
            
       
        #thêm sàn
        floor_x_pos -= 1
        screen.blit(floor,(floor_x_pos,600))
        draw_floor(screen, floor, floor_x_pos)
        if floor_x_pos <= -432:
            print("new ground")
            floor_x_pos = 0
        
        #set trọng lực cho chim
        bird_movement += gravity 
        bird_rect.centery += bird_movement

        #tạo vòng lặp cho các sự kiện có thể gặp trong game
        for event in pygame.event.get():
            
            #nếu bấm vào nút thoát ra ngoài thì thoát cửa số game
            if event.type == pygame.QUIT:
                print('# GAME EXIT !!')
                pygame.quit()
                sys.exit()
    
            #tạo sự kiện nếu như bấm nút K thì con chim sẽ nhảy lên
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print("jump!")
                    bird_movement = 0 #taị thời điểm ấn nút thì tọa độ sẽ quay về 0 tại điểm nhấn
                    bird_movement = -5 #chim sẽ nhảy lên trên với độ cao đơn vị

                #nếu va vào cột thì nhấn một lần nữa để tiếp tục ván mới
                if event.key == pygame.K_f and game_active == False:
                    print("\nGAME OVER!!!")
                    print("SCORE: " + str(int(score)) + '\n')
                    print("*************\n")
                    print("\nNew Game!!\n")
                    game_active = True #chuyển về True để tiếp tục trò chơi
                    pipe_list.clear() #xóa danh sách ống đang có để bắt đầu ván mới
                    bird_rect = bird.get_rect(center = (100,200)) #reset lại con chim
                    bird_movement = 0
                    score = 0

            #tạo sự kiện xuất hiện ống mới
            if event.type == spawnpipe:
                print("new pipe")
                pipe_list.extend(random_height_pipe(pipe_surface, pipe_height))






# import pygame
# import sys
# import random

# class Background:
#     def __init__(self):
#         self.image = pygame.image.load(r'assets\background-night.png').convert()
#         self.image = pygame.transform.scale2x(self.image)

#     def draw(self, screen):
#         screen.blit(self.image, (0, 0))

# class Floor:
#     def __init__(self):
#         self.image = pygame.image.load(r'assets\floor.png')
#         self.image = pygame.transform.scale2x(self.image)
#         self.x_pos = 0

#     def draw(self, screen):
#         screen.blit(self.image, (self.x_pos, 600))
#         screen.blit(self.image, (self.x_pos + 432, 600))

# class Pipe:
#     def __init__(self):
#         self.image = pygame.image.load(r'assets\pipe-green.png').convert()
#         self.image = pygame.transform.scale2x(self.image)
#         self.list = []
#         self.heights = [270, 300, 400, 500]
#         self.spawn_event = pygame.USEREVENT
#         pygame.time.set_timer(self.spawn_event, 1200)

#     def create_new_pipe(self):
#         random_pipe_pos = random.choice(self.heights)
#         bottom_pipe = self.image.get_rect(midtop=(500, random_pipe_pos))
#         top_pipe = self.image.get_rect(midtop=(500, random_pipe_pos - 680))
#         return bottom_pipe, top_pipe

#     def move_pipes(self):
#         for pipe in self.list:
#             pipe.centerx -= 2

#     def draw_pipes(self, screen):
#         for pipe in self.list:
#             if pipe.bottom >= 768:
#                 screen.blit(self.image, pipe)
#             else:
#                 flip_pipe = pygame.transform.flip(self.image, False, True)
#                 screen.blit(flip_pipe, pipe)

# class Bird:
#     def __init__(self):
#         self.image = pygame.image.load(r'assets\yellowbird-midflap.png').convert_alpha()
#         self.image = pygame.transform.scale2x(self.image)
#         self.rect = self.image.get_rect(center=(100, 200))
#         self.gravity = 0.18
#         self.movement = 0

#     def rotate(self):
#         return pygame.transform.rotozoom(self.image, -self.movement * 3, 1)

#     def jump(self):
#         self.movement = 0
#         self.movement -= 5

# class GameOverScreen:
#     def __init__(self):
#         self.image = pygame.image.load(r'assets\message.png').convert_alpha()
#         self.rect = self.image.get_rect(center=(216, 384))

# class Game:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((432, 768))
#         self.clock = pygame.time.Clock()
#         self.font = pygame.font.Font('04B_19.TTF', 40)
#         self.score = 0
#         self.high_score = 0
#         self.game_active = True

#         self.background = Background()
#         self.floor = Floor()
#         self.bird = Bird()
#         self.pipe = Pipe()
#         self.game_over_screen = GameOverScreen()

#     def run(self):
#         pygame.init()

#         while True:
#             self.clock.tick(120)
#             pygame.display.update()

#             self.screen.blit(self.background.image, (0, 0))

#             if self.game_active:
#                 self.pipe.move_pipes()
#                 self.pipe.draw_pipes(self.screen)

#                 rotated_bird = self.bird.rotate()
#                 self.screen.blit(rotated_bird, self.bird.rect)

#                 self.game_active = self.check_collision()

#                 self.score += 0.005
#                 self.high_score = self.update_high_score()

#                 self.score_display('main game')

#             else:
#                 self.screen.blit(self.game_over_screen.image, self.game_over_screen.rect)
#                 self.score_display('game over')

#             self.floor.x_pos -= 1
#             self.screen.blit(self.floor.image, (self.floor.x_pos, 600))
#             self.floor.draw(self.screen)
#             if self.floor.x_pos <= -432:
#                 self.floor.x_pos = 0

#             self.bird.movement += self.bird.gravity
#             self.bird.rect.centery += self.bird.movement

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         self.bird.jump()

#                 if event.type == self.pipe.spawn_event:
#                     self.pipe.list.extend(self.pipe.create_new_pipe())

#     def check_collision(self):
#         for pipe in self.pipe.list:
#             if self.bird.rect.colliderect(pipe):
#                 return False

#         if self.bird.rect.top <= -75 or self.bird.rect.bottom >= 650:
#             return False

#         return True

#     def score_display(self, game_stay):
#         if game_stay == 'main game':
#             score_surface = self.font.render(str(int(self.score)), True, (255, 255, 255))
#             score_rect = score_surface.get_rect(center=(432 / 2, 100))
#             self.screen.blit(score_surface, score_rect)

#         if game_stay == 'game over':
#             score_surface = self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
#             score_rect = score_surface.get_rect(center=(432 / 2, 100))
#             self.screen.blit(score_surface, score_rect)

#             high_score_surface = self.font.render(f'High score: {int(self.high_score)}', True, (255, 255, 255))
#             high_score_rect = high_score_surface.get_rect(center=(432 / 2, 550))
#             self.screen.blit(high_score_surface, high_score_rect)

#     def update_high_score(self):
#         if self.score > self.high_score:
#             self.high_score = self.score
#         return self.high_score

# if __name__ == "__main__":
#     game = Game()
#     game.run()
