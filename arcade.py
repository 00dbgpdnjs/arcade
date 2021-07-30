import os
import pygame

pygame.init() # essential after importing pygame

screen_width = 640 
screen_height = 480 
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("arcade")

clock = pygame.time.Clock() # FPS ??

current_path = os.path.dirname(__file__) # return the path of this file
image_path = os.path.join(current_path, "images") 

background = pygame.image.load(os.path.join(image_path, "background.jpg"))

stage = pygame.image.load(os.path.join(image_path, "stage.jpg"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character =  pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height

character_to_x = 0
character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.jpg"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = [] # Manage multiple shots at a time as a list

weapon_speed = 10

ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# First speed by ball size
ball_speed_y = [-18, -15, -12, -9] # balloon1: -18 ... balloon4: -9

balls = [] # Manage the increased number as the ball splits

# Add first ball/ {}: Manage the information of a ball in dictionary
balls.append({ 
    "pos_x" : 50, 
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x": 3,
    "to_y": -6,
    "init_spd_y" : ball_speed_y[0]})

# To remove from the list if a value are in the var
weapon_to_remove = -1
ball_to_remove = -1

game_font = pygame.font.Font(None, 40)
total_time = 25
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # Weapons fired
                #pass
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x 

    # boundry value
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # y-pos of weapon (-- weapon_speed); Weapons fired upward (x-pos fixed) / boundry value
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons if w[1] - weapon_speed > 0] 
    #weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0] # boundry value # myself

    for ball_idx, ball_val in enumerate(balls): # refer to 'list.py' # do i have to do -> enumerate X
        #print(ball_idx, ball_val)
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # Change the direction of movement of the ball when it touches the side wall
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1  # 이 코드가 'ball_val["pos_x"] += ball_val["to_x"]' 아래 있으면 pos_x가 485일 때 부터 to_X가 -1 1 -1 1 왔다갔다하는 이유 ??
        
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # Adjust the speed in three dimensions according to the parabola
            ball_val["to_y"] += 0.5

        # Reflect the ball's speed to its position
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # collision

    # Set the informatino of character_rect
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # Set the informatino of ball_rect
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # Process collision between characer and balls
        if character_rect.colliderect(ball_rect): 
            running = False
            break # Escape from the for statement

        # To process collision with weapon
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # Set the informatino of weapon_rect
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # Process collision between weapon and balls
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # Set to eliminate collided weapons
                ball_to_remove = ball_idx

                # The effect of looking ball split
                if ball_img_idx < 3:
                    # a ball to be divided
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # a divided ball
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # a ball bouncing to the left
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, 
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,
                        "img_idx" : ball_img_idx + 1, 
                        "to_x": -3, # to the left
                        "to_y": -6, # To go up a little and go down.
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})

                    # a ball bouncing to the right
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, 
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,
                        "img_idx" : ball_img_idx + 1, 
                        "to_x": 3, 
                        "to_y": -6, 
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})

                break
            else: # Refer to 'break.py'
                continue
            break

    # Eliminate collided items
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1 # ?? -> Without this code, we have an error called 'del balls[ball_to_remove] IndexError: list assignment index out of range' ; Continue deleting a deleted value ; impossible
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # You win, if a user get rid of all of balls
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) # Weapon movement is processed by 'y-pos of weapon' code
    for idx, val in enumerate(balls): # do i have to do -> enumerate X
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    elasped_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elasped_time)), True, (255, 255, 255)) # (,antialias,)
    screen.blit(timer, (10, 10))

    # timeout
    if total_time - elasped_time <= 0:
        game_result = "Timeout"
        running = False
    
    pygame.display.update()

# Print 'game_result'
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2))) # No int is fine
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()