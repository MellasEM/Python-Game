# Complete your game here
import pygame
from random import randint

pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Player dimensions and movement speed
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
PLAYER_SPEED = 5

# Coin dimensions and falling speed
COIN_WIDTH = 32
COIN_HEIGHT = 32
COIN_SPEED = 3

# Monster dimensions and falling speed
MONSTER_WIDTH = 64
MONSTER_HEIGHT = 64
MONSTER_SPEED = 4

# Number of coins required to win
COINS_TO_COLLECT = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

# Load images
player_image = pygame.image.load("robot.png")
coin_image = pygame.image.load("coin.png")
monster_image = pygame.image.load("monster.png")
door_image = pygame.image.load("door.png")

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Robot Adventure")

# number of lives
coins_collected = 0
lifes_number = 3

# Direction of the robot
move_toleft = False
move_toright = False

#Won games when you colloct 10 coins and lost games when you collide with the moster three times
won_games = 0
lost_games = 0


clock = pygame.time.Clock()


def create_player(x, y):
    """Create a player object.""" # robot 
    player = {
        "x": x,
        "y": y,
        "image": player_image,
        "rect": pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    }
    return player


def create_coin():
    """Create a coin object at a random position at the top of the screen."""
    x = randint(0, WINDOW_WIDTH - COIN_WIDTH)
    y = randint(COIN_HEIGHT, 1500)
    coin = {
        "x": x,
        "y": -y,
        "image": coin_image,
        "rect": pygame.Rect(x, -COIN_HEIGHT, COIN_WIDTH, COIN_HEIGHT)
    }
    return coin


def create_monster():
    """Create a monster object at a random position at the top of the screen."""
    x = randint(0, WINDOW_WIDTH - MONSTER_WIDTH)
    y = randint(MONSTER_HEIGHT, 2000)
    monster = {
        "x": x,
        "y": -y,
        "image": monster_image,
        "rect": pygame.Rect(x, -MONSTER_HEIGHT, MONSTER_WIDTH, MONSTER_HEIGHT)
    }
    return monster


def move(player):
    if move_toleft and player["x"] >= 2:
        player["x"] -= PLAYER_SPEED

    if move_toright and player["x"] <= WINDOW_WIDTH - PLAYER_WIDTH:
        player["x"] += PLAYER_SPEED

    player["rect"].x = player["x"]


def falling_coins(objects: list):
    for object in objects:
        if object["y"] + COIN_HEIGHT < WINDOW_HEIGHT:
                object["y"] += COIN_SPEED
                object["rect"].y = object["y"]  
        else:
            object["x"] = randint(0, WINDOW_WIDTH - COIN_WIDTH)
            object["y"] = -randint(100, 1000)
            object["rect"].x = object["x"]
            object["rect"].y = object["y"]


def falling_monsters(objects):
    for object in objects:
        if object["y"] + MONSTER_HEIGHT < WINDOW_HEIGHT:
                object["y"] += MONSTER_SPEED
                object["rect"].y = object["y"]
        else:
            object["x"] = randint(0, WINDOW_WIDTH - MONSTER_WIDTH)
            object["y"] = -randint(100, 1000)    
            object["rect"].x = object["x"]
            object["rect"].y = object["y"]


def check_collision(player, coins, monsters):
    #this function is to count how many lifes and coins counted
    global lifes_number
    global coins_collected

    robot_rect = player["rect"]
    for monster in monsters:
        monster_rect = monster["rect"]
        if collision_detection(robot_rect, monster_rect):
            player["x"] = 0
            monsters.remove(monster)
            lifes_number -= 1
            break
    
    for coin in coins:
        coin_rect = coin["rect"]
        if collision_detection(robot_rect, coin_rect):
            coins.remove(coin)
            coins_collected += 1
            break


def collision_detection(rect1, rect2):
    """Check if two rectangles collide."""
    return rect1.colliderect(rect2)


def lives():
    # I used this funtction to restart the game after lossing a game by dying 3 times
    global lost_games

    if lifes_number == 0:
        lost_games += 1
        restart()


def check_coins():
    # I used this funtction to restart the game after wining a game after collecting 10 coins
    global won_games

    if coins_collected == 10:
        won_games += 1
        restart()


def draw_counter():
    #This function will create text counters for How many coines collected, how many lives left, won games(each won games is by collection 10 coins) and lost games(each lost games is after colliding with the monster)
    """Draw the counter on the screen."""
    font = pygame.font.SysFont(None, 36)

    coin_text = font.render("Coins: {}".format(coins_collected), True, WHITE, BLACK )
    lives_text = font.render("Life Left: {}".format(lifes_number), True, WHITE, BLACK )
    lost_text = font.render("Won Games: {}".format(won_games), True, WHITE, BLACK )
    won_text = font.render("Lost Games: {}".format(lost_games), True, WHITE, BLACK )

    window.blit(coin_text, (0, 10))
    window.blit(lives_text, (100, 10))
    window.blit(lost_text, (230, 10))
    window.blit(won_text, (410, 10))


def restart():
    #funstion to restart after wining or loosing
    global player, coins_collected, lifes_number, move_toleft, move_toright, coins, monsters, won_games, lost_games

    player = create_player(0, WINDOW_HEIGHT - 100)  
    coins_collected = 0
    lifes_number = 3
    move_toleft = False
    move_toright = False
    coins = []
    monsters = []

    game()


def game():
    """Main game loop."""
    player = create_player(0, WINDOW_HEIGHT - 100)
    coins = []
    monsters = []

    for i in range(COINS_TO_COLLECT):
        coins.append(create_coin())

    for i in range(15):
        monsters.append(create_monster())

    #check_events()
    while True:
        for event in pygame.event.get():
            global move_toleft
            global move_toright
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_toleft = True
                if event.key == pygame.K_RIGHT:
                    move_toright = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_toleft = False
                if event.key == pygame.K_RIGHT:
                    move_toright = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        move(player)
        falling_coins(coins)
        falling_monsters(monsters)
        check_collision(player, coins, monsters)
        lives()
        check_coins()

        window.fill(WHITE)

        for coin in coins:
            window.blit(coin["image"], (coin["x"], coin["y"]))

        for monster in monsters:
            window.blit(monster["image"], (monster["x"], monster["y"]))

        draw_counter()

        window.blit(player["image"], (player["x"], player["y"]))
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    game()
