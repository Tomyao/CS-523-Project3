import random
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

# 0 stands for empty
# 1 stands for tree
# 2 stands for burning
# 3 stands for tree saved by firefighter

grid_height = 250
grid_width = 250

max_time_steps = 5000

def init_a_forest():
	forest = [[0 for x in range(grid_width)] for y in range(grid_height)]
	return forest

# returns what the updated cell's value should be
def update_cell(array,x,y,p):
	# first check if cell is empty
	if (array[x][y] == 0):
		# with probability p it turns into forest
		outcome = random.uniform(0, 1)
		if (outcome < p):
			return 1
		else:
			return 0
	# then check if cell is burning
	if (array[x][y] == 2):
		return 0
	# cell must be forest, so check the 8 neighbors for burning status
	if (x-1 >= 0):
		if array[x-1][y] == 2:
			return 2
	if (y-1 >= 0):
		if array[x][y-1] == 2:
			return 2
	if (x-1 >= 0) and (y-1 >= 0):
		if array[x-1][y-1] == 2:
			return 2;
	if (x+1 < grid_width):
		if array[x+1][y] == 2:
			return 2
	if (y+1 < grid_height):
		if array[x][y+1] == 2:
			return 2
	if (x+1 < grid_width) and (y+1 < grid_height):
		if array[x+1][y+1] == 2:
			return 2
	if (x+1 < grid_width) and (y-1 >= 0):
		if array[x+1][y-1] == 2:
			return 2
	if (x-1 >= 0) and (y+1 < grid_height):
		if array[x-1][y+1] == 2:
			return 2
	# cell is forest with no burning neighbors
	# lightning strike occurs with probability 1/1000
	outcome = random.uniform(0, 1)
	if (outcome < 0.001):
		return 2
	else:
		return array[x][y]


# Randomly changes f cells to forest put out by firefighters
def fight_fire(array,f):
	# Cast to numpy array
	temparray = np.asarray(array)
	# Store original shape
	shape = temparray.shape
    # Flatten to 1D
	temparray = temparray.flatten()    
	burning = [i for i, x in enumerate(temparray) if x == 2]
	if (len(burning) <= f):
		for index in range(len(burning)):
			temparray[burning[index]] = 3
	else:
		random.shuffle(burning)
		for index in range(f):
			temparray[burning[index]] = 3
	# Restore original shape
	temparray = temparray.reshape(shape)
	# Save changes into array
	array = temparray.tolist()

# Updates the array
def update_array(array,p,f):
	temp_array = deepcopy(array)
	for x in range(grid_width):
		for y in range(grid_height):
			array[x][y] = update_cell(temp_array,x,y,p)
	fight_fire(array,f)

# returns how many cells are trees in the array
def num_tree(array):
	trees = 0
	for x in range(grid_width):
		for y in range(grid_height):
			if (array[x][y] == 1 or array[x][y] == 3):
				trees += 1
	return trees

# returns biomass for a given probability p over it's lifetime with f firefighters
def get_biomass(p,f):
	forest = init_a_forest()
	# initialize values in forest
	update_array(forest,p,f)
	# initialize biomass
	total_biomass = num_tree(forest)
	old_average_biomass = -1
	iter = 0
	while (iter < max_time_steps):
		update_array(forest,p,f)
		total_biomass += num_tree(forest)
		iter += 1
		# If average biomass doesn't change by more than 10
		# then return average biomass
		if (abs(total_biomass/iter - old_average_biomass) <= 10):
			return total_biomass/iter
		old_average_biomass = total_biomass/iter
	# return average biomass
	return total_biomass/max_time_steps

# ===============================================
# MAIN
# ===============================================

# Firefighters starts at 0
firefighter = 0

# Using probability of tree growth that generated highest average
# biomass from the one tree species simulation
prob = 0.169988214073

firefighters = []
fitnesses = []

while (firefighter <= 1000):

	print firefighter

	# Calculate fitness
	biomass = get_biomass(prob,firefighter)

	# Save data for plotting
	firefighters.append(firefighter)
	fitnesses.append(biomass)

	# Update number of firefighters
	firefighter += 50

plt.plot(firefighters,fitnesses,'bo')
plt.show()