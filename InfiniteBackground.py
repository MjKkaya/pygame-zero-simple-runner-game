from pgzero.builtins import Actor
from pgzero.builtins import animate

class InfiniteBackground():

    def __init__(self, background_paths):
        self.background_paths = background_paths
        self.background_items = []
        print("InfiniteBackground:"+str(len(background_paths)))
        self.CreateBackgrounds()

    def draw(self):
        for item in self.background_items:
            item.draw()
        #print("InfiniteBackground-draw:"+str(len(self.background_paths)))


    def repeat_background_ani(self):
        bg_0 = self.background_items.pop(0)
        self.background_items.append(bg_0)
        print("InfiniteBackground-repeat_background_ani"+str(self.is_active_scrolling))
        if self.is_active_scrolling:
            self.scroll_backgrounds()


    def scroll_backgrounds(self):
        bg_0 = self.background_items[0]
        bg_0.topleft = (0, 0)
        bg_1 = self.background_items[1]
        bg_1.topleft = (bg_0.width, 0)
        print("InfiniteBackground-scroll_backgrounds:"+str(bg_0.topleft)+", "+str(bg_1.topleft))

        animate(bg_0, pos=(bg_0.x-bg_0.width, bg_0.y), tween="linear", duration=15, on_finished=self.repeat_background_ani)
        animate(bg_1, pos=(bg_1.x-bg_0.width, bg_0.y), tween="linear", duration=15, on_finished=None)


    def set_active_scrolling(self, is_active):
        print("InfiniteBackground-set_active_scrolling:"+str(is_active))
        self.is_active_scrolling = is_active
        if self.is_active_scrolling:
            self.scroll_backgrounds()


    def CreateBackgrounds(self):
        #pos_x = 0
        for path in self.background_paths:
            bg = Actor(path)
            #bg.topleft = (pos_x, 0)
            self.background_items.append(bg)
            #pos_x += bg.width
            #print("InfiniteBackground-CreateBackgrounds:"+str(pos_x))
