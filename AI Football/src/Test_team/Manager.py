# Choose names for your players and team
# Choose a funny name for each player and your team
# Use names written only in cyrillic
# Make sure that the name is less than 11 characters
# Don't use profanity!!!
import math

import numpy as np

memory_flag_goalkeeper = 0


def team_properties():
    properties = dict()
    player_names = ["Магдалена", "Дуле", "Раде"]
    properties['team_name'] = "Весели Лини anti"
    properties['player_names'] = player_names
    properties['image_name'] = 'Blue.png'  # use image resolution 153x153
    properties['weight_points'] = (29.5, 19.5, 19.5)
    properties['radius_points'] = (10, 0.5, 1)
    properties['max_acceleration_points'] = (10, 40, 1)
    properties['max_speed_points'] = (30, 40, 27.5)
    properties['shot_power_points'] = (20.5, 20, 1)

    # calculate_points(properties)
    return properties


# Return the player that is in 10% of its radius in proximity of the ball
def detect_player_with_ball(team, ball):
    player1_coor = (team[0]["x"], team[0]["y"])
    player1_alpha = team[0]["alpha"]
    player2_coor = (team[1]["x"], team[1]["y"])
    player2_alpha = team[1]["alpha"]
    player3_coor = (team[2]["x"], team[2]["y"])
    player3_alpha = team[2]["alpha"]
    ball_coor = (ball["x"], ball["y"])
    ball_alpha = ball["alpha"]

    player1_radius = team[0]["radius"]
    player2_radius = team[1]["radius"]
    player3_radius = team[2]["radius"]
    ball_radius = ball["radius"]

    if ball_radius + player1_radius >= math.sqrt(
            (ball_coor[0] - player1_coor[0]) ** 2 + (ball_coor[1] - player1_coor[1]) ** 2):
        return team[0]
    elif ball_radius + player2_radius >= math.sqrt(
            (ball_coor[0] - player2_coor[0]) ** 2 + (ball_coor[1] - player2_coor[1]) ** 2):
        return team[1]
    elif ball_radius + player3_radius >= math.sqrt(
            (ball_coor[0] - player3_coor[0]) ** 2 + (ball_coor[1] - player3_coor[1]) ** 2):
        return team[2]
    else:
        return None


# Calculate the angle from the first argument to the second in radians
def calculate_angle(player_pos, obj_pos):
    # Calculate the differences in x and y coordinates between the player and the ball
    delta_x = obj_pos[0] - player_pos[0]
    delta_y = obj_pos[1] - player_pos[1]

    # Calculate the angle using arctangent, and convert it to degrees
    angle_rad = np.arctan2(delta_y, delta_x)

    # Ensure the angle is between 0 and 2*pi
    if angle_rad < 0:
        angle_rad += 2 * np.pi

    return angle_rad


# Check if the points are correctly placed
def calculate_points(properties):
    sum_all = 0
    sum_players = []

    for i in range(3):
        sum_player = 0
        sum_all += properties['weight_points'][i]
        sum_all += properties['radius_points'][i]
        sum_all += properties['max_acceleration_points'][i]
        sum_all += properties['max_speed_points'][i]
        sum_all += properties['shot_power_points'][i]

        sum_player += properties['weight_points'][i]
        sum_player += properties['radius_points'][i]
        sum_player += properties['max_acceleration_points'][i]
        sum_player += properties['max_speed_points'][i]
        sum_player += properties['shot_power_points'][i]

        sum_players.append(sum_player)


# Return the player that is in proximity to the first player with an offset of 10% of the sum of their radius,
# or return None
def detect_collision(first, second, third):
    player1_pos = (first["x"], first["y"])
    player2_pos = (second["x"], second["y"])
    player3_pos = (third["x"], third["y"])

    player1_radius = first["radius"]
    player2_radius = second["radius"]
    player3_radius = third["radius"]

    if (player1_radius + player2_radius) >= math.sqrt(
            (player1_pos[0] - player2_pos[0]) ** 2 + (player1_pos[1] - player2_pos[1]) ** 2) - 50:
        return second
    elif (player1_radius + player3_radius) >= math.sqrt(
            (player1_pos[0] - player3_pos[0]) ** 2 + (player1_pos[1] - player3_pos[1]) ** 2) - 50:
        return third
    else:
        return None


def move_around_opponent(player_coords, opponent_coords, distance):
    # Convert Cartesian coordinates to polar coordinates
    player_rho, player_phi = cart_to_polar(*player_coords)
    opponent_rho, opponent_phi = cart_to_polar(*opponent_coords)

    # Calculate the new angle for the player to move around the opponent
    new_phi = opponent_phi + math.pi / 2  # Move 90 degrees counter-clockwise around the opponent

    # Convert back to Cartesian coordinates
    new_x, new_y = polar_to_cart(distance, new_phi)

    # Update player coordinates
    new_player_x = player_coords[0] + new_x
    new_player_y = player_coords[1] + new_y

    return new_player_x, new_player_y


