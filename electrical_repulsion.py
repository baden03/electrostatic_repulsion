import numpy as np
import bpy

def random_point_on_sphere(radius):
    """Generate a random point on a sphere of given radius."""
    theta = 2 * np.pi * np.random.rand()
    phi = np.arccos(2 * np.random.rand() - 1)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return x, y, z

def electrostatic_repulsion(points, spheres, radius, iterations=500, time_step=0.005, k_constant=1, equilibrium_threshold=2.63):
    """Apply electrostatic repulsion to points until equilibrium, and animate the process."""
    max_force = 100
    min_count = 0
    for iteration in range(iterations):
        forces = np.zeros_like(points)
        max_force_magnitude = 0  # To track the largest force magnitude in this iteration

        for i in range(len(points)):
            for j in range(len(points)):
                if i != j:
                    direction = points[i] - points[j]
                    distance = np.linalg.norm(direction)
                    if distance == 0:
                        continue
                    force_magnitude = k_constant / (distance ** 2)
                    force = force_magnitude * (direction / distance)
                    forces[i] += force

                    # Update the max force magnitude if this force is larger
                    if np.linalg.norm(force) > max_force_magnitude:
                        max_force_magnitude = np.linalg.norm(force)

        if max_force_magnitude < max_force:
            max_force = max_force_magnitude
            min_count = 0
            # print(max_force)
        else:
            min_count += 1
        
        # If the largest force in this iteration is below the threshold, we consider it equilibrium
        # 80 @ 1 = 6.95
        # 80 @ 2 = 2.10
        # 80 @ 3 = 1.05
        # 150 @ 2 = 3.7
        # 150 @ 3 = 1.7
        if max_force < equilibrium_threshold or min_count > 100:
            print(f"Equilibrium reached after {iteration} iterations with a max_force_magnitude of {max_force} and min_count of {min_count}.")
            break

        # Update point positions based on forces
        for i in range(len(points)):
            points[i] = points[i] + forces[i] * time_step
            points[i] = points[i] / np.linalg.norm(points[i]) * radius

            # Update the position of the sphere in Blender and set a keyframe
            spheres[i].location = points[i]
            spheres[i].keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

        # Move to the next frame in the timeline
        bpy.context.scene.frame_current += 1

    bpy.context.scene.frame_end = iteration 
    return points

def create_spheres(points, size):
    """Create spheres at given points and return the created Blender objects."""
    spheres = []
    for point in points:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=(point[0], point[1], point[2]))
        sphere = bpy.context.active_object
        spheres.append(sphere)
    return spheres

def print_points(points, spheres, radius):
    blender_points = []
    for i in range(len(points)):
        points[i] = points[i] / np.linalg.norm(points[i]) * radius
        blender_points.append(tuple(points[i]))
        spheres[i].location = points[i]
        spheres[i].keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)
    print(blender_points)

num_points = int(input("Enter number of nodes: "))
radius = float(input("Enter distance from origin for calc: "))
print_it = int(input("Print final coords (0/1): "))
if print_it > 0:
    radius_print = float(input("Enter distance from origin for coords: "))

bpy.context.scene.frame_current = 1 #rewind to first frame
points = np.array([random_point_on_sphere(radius) for _ in range(num_points)])
spheres = create_spheres(points, 0.05)

# Run the repulsion with animation
final_points = electrostatic_repulsion(points, spheres, radius)
if print_it > 0:
    print_points(final_points, spheres, radius_print)
