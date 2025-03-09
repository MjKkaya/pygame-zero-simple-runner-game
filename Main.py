import pgzrun
import random
from Characters import *
from InfiniteBackground import InfiniteBackground

WIDTH = 900
HEIGHT = 500

game_state = 0              # 0: Game not started,  1: Game started, 2: Game over
is_sound_on = True
menu_button_size = (64, 64)

score = 10;
total_score = 0;


def play_music(name):
    if is_sound_on:
        music.play(name)


# Region : Home Screen

play_music("intro")
play_button = Actor("ui/play")
sound_icon_on = "ui/sound_on"
sound_icon_off = "ui/sound_off"
sound_button = Actor(sound_icon_on)
quit_button = Actor("ui/quit")


def draw_home_screen():
    screen.blit("background", (0, 0))
    screen.draw.textbox("Simple Runner", (WIDTH*0.1, (HEIGHT * 0.25) ,WIDTH*0.8,65), color="white", shadow=(1.0,1.0), scolor="blue")

    button_count = 3
    button_gap_horizontal = menu_button_size[0]

    button_start_pos_x = (WIDTH -((menu_button_size[0] * button_count) + (button_gap_horizontal * (button_count - 1)))) * 0.5
    button_start_pos_y = HEIGHT * 0.75

    play_button.midleft = (button_start_pos_x, button_start_pos_y)
    play_button.draw()

    sound_button.midleft = (play_button.midleft[0] + menu_button_size[0] + button_gap_horizontal, button_start_pos_y)
    sound_button.draw()

    quit_button.midleft = (sound_button.midleft[0] + menu_button_size[0] + button_gap_horizontal, button_start_pos_y)
    quit_button.draw()


def check_home_screen_mouse_inputs(button, pos):
    if button == mouse.LEFT:
        global is_sound_on
        if play_button.collidepoint(pos):
            initialize_game_screen()

        elif sound_button.collidepoint(pos):
            is_sound_on = not is_sound_on
            if is_sound_on:
                music.play("intro")
            else:
                music.stop()
            sound_button.image = sound_icon_on if is_sound_on else sound_icon_off

        elif quit_button.collidepoint(pos):
            quit()

# End region


# Region : Game Screen

infinite_background = InfiniteBackground(["game_background", "game_background"])
carrot = Actor("carrot")

player_run_path = "characters/player/run/"
player_jump_path = "characters/player/jump/"
player_animations = {
    "run": [player_run_path+"run_0", player_run_path+"run_1", player_run_path+"run_2", player_run_path+"run_3", player_run_path+"run_4", player_run_path+"run_5", player_run_path+"run_6", player_run_path+"run_7"],
    "jump": [player_jump_path+"jump_0", player_jump_path+"jump_1", player_jump_path+"jump_2", player_jump_path+"jump_3", player_jump_path+"jump_4", player_jump_path+"jump_5", player_jump_path+"jump_6", player_jump_path+"jump_7"],
}
player = Player((200,370), "run", player_animations)


enemy_list = []
active_enemy_list = []
max_enemy_count = 10

fly_enemy_path = "characters/enemies/fly/"
fly_enemy_animations = { "fly": [fly_enemy_path+"fly_00", fly_enemy_path+"fly_01", fly_enemy_path+"fly_02", fly_enemy_path+"fly_03", fly_enemy_path+"fly_04", fly_enemy_path+"fly_05", fly_enemy_path+"fly_06", fly_enemy_path+"fly_07", fly_enemy_path+"fly_08", fly_enemy_path+"fly_09", fly_enemy_path+"fly_10"] }
fly_enemy = Enemy((800,370), "fly", fly_enemy_animations)

walk_enemy_path = "characters/enemies/walk/"
walk_enemy_animations = { "walk": [walk_enemy_path+"walk_0", walk_enemy_path+"walk_1", walk_enemy_path+"walk_2", walk_enemy_path+"walk_3", walk_enemy_path+"walk_4", walk_enemy_path+"walk_5", walk_enemy_path+"walk_6", walk_enemy_path+"walk_7"] }
walk_enemy = Enemy((400,370), "walk", walk_enemy_animations, 8)
walk_enemy.bottom = player.bottom