def cart_to_polar(x, y):
    rho = math.sqrt(x ** 2 + y ** 2)
    phi = math.atan2(y, x)
    return rho, phi


def polar_to_cart(rho, phi):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return x, y


# Return the player from argument 2 that is in proximity of 60 pixels to player
def detect_collision_with_opponent(player, their_team):
    first = their_team[0]
    second = their_team[1]
    third = their_team[2]

    player_coor = (player["x"], player["y"])
    first_coor = (first["x"], first["y"])
    second_coor = (second["x"], second["y"])
    third_coor = (third["x"], third["y"])

    if math.sqrt((player_coor[0] - first_coor[0]) ** 2 + (player_coor[1] - first_coor[1]) ** 2) <= 60:
        return first
    elif math.sqrt((player_coor[0] - second_coor[0]) ** 2 + (player_coor[1] - second_coor[1]) ** 2) <= 60:
        return second
    elif math.sqrt((player_coor[0] - third_coor[0]) ** 2 + (player_coor[1] - third_coor[1]) ** 2) <= 60:
        return third
    else:
        return None


angle = (3 / 4) * np.pi


def calculate_points_for_polar_coordinates(opponent, offset):
    distance_from_opponent = opponent["radius"] + offset
    opponent_x = opponent["x"]
    opponent_y = opponent["y"]
    global angle

    x = distance_from_opponent + math.cos(angle) + opponent_x
    y = -distance_from_opponent + math.sin(angle) + opponent_y
    angle = angle - (np.pi / 4)
    if angle < 0:
        angle = (3 / 4) * np.pi

    return x, y


