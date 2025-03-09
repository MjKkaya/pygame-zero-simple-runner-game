from pgzero.builtins import Actor


class Character(Actor):

    def __init__(self, position, current_state, animations, fps):
        super().__init__(animations[current_state][0], position)
        self.state = current_state              # default state
        self.animations = animations            # Store animation dictionary
        self.elapsedtime = 0
        self.imageIndexNo = 0
        self.default_pos = position
        self.animation_time = 1/fps
        #print("fps:"+str(self.animation_time))



    def sprite_animation(self, dt):
        self.elapsedtime += dt
        if self.elapsedtime > self.animation_time:
            self.elapsedtime = 0
            self.image = self.animations[self.state][self.imageIndexNo]
            self.imageIndexNo += 1
            if self.imageIndexNo == len(self.animations[self.state])-1:
                self.imageIndexNo = 0


    def update(self, dt):
        self.sprite_animation(dt)



class Player(Character):
    gravity = 1
    jump_velocity = -20


    def __init__(self, position, current_state, animations, fps = 30):
        super().__init__(position, current_state, animations, fps)
        self.is_ground = True
        self.jump_elapsed_time = 0
        self.current_jump_velocity = 0


    def update(self, dt):
        super().update(dt)
        if not self.is_ground:  # player is in the air!
            self.y += self.current_jump_velocity
            self.current_jump_velocity += self.gravity

            if self.default_pos[1] == self.y:   # player touchs the ground.
                self.current_jump_velocity = 0
                self.is_ground = True
                self.state = "run"


    def jump(self):
        if self.is_ground:
            self.current_jump_velocity = self.jump_velocity
            self.elapsedtime = 0
            self.imageIndexNo = 0
            self.jump_elapsed_time = 0
            self.state = "jump"
            self.is_ground = False



class Enemy(Character):

    def __init__(self, position, current_state, animations, fps = 30):
        super().__init__(position, current_state, animations, fps)


    def update(self, dt):
        super().update(dt)


    def move(self):
        print("move")

