import sys, logging, arcade, random, math, os, open_color

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space shooter"

BULLET_DAMAGE = 10
ENEMY_HP = 50
PlAYER_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("bullet.png",0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Ships/spaceShips_008.png",0.5)
        self.hp = PlAYER_HP
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__("Ships/spaceShips_001.png",0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):        #CONFUSING

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0



    def setup(self):
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            damageList = arcade.check_for_collision_with_list(e,self.bullet_list)
            for d in damageList:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp <= 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                    self.score = self.score + HIT_SCORE
                else:
                    self.score = self.score + HIT_SCORE

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_text(str(self.score),20, SCREEN_HEIGHT - 40, open_color.white,16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()




    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.player.position_x = x
        self.player.position_y = y
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()