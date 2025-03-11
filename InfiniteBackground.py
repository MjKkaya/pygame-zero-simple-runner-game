from pgzero.builtins import Actor
from pgzero.builtins import animate

class InfiniteBackground():

    def __init__(self, background_paths, speed):
        self.__background_paths = background_paths
        self.__speed = speed
        self.__background_items = []
        print("InfiniteBackground:"+str(len(background_paths)))
        self.__create_backgrounds()


    def __scroll_backgrounds(self, dt):
        bg_0 = self.__background_items[0]
        if bg_0.right <=  0:
            bg_0 = self.__background_items.pop(0)
            self.__background_items.append(bg_0)
            bg_0.left = self.__background_items[0].right

        for item in self.__background_items:
            item.x -= self.__speed * dt


    def __create_backgrounds(self):
        pos_x = 0
        for path in self.__background_paths:
            bg = Actor(path)
            bg.topleft = (pos_x, 0)
            self.__background_items.append(bg)
            pos_x += bg.width
            #print("InfiniteBackground-CreateBackgrounds:"+str(pos_x))


    def set_active_scrolling(self, is_active):
        #print("InfiniteBackground-set_active_scrolling:"+str(is_active))
        self.is_active_scrolling = is_active


    def draw(self):
        for item in self.__background_items:
            item.draw()


    def update(self, dt):
        if self.is_active_scrolling:
            self.__scroll_backgrounds(dt)
