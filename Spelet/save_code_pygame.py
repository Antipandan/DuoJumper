import pygame

# spel variabler

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
delta_time = 0
gravity = 11
amount = 30
acceleration = amount
RUNNING = True
player_pos = pygame.Vector2(1080 / 2, 2 / 2)
falling = True
bool_y_pos_s = True
bool_y_pos_w = True
bool_x_pos_a = True
bool_x_pos_d = True


# funktioner

class Platforms:
    def __init__(self, color, width, corners):
        self.color = color
        self.width = width
        self.corners = corners

    def __str__(self):
        return "koordinat || {}, {}, {}, {}".format(self.corners[0], self.corners[1], self.corners[2], self.corners[3])

    def draw_platform(self):
        # TODO rita insidan
        # ritar övre linje
        top = pygame.draw.line(screen, self.color, self.corners[0], self.corners[1], self.width)
        # ritar nedre linje
        bottom = pygame.draw.line(screen, self.color, self.corners[2], self.corners[3], self.width)
        # ritar den vänstra linjen
        left = pygame.draw.line(screen, self.color, self.corners[0], self.corners[2], self.width)
        # ritar den högra linjen
        right = pygame.draw.line(screen, self.color, self.corners[1], self.corners[3], self.width)
        return {1: top, 2: bottom, 3: left, 4: right}


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, y_speed, x_speed, ID, max_speed):
        # ladda in variabler
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.max_speed = max_speed
        self.ID = ID
        self.falling = True

    def __str__(self):
        return "{} y.pos || {} x.pos".format(self.y_pos, self.x_pos)

    def draw(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
        return self.ball

    def gravity(self):
        self.y_speed += gravity
        self.y_pos += self.y_speed * delta_time
        if self.y_speed > self.max_speed * 2:
            self.y_speed = self.max_speed * 2

    def movement(self, keys_pressed):
        if bool_y_pos_s:
            if keys_pressed[pygame.K_s]:
                self.y_speed += acceleration
        if bool_x_pos_a:
            if keys_pressed[pygame.K_a]:
                self.x_speed -= acceleration
        if bool_x_pos_d:
            if keys_pressed[pygame.K_d]:
                self.x_speed += acceleration
        self.y_pos += self.y_speed * delta_time
        self.x_pos += self.x_speed * delta_time

    def check_collision_walls(self):
        if bool_y_pos_s:
            if self.y_pos <= 0:
                self.y_pos = 1
                self.y_speed = 0
            if self.x_pos >= screen_width:
                self.x_pos = screen_width - 1
                self.x_speed = 0
            if self.x_pos <= 0:
                self.x_speed = 0
                self.x_pos = 1


# deklarera bollar

ball_1 = Ball(player_pos[0], player_pos[1], 20, [255, 0, 0], 0, 0, 0, 300)
# ball_2 = Ball(player_pos[0] + 50, player_pos[1] + 50, 30, "blue", 100, 0.9, 0, 0, 1)

# def __init__(self, color, width, corners):
platform_1 = Platforms("#E8181C", 5, [[300, 500], [700, 500], [300, 700], [700, 700]])
while True:
    pygame.display.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
    screen.fill("black")
    player_input = pygame.key.get_pressed()
    if player_input[pygame.K_ESCAPE]:
        pygame.display.quit()
        quit()
    if RUNNING:
        platform_var_1 = platform_1.draw_platform()
        player = ball_1.draw()
        if bool_y_pos_s:
            ball_1.gravity()
        ball_1.movement(player_input)
        ball_1.check_collision_walls()
        # TODO lägg till kollision för alla andra platformar
        for i in platform_var_1:
            if i == 1 and platform_var_1[1].colliderect(player):
                bool_y_pos_s = False
                ball_1.y_speed = 0
                ball_1.y_pos = platform_var_1[i][1] - ball_1.radius + 1
                ball_1.x_speed *= 0.93
                if abs(ball_1.x_speed) <= 20:
                    ball_1.x_speed = 0
            if platform_var_1[1].colliderect(player) and (player_input[pygame.K_SPACE] or player_input[pygame.K_w]):
                ball_1.y_speed -= 75
                ball_1.y_pos += ball_1.y_speed * delta_time
                bool_y_pos_s = True

        if ball_1.y_pos >= screen_height:
            RUNNING = False
    else:
        #screen.fill("red")
        if player_input[pygame.K_SPACE]:
            ball_1.y_pos = screen_height / 2
            RUNNING = True
    print(bool_y_pos_s)
    print(type(ball_1.ball))
    pygame.display.update()
    # TODO fixa så att fysik inte är FPS baserat
    delta_time = clock.tick(60) / 1000