stand_enemy_path = "characters/enemies/stand/"
stand_enemy_animations = { "stand": [stand_enemy_path+"stand_0", stand_enemy_path+"stand_1", stand_enemy_path+"stand_2", stand_enemy_path+"stand_3", stand_enemy_path+"stand_4", stand_enemy_path+"stand_5", stand_enemy_path+"stand_6", stand_enemy_path+"stand_7"] }
stand_enemy = Enemy((600,370), "stand", stand_enemy_animations, 8)
stand_enemy.bottom = player.bottom


def set_carrot():
    carrot.x = random.randrange(WIDTH + 100 , WIDTH + 500)
    carrot.y = random.randrange(150, 400)
    carrot.angle = random.randrange(360)


def initialize_game_screen():
    global game_state
    game_state = 1
    play_music("game_music")
    infinite_background.set_active_scrolling(True)
    global total_score
    total_score = 0
    set_carrot()


def check_player_collider():
    if player.colliderect(carrot):
        set_carrot()
        sounds.pickup.play()
        global total_score
        total_score += score


def draw_game_background():
    screen.fill((46,46,255))
    infinite_background.draw()

def draw_game_screen():
    draw_game_background()
    player.draw()
    fly_enemy.draw()
    walk_enemy.draw()
    stand_enemy.draw()
    screen.draw.textbox(f"Score: {total_score}", (0, 10, 100, 20), color="white", owidth=1, ocolor="black")
    carrot.draw()

def update_game_screen(dt):
    player.update(dt)
    fly_enemy.update(dt)
    walk_enemy.update(dt)
    stand_enemy.update(dt)
    check_player_collider()
    carrot.x -= 300 * dt
    if carrot.right < 0:
        set_carrot()


def check_game_screen_keyboard_inputs(key):
    if key == keys.RETURN:
        global game_state
        game_state = 2
        infinite_background.set_active_scrolling(False)
        if is_sound_on:
            music.stop()
            sounds.game_over.play()

    if key == keys.SPACE:
        player.jump()
        sounds.jump.play()


# End region


# Region : Game Over Screen

home_button = Actor("ui/home")

def draw_game_over_screen():
    screen.blit("background", (0, 0))
    screen.draw.textbox("GAME OVER", (WIDTH*0.1, (HEIGHT * 0.25) ,WIDTH*0.8,65), color="white", owidth=1, ocolor="red")
    screen.draw.textbox(f"Total Score: {total_score}", (WIDTH*0.1, (HEIGHT * 0.25) + 100, WIDTH*0.8, 35), color="white")

    button_pos_y = HEIGHT * 0.75
    play_button.midleft = ((WIDTH * 0.5) - (menu_button_size[0] * 2), button_pos_y)
    play_button.draw()

    home_button.midright = ((WIDTH * 0.5) + (menu_button_size[0] * 2), button_pos_y)
    home_button.draw()


def check_game_over_screen_mouse_inputs(button, pos):
    if button == mouse.LEFT:
        global game_state

        if home_button.collidepoint(pos):
            game_state = 0
            play_music("intro")

        if play_button.collidepoint(pos):
            initialize_game_screen()

# End region


def draw():
    screen.clear() # we must call the method because all old and draing items will be overlap!
    if game_state == 0:
        draw_home_screen()
    elif game_state == 1:
        draw_game_screen()
    else:
        draw_game_over_screen()


def update(dt):
    if game_state == 1:
        update_game_screen(dt)


def on_mouse_down(button, pos):
    if game_state == 0:
        check_home_screen_mouse_inputs(button, pos)
    elif game_state == 2:
        check_game_over_screen_mouse_inputs(button, pos)

def on_key_down(key):
    if game_state == 1:
        check_game_screen_keyboard_inputs(key)
    #elif game_state == 2:
    #    check_game_over_screen_keyboard_inputs(key)

pgzrun.go()
