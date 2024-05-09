# exp 2

import random

# Define grid size and agent position
GRID_SIZE = 5
agent_pos = [0, 0]

# Define obstacle positions
obstacles = [[1, 2], [2, 1], [3, 3]]

# Define goal position
goal_pos = [4, 4]

# Function to move the agent
def move_agent(direction):
    global agent_pos
    new_pos = agent_pos[:]
    if direction == 'up' and agent_pos[0] > 0:
        new_pos[0] -= 1
    elif direction == 'down' and agent_pos[0] < GRID_SIZE - 1:
        new_pos[0] += 1
    elif direction == 'left' and agent_pos[1] > 0:
        new_pos[1] -= 1
    elif direction == 'right' and agent_pos[1] < GRID_SIZE - 1:
        new_pos[1] += 1
    if new_pos not in obstacles:
        agent_pos = new_pos

# Function to check if the agent reached the goal
def check_goal():
    if agent_pos == goal_pos:
        return True
    return False

# Main program loop
while True:
    print("Agent position:", agent_pos)
    direction = random.choice(['up', 'down', 'left', 'right'])
    print("Agent moving", direction)
    move_agent(direction)
    if check_goal():
        print("Goal reached!")
        break
