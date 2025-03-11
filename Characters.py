from pgzero.builtins import Actor


class Character(Actor):

    def __init__(self, position, current_state, animations, fps):
        super().__init__(animations[current_state][0], position)
        self._state = current_state              # default state
        self.__animations = animations            # Store animation dictionary
        self.__animation_time = 1/fps
        self._elapsedtime = 0
        self._imageIndexNo = 0
        self._default_pos = position


    def sprite_animation(self, dt):
        self._elapsedtime += dt
        if self._elapsedtime > self.__animation_time:
            self._elapsedtime = 0
            self.image = self.__animations[self._state][self._imageIndexNo]
            self._imageIndexNo += 1
            if self._imageIndexNo == len(self.__animations[self._state])-1:
                self._imageIndexNo = 0


    def update(self, dt):
        self.sprite_animation(dt)


    def draw(self):
        super().draw()


    @property
    def state(self):
        return self._state



class Player(Character):
    __GRAVITY = 1
    __JUMP_VELOCITY = -20


    def __init__(self, position, current_state, animations, fps = 30):
        super().__init__(position, current_state, animations, fps)
        self.__is_ground = True
        self.__current_jump_velocity = 0


    def update(self, dt):
        super().update(dt)
        if not self.__is_ground:  # player is in the air!
            self.y += self.__current_jump_velocity
            self.__current_jump_velocity += self.__GRAVITY

            if self._default_pos[1] == self.y:   # player touchs the ground.
                self.__current_jump_velocity = 0
                self.__is_ground = True
                self._state = "run"


    def jump(self):
        if self.__is_ground:
            self.__current_jump_velocity = self.__JUMP_VELOCITY
            self._elapsedtime = 0
            self._imageIndexNo = 0
            self._state = "jump"
            self.__is_ground = False


    def reset(self):
        self.__is_ground = True
        self._state = "run"
        self._elapsedtime = 0
        self._imageIndexNo = 0
        self.__current_jump_velocity = 0
        self.pos = self._default_pos





class Enemy(Character):

    def __init__(self, position, current_state, animations, deactivated_callback, speed, fps = 30):
        super().__init__(position, current_state, animations, fps)
        self.__is_active = False
        self.__speed = speed
        self.__deactivated_callback = deactivated_callback


    def update(self, dt):
        if self.__is_active:
            super().update(dt)
            self.__move(dt)


    def draw(self):
        if self.__is_active:
            super().draw()


    def __move(self, dt):
        self.x -= (dt * self.__speed)
        if self.right < 0:
            self.__is_active = False
            self.__deactivated_callback(self)
        #print("__move", str(self.x))


    def set_active(self, is_active):
        self.__is_active = is_active
