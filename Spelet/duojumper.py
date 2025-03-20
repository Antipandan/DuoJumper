from class_level import Level
from constants import *

RUNNING = True
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("DuoJumper")


def render_text(text: str, size=36, color="white"):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    return text_surface


def menu(top_text: str, middle_text="Play again", bottom="Quit"):
    button_centered(top_text, screen_width / 2, 10, 60)
    button_1 = button_centered(middle_text, screen_width / 2, 200)
    button_2 = button_centered(bottom, screen_width / 2, 350)
    return [button_1, button_2]

def reset_pos(player_group: pygame.sprite.Group):
    for player in player_group.sprites():
        player.x_pos, player.y_pos = start_pos[0], start_pos[1]
        player.x_speed, player.y_speed = 0, 0
        level.player_1.x_speed, level.player_1.y_speed = 0, 0


def button_centered(text: str, pos_x: int, pos_y: int, size=36, color="white"):
    title = render_text(text, size, color)
    title_rect = title.get_rect()
    title_rect.update(pos_x - title_rect.width / 2, pos_y, title_rect.width, title_rect.height)
    screen.blit(title, (title_rect.x, title_rect.y))
    return title_rect


def back_to_main_menu(pos_x, pos_y, size=36):
    main = render_text("<-- Main Menu", size)
    main_menu_rect = main.get_rect()
    screen.blit(main, (pos_x, pos_y))
    return main_menu_rect


def mouse_click_button(button_rect: pygame.Rect, mouse_position: list, mouse):
    if button_rect.collidepoint(mouse_position[0], mouse_position[1]) and mouse[0]:
        return True


class RenderLevelIcon:
    def __init__(self, offset_x: int, offset_y: int, image_path: str, map_name: str = "Placeholder", map_location=""):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.image_path = image_path
        self.map_name = map_name
        self.map_location = map_location

    def render_level_icon(self):
        level_1_image = pygame.image.load(self.image_path)
        level_1_image_rect = level_1_image.get_rect()
        level_1_image_rect.update(self.offset_x, self.offset_y, level_1_image.width, level_1_image.height)

        screen.blit(level_1_image, (level_1_image_rect.x, level_1_image_rect.y))
        pygame.draw.rect(screen, "white", level_1_image_rect, 1)

        level_text = render_text(self.map_name, 20)
        level_text_rect = level_text.get_rect()
        level_text_rect.top = level_1_image_rect.bottom
        level_text_rect.midtop = level_1_image_rect.midtop
        screen.blit(level_text, (level_text_rect.x, level_1_image_rect.y))

        return level_1_image_rect


in_game = False
in_main = True
level_select = False
paused = False
all_alive = True
while RUNNING:
    pygame.display.init()
    player_input = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
    if player_input[pygame.K_ESCAPE]:
        paused = True
        in_game = False
    # lägg all körbar kod här så att menyn kan se lite bättre ut
    mouse_pos = pygame.mouse.get_pos()
    mouse_input = pygame.mouse.get_pressed(3)
    if in_main:
        # fråga mig inte varför jag renderar nivån och inte bara använder mig av en bild
        # libpng warning: iCCP: known incorrect sRGB profile
        render_level_only(screen, bg_path)
        title_rect = button_centered("DuoJumper", screen_width / 2, 10, 60)
        play_rect = button_centered("Play", screen_width / 2, 250, 45)
        quit_rect = button_centered("QUIT", screen_width / 2, 500, 45)
        if mouse_click_button(play_rect, mouse_pos, mouse_input):
            in_main = False
            level_select = True
            paused = False
            in_game = False
        elif mouse_click_button(quit_rect, mouse_pos, mouse_input):
            quit()
            pygame.display.quit()
        pygame.display.update()

    else:
        if level_select:
            screen.fill("black")
            render_level_only(screen, asset_path + "showcase_levels/" + chosen_map_path)
            map_select = button_centered("Select a map", screen_width / 2, 10, 60)
            image_level_1 = RenderLevelIcon(58, 90, images_path + "map_img_2.jpg", "Wanderers Rest", level_path + "Level_1.tmx")
            # 210 eftersom bilderna är 210 pixlar bredda kanske måste fixas men funkar nu
            image_level_2 = RenderLevelIcon(148 + 210, 90, images_path + "map_img_4.jpg", "Floating point",
                                            level_path + "Level_2.tmx")
            # Började att använda mig av JPG så att jag inte skulle få röda varningar?? De orsakade inga problem men
            # de var inte trevliga att ha. Dessutom blir det lite lättare att läsa text nu
            image_level_3 = RenderLevelIcon(148 + (90 * 3) + 210, 90, images_path + "map_img_5.jpg", "Hip Hop Hill",
                                            level_path + "Level_3.tmx")
            maps = [image_level_1, image_level_2, image_level_3]
            main_rect = back_to_main_menu(0, 0, 45)
            for iter_map in maps:
                if iter_map.render_level_icon().collidepoint(mouse_pos) and mouse_input[0] and iter_map.map_location != "":
                    level_select = False
                    in_game = True
                    in_main = False
                    paused = False
                    level = Level(screen, iter_map.map_location)
            pygame.display.update()
            if main_rect.collidepoint(mouse_pos) and mouse_input[0]:
                in_main = True
                level_select = False
                in_game = False
                paused = False
                screen.fill("black")
                pygame.display.update()
        else:
            if in_game:
                level.run()
                # Försökte att loopa igenom alla spelar instanser för att kolla om alla var vid liv. Det fungerade inte
                # Värdet baserades då på en instans. Använd denna funktion för att kolla om alla är vid liv
                all_alive = check_all_are_alive(level.player_group)
                pygame.display.update()
                delta_time = clock.tick(60)

            if not all_alive:
                in_game = False
                mouse_pos = pygame.mouse.get_pos()
                button = menu("You died", "Try again", "Back to main menu")
                pygame.display.update()
                # Mouse input är dict. Index anger vilken knapp true har tryckt false ej
                if button[0].collidepoint(mouse_pos) and mouse_input[0]:
                    reset_pos(level.player_group)
                    in_game = True
                elif button[1].collidepoint(mouse_pos) and mouse_input[0]:
                    screen.fill("black")
                    in_game = True
                    in_main = True
                    reset_pos(level.player_group)
            elif paused:
                in_game = False
                pause_input = pygame.key.get_pressed()
                main_rect_2 = back_to_main_menu(0, 0, 45)
                button_pause = menu("Paused", "Resume", "Select New Map")
                pygame.display.update()
                if pause_input[pygame.K_ESCAPE]:
                    in_game = True
                    paused = False
                if button_pause[0].collidepoint(mouse_pos) and mouse_input[0]:
                    in_game = True
                    paused = False
                elif main_rect_2.collidepoint(mouse_pos) and mouse_input[0]:
                    in_game = False
                    level_select = False
                    in_main = True
                    screen.fill("black")
                    reset_pos(level.player_group)
                    pygame.display.update()
                elif button_pause[1].collidepoint(mouse_pos) and mouse_input[0]:
                    in_game = False
                    level_select = True
                    screen.fill("black")
                    reset_pos(level.player_group)
                    pygame.display.update()
