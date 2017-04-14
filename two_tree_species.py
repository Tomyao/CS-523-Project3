import random
from copy import deepcopy
import matplotlib.pyplot as plt

# 0 stands for empty
# 1 stands for tree type 1
# 3 stands for tree type 2
# 2 stands for burning

grid_height = 250
grid_width = 250

max_time_steps = 5000

def init_a_forest():
	forest = [[0 for x in range(grid_width)] for y in range(grid_height)]
	return forest

# returns what the updated cell's value should be
def update_cell(array,x,y,p1,p2):
	# first check if cell is empty
	if (array[x][y] == 0):
		# with probability p1 it turns into tree type 1
		# with probability p2 it turns into tree type 2
		outcome = random.uniform(0, 1)
		if (outcome < p1):
			return 1
		elif (outcome < p1 + p2):
			return 3
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

# Updates the array
def update_array(array,p1,p2):
	temp_array = deepcopy(array)
	for x in range(grid_width):
		for y in range(grid_height):
			array[x][y] = update_cell(temp_array,x,y,p1,p2)

# returns how many cells are trees in the array
def num_tree(array):
	trees = 0
	for x in range(grid_width):
		for y in range(grid_height):
			if (array[x][y] == 1 or array[x][y] == 3):
				trees += 1
	return trees

# returns biomass for a given probability p over it's lifetime
def get_biomass(p1,p2):
	forest = init_a_forest()
	# initialize values in forest
	update_array(forest,p1,p2)
	# initialize biomass
	total_biomass = num_tree(forest)
	old_average_biomass = -1
	iter = 0
	while (iter < max_time_steps):
		update_array(forest,p1,p2)
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

max_prob1 = -1
max_prob2 = -1
max_biomass = 0

# Probability 1 and 2 start at 0
prob1 = 0
prob2 = 0

probabilities = []
fitnesses = []

while (True):

	print (prob1 + prob2)

	# First calculate fitness
	biomass = get_biomass(prob1,prob2)

	# Save data for plotting
	probabilities.append(prob1 + prob2)
	fitnesses.append(biomass)

	# Check for new max_biomass
	if (biomass > max_biomass):
		max_prob1 = prob1
		max_prob2 = prob2
		max_biomass = biomass

	# Mutate
	prob1 += random.uniform(0, 1)/200
	prob2 += random.uniform(0, 1)/200
	if (prob1 + prob2 >= 1):
		break

print "max_prob1: " + str(max_prob1)
print "max_prob2: " + str(max_prob2)
print "max_biomass: " + str(max_biomass)

plt.plot(probabilities,fitnesses,'bo')
plt.show()