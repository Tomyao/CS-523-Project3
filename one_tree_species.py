import random
from copy import deepcopy
import matplotlib.pyplot as plt

# 0 stands for empty
# 1 stands for tree
# 2 stands for burning

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
		return 1


# Updates the array
def update_array(array,p):
	temp_array = deepcopy(array)
	for x in range(grid_width):
		for y in range(grid_height):
			array[x][y] = update_cell(temp_array,x,y,p)

# returns whether all cells are empty
# used only in get_longevity which is not used
#def is_empty(array):
#	for x in range(grid_width):
#		for y in range(grid_height):
#			if (array[x][y] != 0):
#				return False
#	return True

# returns longevity for a given probability p
# the forest is never empty for many values of p so finding a value of p
# which maximizes longevity is pointless
#def get_longevity(p):
#	forest = init_a_forest()
	# initialize values in forest
#	update_array(forest,p)
#	counter = 0
#	while (is_empty(forest) != True):
#		update_array(forest,p)
#		counter = counter + 1
#		print counter
#	return counter

# returns how many cells are trees in the array
def num_tree(array):
	trees = 0
	for x in range(grid_width):
		for y in range(grid_height):
			if (array[x][y] == 1):
				trees += 1
	return trees

# returns biomass for a given probability p over it's lifetime
def get_biomass(p):
	forest = init_a_forest()
	# initialize values in forest
	update_array(forest,p)
	# initialize biomass
	total_biomass = num_tree(forest)
	old_average_biomass = -1
	iter = 0
	while (iter < max_time_steps):
		update_array(forest,p)
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

max_prob = -1
max_biomass = 0

# Probability starts at 0
prob = 0

probabilities = []
fitnesses = []

while (True):

	print prob

	# Calculate fitness
	biomass = get_biomass(prob)

	# Save data for plotting
	probabilities.append(prob)
	fitnesses.append(biomass)

	# Check for new max_biomass
	if (biomass > max_biomass):
		max_prob = prob
		max_biomass = biomass

	# Mutate
	prob += random.uniform(0, 1)/100
	if (prob >= 1):
		break

print "max_prob: " + str(max_prob)
print "max_biomass: " + str(max_biomass)

plt.plot(probabilities,fitnesses,'bo')
plt.show()