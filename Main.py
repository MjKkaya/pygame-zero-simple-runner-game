import pgzrun


WIDTH = 900
HEIGHT = 500


# 0: Game not started,  1: Game started, 2: Game over
game_state = 0
is_sound_on = True

menu_button_size = (64, 64)



# Begin region : Home Screen

if is_sound_on:
    music.play("intro")

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
            global game_state
            game_state = 1
            if is_sound_on:
                music.play("game_music")

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


# Begin region : Game Screen

def draw_game_screen():
    print("Draw game screen!")


def check_game_screen_keyboard_inputs(key):
    if key == keys.RETURN:
        global game_state
        game_state = 2
        if is_sound_on:
            music.stop()
            sounds.game_over.play()



# End region


# Begin region : Game Over Screen

home_button = Actor("ui/home")

def draw_game_over_screen():
    screen.blit("background", (0, 0))
    screen.draw.textbox("GAME OVER", (WIDTH*0.1, (HEIGHT * 0.25) ,WIDTH*0.8,65), color="white", owidth=1, ocolor="red")
    screen.draw.textbox(f"Final Score: {99}", (WIDTH*0.1, (HEIGHT * 0.25) + 100, WIDTH*0.8, 35), color="white")
    #screen.draw.textbox("Press 'Enter' to return to the menu.", (WIDTH*0.1, (HEIGHT * 0.25) +200 ,WIDTH*0.8,35), color="white")


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
            if is_sound_on:
                music.play("intro")

        if play_button.collidepoint(pos):
            game_state = 1
            if is_sound_on:
                music.play("game_music")

"""
def check_game_over_screen_keyboard_inputs(key):
    if key == keys.RETURN:
        global game_state
        game_state = 0
"""
# End region


def draw():
    screen.clear() # we must call the method because all old and draing items will be overlap!
    if game_state == 0:
        draw_home_screen()
    elif game_state == 1:
        draw_game_screen()
    else:
        draw_game_over_screen()


#def update(): #dt : delta-time


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
