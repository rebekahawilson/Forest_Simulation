import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
forest_size = 50  # Size of the forest (grid size)
prob_growth_base = 0.01  # Base probability of a new tree growing in an empty spot
num_steps = 200  # Number of steps in the simulation
seed_dispersion_radius = 1  # Radius for seed dispersal

# Forest grid (0 = empty, 1 = young tree, 2 = mature tree, 3 = dead tree)
forest = np.zeros((forest_size, forest_size), dtype=int)

# Environmental grids
sunlight = np.random.rand(forest_size, forest_size)  # Random sunlight values between 0 and 1
soil_quality = np.random.rand(forest_size, forest_size)  # Random soil quality values between 0 and 1
rainfall = np.random.rand(forest_size, forest_size)  # Random rainfall values between 0 and 1

# Function to update forest state
def update_forest(forest):
    new_forest = forest.copy()
    
    for i in range(forest_size):
        for j in range(forest_size):
            # Calculate average environmental influence
            growth_factor = (sunlight[i, j] + soil_quality[i, j] + rainfall[i, j]) / 3
            
            if forest[i, j] == 0:  # Empty spot
                prob_growth = prob_growth_base * growth_factor
                if np.random.rand() < prob_growth:
                    new_forest[i, j] = 1  # A young tree grows
            elif forest[i, j] == 1:  # Young tree
                if np.random.rand() < 0.05:  # Fixed maturation probability
                    new_forest[i, j] = 2  # It becomes a mature tree
            elif forest[i, j] == 2:  # Mature tree
                if np.random.rand() < 0.02:  # Fixed death probability
                    new_forest[i, j] = 3  # The tree dies
                else:
                    # Seed dispersal: try to plant a new tree in adjacent empty cells
                    for di in range(-seed_dispersion_radius, seed_dispersion_radius + 1):
                        for dj in range(-seed_dispersion_radius, seed_dispersion_radius + 1):
                            if abs(di) + abs(dj) <= seed_dispersion_radius:  # Check within the radius
                                ni, nj = i + di, j + dj
                                if 0 <= ni < forest_size and 0 <= nj < forest_size and new_forest[ni, nj] == 0:
                                    new_forest[ni, nj] = 1  # A young tree grows from seed
            elif forest[i, j] == 3:  # Dead tree
                new_forest[i, j] = 0  # Dead tree decays and space becomes empty
    return new_forest

# Set up the figure and axis for plotting
fig, ax = plt.subplots(figsize=(6, 6))
cmap = plt.get_cmap('YlGn')  # Color map for forest (green colors)

# Function to animate the forest growth
def animate(step):
    global forest
    ax.clear()
    ax.set_title(f"Forest Development - Step {step}")
    ax.imshow(forest, cmap=cmap, vmin=0, vmax=3)

    # Adding legend outside the grid
    handles = [
        plt.Line2D([0], [0], color=cmap(0), lw=4, label='Empty Space'),
        plt.Line2D([0], [0], color=cmap(0.5), lw=4, label='Young Tree'),
        plt.Line2D([0], [0], color=cmap(0.75), lw=4, label='Mature Tree'),
        plt.Line2D([0], [0], color='brown', lw=4, label='Dead Tree')
    ]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1), title="Legend")

    forest = update_forest(forest)

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=100)

# Show the animation
plt.tight_layout(rect=[0, 0, 0.75, 1])  # Adjust layout to make room for the legend
plt.show()