def player1(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    player = our_team[0]
    player_pos = (player["x"], player["y"])
    ball_pos = (ball["x"], ball["y"])

    if your_side == "right":
        goal_coordinates = (1272, 460.5)
        their_goal_coordinates = (74, 460.5)
    else:
        goal_coordinates = (74, 460.5)
        their_goal_coordinates = (1272, 460.5)

    keeper = dict()

    # If you are looking at your side of the field, don't shoot
    if (your_side == "left" and (1 / 2) * np.pi <= player["alpha"] <= (3 / 2) * np.pi) or (your_side == "right" and (
            0 <= player["alpha"] <= (1 / 2) * np.pi or (3 / 2) * np.pi <= player["alpha"] <= 2 * np.pi)):
        keeper['shot_request'] = False
        keeper['shot_power'] = 0
    else:
        keeper['shot_request'] = True
        keeper['shot_power'] = np.inf

    keeper["force"] = np.inf

    # Keep memory for the goalkeeper to intercept balls behind them
    global memory_flag_goalkeeper
    if memory_flag_goalkeeper == 1:
        memory_flag_goalkeeper = 0
        keeper["alpha"] = calculate_angle(player_pos, ball_pos)

    # If you are in collision with one of our players, go to the other side of your player
    collided_teammate = detect_collision(our_team[0], our_team[1], our_team[2])
    if collided_teammate is not None:
        keeper["alpha"] = (collided_teammate["alpha"] + np.pi) % (2 * np.pi)
        return keeper

    if (player_pos[0] <= 100 and 343 <= player_pos[1] <= 578 and your_side == "left") or (
            player_pos[0] >= 1266 and 343 <= player_pos[1] <= 578 and your_side == "right"):
        # If you are in front of the goal, look at the ball
        keeper["alpha"] = calculate_angle(player_pos, ball_pos)
    elif (ball_pos[0] <= 341.5 and your_side == "left") or (ball_pos[0] >= 1024.5 and your_side == "right"):
        # If the ball is in I quadrant, go towards the ball
        keeper["alpha"] = calculate_angle(player_pos, ball_pos)
    else:
        # Else go towards the goal
        keeper['alpha'] = calculate_angle(player_pos, goal_coordinates)

    # If the ball is behind the keeper
    if memory_flag_goalkeeper != 1:
        if ball_pos[0] - player_pos[0] < 0 and your_side == "left":
            keeper["alpha"] = calculate_angle(player_pos, (ball_pos[0], ball_pos[1] - 10))
            memory_flag_goalkeeper = 1
        elif player_pos[0] - ball_pos[0] < 0 and your_side == "right":
            keeper["alpha"] = calculate_angle(player_pos, (ball_pos[0], ball_pos[1] - 10))
            memory_flag_goalkeeper = 1

    return keeper


def player2(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    player = our_team[1]

    attacker = dict()

    player_pos = (player["x"], player["y"])
    ball_pos = (ball["x"], ball["y"])

    if your_side == "left":
        their_goal_coordinates = (1316, 460.5)
        our_goal_coordinates = (50, 460.5)
    else:
        their_goal_coordinates = (50, 460.5)
        our_goal_coordinates = (1316, 460.5)

    attacker['force'] = np.inf

    if ((ball_pos[0] >= 1024.5 and your_side == "left") or (
            ball_pos[0] <= 341.5 and your_side == "right")):
        attacker['shot_request'] = True
    else:
        attacker['shot_request'] = False

    attacker['shot_power'] = player["shot_power_max"] / 10
    ball_acquired = detect_player_with_ball(our_team, ball) == our_team[1]

    if (ball_acquired and player_pos[0] > 853.75 and your_side == "left") or (
            ball_acquired and player_pos[0] < 512.25 and your_side == "right"):
        attacker["alpha"] = calculate_angle(player_pos, their_goal_coordinates)
        attacker['shot_request'] = True
        if (player_pos[0] > 1024.5 and your_side == "left") or (player_pos[0] < 341.5 and your_side == "right"):
            attacker["shot_power_max"] = np.inf
        return attacker

    if not ball_acquired:
        attacker["alpha"] = calculate_angle(player_pos, ball_pos)
    elif (player_pos[0] < 683 and your_side == "left") or (
            player_pos[0] >= 683 and your_side == "right"):
        attacker["alpha"] = calculate_angle(player_pos, our_goal_coordinates)
    else:
        attacker["alpha"] = calculate_angle(player_pos, their_goal_coordinates)

    return attacker


def find_goalkeeper(their_team, our_side):
    goalkeeper = their_team[0]
    position = goalkeeper["x"]

    if our_side == "left":
        for player in their_team:
            if player["x"] >= position:
                position = player["x"]
                goalkeeper = player
    else:
        for player in their_team:
            if player["x"] < position:
                position = player["x"]
                goalkeeper = player

    return goalkeeper


def find_slimmest_opponent(their_team, your_side):
    min_mass = their_team[0]["mass"]
    min_mass_player = their_team[0]
    for player in their_team:
        if player["mass"] < min_mass:
            min_mass = player["mass"]
            min_mass_player = player

    if min_mass_player["x"] < 683 and your_side == "left":
        return min_mass_player
    if min_mass_player["x"] > 683 and your_side == "right":
        return min_mass_player

    return None


def player3(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    player = our_team[2]
    helper = dict()

    player_position = (player["x"], player["y"])
    ball_position = (ball["x"], ball["y"])

    if your_side == "left":
        their_goal_coordinates = (1316, 460.5)
        our_goal_coordinates = (50, 460.5)
    else:
        their_goal_coordinates = (50, 460.5)
        our_goal_coordinates = (1316, 460.5)

    helper['force'] = np.inf
    helper["shot_request"] = True
    helper['shot_power'] = np.inf

    if ball_position == (683, 460):
        helper["alpha"] = calculate_angle(player_position, ball_position)
        return helper

    ball_acquired = detect_player_with_ball(our_team, ball) == our_team[2]
    goalkeeper = find_goalkeeper(their_team, your_side)
    goalkeeper_position = (goalkeeper["x"], goalkeeper["y"])

    if (ball_position[0] > 683 and your_side == "left") or (ball_position[0] <= 683 and your_side == "right"):
        if goalkeeper is not None:
            helper["alpha"] = calculate_angle(player_position, goalkeeper_position)
        else:
            helper["alpha"] = calculate_angle(player_position, (683, 460))
        return helper
    elif (ball_position[0] < 683 and your_side == "left") or (ball_position[0] >= 683 and your_side == "right"):
        slimmest_opponent_in_our_side = find_slimmest_opponent(their_team, your_side)
        if slimmest_opponent_in_our_side is not None:
            helper["alpha"] = calculate_angle(player_position, (slimmest_opponent_in_our_side["x"], slimmest_opponent_in_our_side["y"]))
        else:
            helper["alpha"] = calculate_angle(player_position, (683, 460))
        return helper
    else:
        helper["alpha"] = calculate_angle(player_position, (683, 460))

    if ball_acquired:
        helper["alpha"] = calculate_angle(player_position, their_goal_coordinates)
        return helper
    else:
        helper["alpha"] = calculate_angle(player_position, (683, 460))

    return helper


def decision(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    manager_decision = [dict(), dict(), dict()]

    manager_decision[0] = player1(our_team, their_team, ball, your_side, half, time_left, our_score, their_score)
    manager_decision[1] = player2(our_team, their_team, ball, your_side, half, time_left, our_score, their_score)
    manager_decision[2] = player3(our_team, their_team, ball, your_side, half, time_left, our_score, their_score)

    return manager_decision
