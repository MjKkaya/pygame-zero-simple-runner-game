from pgzero.builtins import Actor


class Character(Actor):
    gravity = 1
    default_jump_velocity = -15


    def __init__(self, image, position, current_state, animations):
        super().__init__(image, position)
        self.state = current_state              # default state
        self.animations = animations            # Store animation dictionary
        self.elapsedtime = 0
        self.imageIndexNo = 0
        self.is_ground = True
        self.jump_elapsed_time = 0
        self.default_pos = position
        self.jump_velocity = 0


    def sprite_animation(self, dt):
        self.elapsedtime += dt
#        return
        if self.elapsedtime > 0.03:  # fps is 33 frame
            self.elapsedtime = 0
            #print("imageIndexNo:",self.imageIndexNo, "ss:",self.animations[self.state][self.imageIndexNo])
            self.image = self.animations[self.state][self.imageIndexNo]
            self.imageIndexNo += 1
            if self.imageIndexNo == len(self.animations[self.state])-1:
                self.imageIndexNo = 0


    def update(self, dt):
        self.sprite_animation(dt)

        if not self.is_ground:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity

            print("y:",self.y)
            if self.default_pos[1] == self.y:
                self.jump_velocity = 0
                self.is_ground = True
                self.state = "run"



    def jump(self):
        print("is_ground:",self.is_ground)
        if self.is_ground:
            self.jump_velocity = self.default_jump_velocity
            self.elapsedtime = 0
            self.imageIndexNo = 0
            self.jump_elapsed_time = 0
            self.state = "jump"
            self.is_ground = False

