from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos: float, y_pos: float, movement_keys: list, class_id: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_character)
        # TODO lägg till system för att hantera olika input ex WASD, pil
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.movement_keys = movement_keys
        # orkar inte att lägga den variabel i constants
        self.max_speed_grounded = 1200
        self.player_pos = [self.x_pos, self.y_pos]
        self.rect = self.image.get_rect()
        self.length_x = self.rect.width
        self.length_y = self.rect.height
        self.falling = True
        self.delta_speed_x = self.x_speed * delta_time
        self.collision_rect_x = pygame.rect.Rect(self.x_pos - self.length_x / 2 + self.delta_speed_x,
                                                 self.y_pos - self.length_y / 2,
                                                 self.length_x + 1,
                                                 self.length_y)
        self.delta_speed_y = self.y_speed * delta_time
        self.collision_rect_y = pygame.rect.Rect(self.x_pos - self.length_x / 2,
                                                 self.y_pos - self.length_y / 2 + self.delta_speed_y,
                                                 self.length_x,
                                                 self.length_y + 1)
        self.alive = True
        self.class_id = class_id
        #self.__owned_tiles = []

    def gravity(self):
        if self.falling:
            if self.y_speed <= self.max_speed_grounded:
                self.y_speed += gravity
            else:
                self.y_speed = self.max_speed_grounded

    def friction(self):
        if abs(self.x_speed) > 25:
            self.x_speed *= friction
        else:
            self.x_speed = 0

    def collision_with_platforms(self, tiles):
        # har ej hittat ett smidigt sätt för att sätta falling = True än Jag vill implementera ett sätt för att kolla
        # bara de tiles som spelaren faktiskt kolliderar med och inte kolla alla! Det är dåligt men det fungerar nu
        self.falling = True
        # Det här är ineffektivt men det får vara så här.
        for tile in tiles:
            if tile.owner == "Player_{}".format(self.class_id) or tile.owner == None:
                if tile.rect.colliderect(self.collision_rect_y):
                    if self.y_speed < 0:
                        self.y_pos = tile.pos[1] + tile_size_y + self.length_y / 2 + 1
                        self.y_speed = -1
                    elif self.y_speed >= 0:
                        self.friction()
                        self.y_speed = 0
                        self.y_pos = tile.pos[1] - self.length_y / 2
                        self.falling = False
                        tile.change_owner("Player_{}".format(self.class_id))
                if tile.rect.colliderect(self.collision_rect_x):
                    if self.x_speed < 0:
                        self.x_speed = 0
                        # Jag vet inte varför + 33 pixlar fungerar men den gör det så...
                        self.x_pos = tile.pos[0] + self.length_x / 2 + tile_size_x + 1
                    elif self.x_speed > 0:
                        self.x_pos = tile.pos[0] - self.length_x / 2
                        self.x_speed = 0

    def collision_with_viewport(self):
        if self.x_pos <= 0 - self.length_x / 2 or self.x_pos >= screen_width + self.length_x / 2:
            self.x_pos = screen_width / 2
            self.x_speed *= 0.8
        if self.y_pos <= 0 - self.length_y / 2:
            self.y_pos = 0
        if self.y_pos >= screen_height + self.length_y / 2:
            self.y_pos = 0
            self.alive = False
        else:
            self.alive = True

    def movement(self):
        pressed_keys = pygame.key.get_pressed()
        if self.falling:
            # movement keys finns här eftersom det är en index tagen från en ett indexerat värde
            # eg self.movent_keys[2] istället för pygame.K_s i detta fall
            if pressed_keys[self.movement_keys[2]]:
                self.y_speed += acceleration
            if pressed_keys[self.movement_keys[1]]:
                self.x_speed -= acceleration * resistance_in_air
            if pressed_keys[self.movement_keys[3]]:
                self.x_speed += acceleration * resistance_in_air
            if self.x_speed >= max_speed_air:
                self.x_speed = max_speed_air
            if self.x_speed <= -1 * max_speed_air:
                self.x_speed = -1 * max_speed_air
        elif not self.falling:
            if pressed_keys[self.movement_keys[0]]:
                # hoppa
                self.y_speed = -jump_strength
            if pressed_keys[self.movement_keys[1]]:
                self.x_speed -= acceleration
            if pressed_keys[self.movement_keys[3]]:
                self.x_speed += acceleration
            if self.x_speed >= self.max_speed_grounded:
                self.x_speed = self.max_speed_grounded

        self.x_pos += self.x_speed * delta_time
        self.y_pos += self.y_speed * delta_time
        # Uppdatera collisions rects här med center
        self.collision_rect_y.center = (self.x_pos, self.y_pos + self.y_speed * delta_time)
        self.collision_rect_x.center = (self.x_pos + self.x_speed * delta_time, self.y_pos)
        self.rect.center = (self.x_pos, self.y_pos)

    def update(self, tiles):
        self.movement()
        self.gravity()
        self.collision_with_platforms(tiles)
        self.collision_with_viewport()

    def __str__(self):
        return "xpos: {}, y_pos: {}\n\nx_speed: {}, y_speed: {}".format(self.x_pos, self.y_pos,
                                                                        self.x_speed, self.x_speed)
