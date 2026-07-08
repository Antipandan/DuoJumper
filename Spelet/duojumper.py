from pygame.font import Font
from pygame.key import ScancodeWrapper
from pygame.time import Clock
from pygame import Rect
from pygame import Surface

from class_level import Level
from constants import *

pygame.init()
screen: Surface = pygame.display.set_mode((screen_width, screen_height))
clock: Clock = pygame.time.Clock()
pygame.display.set_caption("DuoJumper")


def render_text(text: str, size: int = 36, color: str = "white") -> Surface:
    font: Font = pygame.font.SysFont("Arial", size)
    text_surface: Surface = font.render(text, True, color)
    return text_surface


def menu(top_text: str, middle_text: str = "Play again", bottom: str = "Quit") -> list[Rect]:
    button_centered(top_text, int(screen_width / 2), 10, 60)
    button_1: Rect = button_centered(middle_text, int(screen_width / 2), 200)
    button_2: Rect = button_centered(bottom, int(screen_width / 2), 350)
    return [button_1, button_2]


def reset_pos(player_group: pygame.sprite.Group) -> None:
    for player in player_group.sprites():
        player.x_pos, player.y_pos = start_pos[0], start_pos[1]
        player.x_speed, player.y_speed = 0, 0
        level.player_1.x_speed, level.player_1.y_speed = 0, 0


def button_centered(text: str, pos_x: int, pos_y: int, size=36, color="white") -> Rect:
    title: Surface = render_text(text, size, color)
    title_rect_local: Rect = title.get_rect()
    title_rect_local.update(pos_x - title_rect_local.width / 2, pos_y, title_rect_local.width, title_rect_local.height)
    screen.blit(title, (title_rect_local.x, title_rect_local.y))
    return title_rect_local


def back_to_main_menu(pos_x: int, pos_y: int, size: int = 36) -> Rect:
    main: Surface = render_text("<-- Main Menu", size)
    main_menu_rect: Rect = main.get_rect()
    screen.blit(main, (pos_x, pos_y))
    return main_menu_rect


def mouse_click_button(button_rect: pygame.Rect, mouse_position: tuple[int, int], mouse: tuple[int, int]) -> bool | int:
    return button_rect.collidepoint(mouse_position[0], mouse_position[1]) and mouse[0]


class RenderLevelIcon:
    def __init__(self, offset_x: int, offset_y: int, image_path: str, map_name: str = "Placeholder",
                 map_location="") -> None:
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y
        self.image_path: str = image_path
        self.map_name: str = map_name
        self.map_location: str = map_location

    def render_level_icon(self) -> Rect:
        level_1_image: Surface = pygame.image.load(self.image_path)
        level_1_image_rect: Rect = level_1_image.get_rect()
        level_1_image_rect.update(self.offset_x, self.offset_y, level_1_image.get_width(), level_1_image.get_height())

        screen.blit(level_1_image, (level_1_image_rect.x, level_1_image_rect.y))
        pygame.draw.rect(screen, "white", level_1_image_rect, 1)

        level_text: Surface = render_text(self.map_name, 20)
        level_text_rect: Rect = level_text.get_rect()
        level_text_rect.top = level_1_image_rect.bottom
        level_text_rect.midtop = level_1_image_rect.midtop
        screen.blit(level_text, (level_text_rect.x, level_1_image_rect.y))
        return level_1_image_rect


in_game: bool = False
in_main: bool = True
level_select: bool = False
paused: bool = False
all_alive: bool = True
while RUNNING:
    pygame.display.init()
    player_input: ScancodeWrapper = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()

    if player_input[pygame.K_ESCAPE]:
        paused = True
        in_game = False

    # lägg all körbar kod här så att menyn kan se lite bättre ut
    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
    mouse_input: tuple[bool, bool, bool] = pygame.mouse.get_pressed(3)

    if in_main:
        # fråga mig inte varför jag renderar nivån och inte bara använder mig av en bild
        # libpng warning: iCCP: known incorrect sRGB profile
        render_level_only(screen, bg_path)
        title_rect: Rect = button_centered("DuoJumper", int(screen_width / 2), 10, 60)
        play_rect: Rect = button_centered("Play", int(screen_width / 2), 250, 45)
        quit_rect: Rect = button_centered("QUIT", int(screen_width / 2), 500, 45)

        if mouse_click_button(play_rect, mouse_pos, mouse_input):
            in_main = False
            level_select = True
            paused = False
            in_game = False
        elif mouse_click_button(quit_rect, mouse_pos, mouse_input):
            pygame.display.quit()
            quit()

        pygame.display.update()

    else:

        if level_select:
            screen.fill("black")
            render_level_only(screen, asset_path + "showcase_levels/" + chosen_map_path)
            map_select: Rect = button_centered("Select a map", int(screen_width / 2), 10, 60)

            # nivå 1
            image_level_1: RenderLevelIcon = RenderLevelIcon(
                standard_offset_x, standard_offset_y, images_path + "map_img_2.jpg",
                "Wanderers Rest", level_path + "level_1.tmx")

            # nivå 2
            image_level_2: RenderLevelIcon = RenderLevelIcon(
                standard_offset_x + space_in_between + standard_image_width, 90,
                images_path + "map_img_4.jpg", "Floating point", level_path + "level_2.tmx")

            # Började att använda mig av JPG så att jag inte skulle få röda varningar?? De orsakade inga problem men
            # de var inte trevliga att ha. Dessutom blir det lite lättare att läsa text nu
            # nivå 3
            image_level_3: RenderLevelIcon = RenderLevelIcon(
                standard_offset_x + space_in_between * 2 + standard_image_width * 2, standard_offset_y,
                images_path + "map_img_5.jpg", "Hip Hop Hill", level_path + "level_3.tmx")

            maps: list[RenderLevelIcon] = [image_level_1, image_level_2, image_level_3]
            main_rect: Rect = back_to_main_menu(0, 0, 45)
            level = None
            for current_map in maps:
                if current_map.render_level_icon().collidepoint(mouse_pos) and mouse_input[
                    0] and current_map.map_location != "":
                    level_select = False
                    in_game = True
                    in_main = False
                    paused = False
                    level: Level = Level(screen, current_map.map_location)
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
                all_alive: bool = check_all_are_alive(level.player_group)
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
