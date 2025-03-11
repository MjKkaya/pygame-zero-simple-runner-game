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
    screen.draw.textbox("Runner Game", (WIDTH*0.1, (HEIGHT * 0.2) ,WIDTH*0.8,65), color="white", shadow=(1.0,1.0), scolor="black")

    button_count = 3
    button_gap_horizontal = menu_button_size[0]

    button_start_pos_x = (WIDTH -((menu_button_size[0] * button_count) + (button_gap_horizontal * (button_count - 1)))) * 0.5
    button_start_pos_y = HEIGHT * 0.65

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
MAX_ENEMY_COUNT = 10
BACKGROUND_SPEED = 60
elapsed_enemy_activation_time = 0
next_enemy_activation_time = 0


infinite_background = InfiniteBackground(["game_background", "game_background"], BACKGROUND_SPEED)
carrot = Actor("carrot")

player_run_path = "characters/player/run/"
player_jump_path = "characters/player/jump/"
player_animations = {
    "run": [player_run_path+"run_0", player_run_path+"run_1", player_run_path+"run_2", player_run_path+"run_3", player_run_path+"run_4", player_run_path+"run_5", player_run_path+"run_6", player_run_path+"run_7"],
    "jump": [player_jump_path+"jump_0", player_jump_path+"jump_1", player_jump_path+"jump_2", player_jump_path+"jump_3", player_jump_path+"jump_4", player_jump_path+"jump_5", player_jump_path+"jump_6", player_jump_path+"jump_7"],
}
player = Player((200,380), "run", player_animations)


active_enemy_list = []
passive_enemy_list = []


def initialize_enemies():
    active_enemy_list.clear()
    passive_enemy_list.clear()
    for index in range(MAX_ENEMY_COUNT):
        random_index = random.randrange(2)
        if random_index == 0:
            walk_enemy_path = "characters/enemies/walk/"
            walk_enemy_animations = { "walk": [walk_enemy_path+"walk_0", walk_enemy_path+"walk_1", walk_enemy_path+"walk_2", walk_enemy_path+"walk_3", walk_enemy_path+"walk_4", walk_enemy_path+"walk_5", walk_enemy_path+"walk_6", walk_enemy_path+"walk_7"] }
            enemy = Enemy((WIDTH,HEIGHT), "walk", walk_enemy_animations, enemy_deactivated, BACKGROUND_SPEED * 6, 16)
            enemy.bottom = player.bottom

        else:
            fly_enemy_path = "characters/enemies/fly/"
            fly_enemy_animations = { "fly": [fly_enemy_path+"fly_00", fly_enemy_path+"fly_01", fly_enemy_path+"fly_02", fly_enemy_path+"fly_03", fly_enemy_path+"fly_04", fly_enemy_path+"fly_05", fly_enemy_path+"fly_06", fly_enemy_path+"fly_07", fly_enemy_path+"fly_08", fly_enemy_path+"fly_09", fly_enemy_path+"fly_10"] }
            enemy = Enemy((WIDTH,HEIGHT), "fly", fly_enemy_animations, enemy_deactivated, BACKGROUND_SPEED * 7)

        passive_enemy_list.append(enemy)


def enemy_activation(dt):
    global elapsed_enemy_activation_time
    global next_enemy_activation_time
    elapsed_enemy_activation_time += dt
    if elapsed_enemy_activation_time >= next_enemy_activation_time:
        next_enemy_activation_time = random.uniform(1.5, 3.0)
        elapsed_enemy_activation_time = 0
        set_active_random_enemy()


def set_active_random_enemy():
    index_no = random.randrange(len(passive_enemy_list))
    enemy = passive_enemy_list.pop(index_no)
    active_enemy_list.append(enemy)
    enemy.x = random.randrange(WIDTH + 100 , WIDTH + 500)
    if enemy.state == "fly":
        enemy.y = random.randrange(150, 280)
        #print("set_active_random_enemy:",str(index_no), "y:",str(enemy.y))
    enemy.set_active(True)


def enemy_deactivated(enemy):
    #print("enemy_deactivated:",enemy," lists:",str(len(active_enemy_list)),"/",str(len(passive_enemy_list)))
    passive_enemy_list.append(enemy)
    active_enemy_list.remove(enemy)


def draw_enemies():
    for enemy in active_enemy_list:
        enemy.draw()


def update_enemies(dt):
    for enemy in active_enemy_list:
        enemy.update(dt)


def set_carrot():
    carrot.x = random.randrange(WIDTH + 100 , WIDTH + 300)
    carrot.y = random.randrange(150, 430)
    carrot.angle = random.randrange(360)


def initialize_game_screen():
    global game_state
    global gameplay_time
    gameplay_time = 0
    play_music("game_music")
    infinite_background.set_active_scrolling(True)
    global total_score
    total_score = 0
    player.reset()     # We have to reset because after first game, player position can changes and it affects other items/enemies position!
    set_carrot()
    initialize_enemies()
    game_state = 1


def check_player_collider():
    if player.colliderect(carrot):
        set_carrot()
        if is_sound_on:
            sounds.pickup.play()
        global total_score
        total_score += score
    check_enemy_collision()

def check_enemy_collision():
    for enemy in active_enemy_list:
        #print("check_enemy_collision:",str(len(active_enemy_list)),enemy)
        if player.colliderect(enemy):
            stop_game_screen();
            break;


def draw_game_background():
    screen.fill((46,46,255))
    infinite_background.draw()

def draw_game_screen():
    draw_game_background()
    player.draw()
    screen.draw.textbox(f"Score: {total_score}", (0, 10, 100, 20), color="white", owidth=1, ocolor="black")
    carrot.draw()
    draw_enemies()

def update_game_screen(dt):
    global gameplay_time
    gameplay_time += dt
    player.update(dt)
    update_enemies(dt)
    check_player_collider()
    carrot.x -= 300 * dt
    if carrot.right < 0:
        set_carrot()
    infinite_background.update(dt)
    enemy_activation(dt)


def check_game_screen_keyboard_inputs(key):
    if key == keys.SPACE:
        player.jump()
        if is_sound_on:
            sounds.jump.play()


def stop_game_screen():
    global game_state
    game_state = 2
    infinite_background.set_active_scrolling(False)
    if is_sound_on:
        music.stop()
        sounds.game_over.play()

# End region


# Region : Game Over Screen

home_button = Actor("ui/home")

def draw_game_over_screen():
    screen.blit("background", (0, 0))
    screen.draw.textbox("GAME OVER", (WIDTH*0.1, (HEIGHT * 0.2) ,WIDTH*0.8,65), color="white", owidth=1, ocolor="red")
    screen.draw.textbox(f"Total Score: {total_score}", (WIDTH*0.1, (HEIGHT * 0.25) + 80, WIDTH*0.8, 35), color="black")

    button_pos_y = HEIGHT * 0.65
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

pgzrun.go()
