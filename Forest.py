import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
forest_size = 50  # Size of the forest (grid size)
prob_growth = 0.01  # Probability of a new tree growing in an empty spot
prob_mature = 0.05  # Probability of a young tree maturing
prob_death = 0.02  # Probability of a mature tree dying
num_steps = 200  # Number of steps in the simulation

# Forest grid (0 = empty, 1 = young tree, 2 = mature tree, 3 = dead tree)
forest = np.zeros((forest_size, forest_size), dtype=int)

# Function to update forest state
def update_forest(forest):
    new_forest = forest.copy()
    for i in range(forest_size):
        for j in range(forest_size):
            if forest[i, j] == 0:  # Empty spot
                if np.random.rand() < prob_growth:
                    new_forest[i, j] = 1  # A young tree grows
            elif forest[i, j] == 1:  # Young tree
                if np.random.rand() < prob_mature:
                    new_forest[i, j] = 2  # It becomes a mature tree
            elif forest[i, j] == 2:  # Mature tree
                if np.random.rand() < prob_death:
                    new_forest[i, j] = 3  # The tree dies
            elif forest[i, j] == 3:  # Dead tree
                new_forest[i, j] = 0  # Dead tree decays and space becomes empty
    return new_forest

# Set up the figure and axis for plotting
fig, ax = plt.subplots()
cmap = plt.get_cmap('YlGn')  # Color map for forest (green colors)

# Function to animate the forest growth
def animate(step):
    global forest
    ax.clear()
    ax.set_title(f"Forest Development - Step {step}")
    ax.imshow(forest, cmap=cmap, vmin=0, vmax=3)
    forest = update_forest(forest)

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=100)

# Show the animation
plt.show()
