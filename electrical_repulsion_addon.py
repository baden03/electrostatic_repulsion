bl_info = {
    "name": "Electrical Repulsion",
    "author": "Twinpictures",
    "version": (1, 0, 2),
    "blender": (3, 6, 4),
    "location": "View3D > Tool Shelf > Tool",
    "description": "Evenly distribute nodes on a sphere using Electrostatic Repulsion.",
    "category": "Tool",
}

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

def electrostatic_repulsion(points, spheres, radius, iterations=500, time_step=0.005, k_constant=1, convergence_threshold=0):
    """Apply electrostatic repulsion to points until equilibrium, and animate the process."""    
    max_force_history = []
    max_force = 100
    N = 100  # Number of iterations to consider for mean variation

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

        # Update max_force_history with the variation in max_force
        if iteration > 0:
            max_force_history.append(abs(max_force_magnitude - max_force))
       
        if len(max_force_history) > N:
            max_force_history.pop(0)  # Remove oldest value

        if max_force_magnitude < max_force:
            max_force = max_force_magnitude
                
        # Check for convergence based on mean variation in max_force over the last N iterations
        if len(max_force_history) == N:
            mean_variation = sum(max_force_history) / N
            if mean_variation < convergence_threshold:
                print(f"Breaking due to mean variation {mean_variation} being less than the Convergence Threshold {convergence_threshold}.")
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
    print(f"Equilibrium reached after {iteration} iterations with a max_force_magnitude of {max_force}.")
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
    
    return(blender_points)

class ElectricalRepulsionProperties(bpy.types.PropertyGroup):
    # The total number of nodes to distribute on the sphere. More nodes may require more iterations for a stable configuration.
    num_points: bpy.props.IntProperty(
        name="Number of Nodes",
        default=80,
        min=2,
        description="The total number of nodes to distribute on the sphere."
    )
    # The distance from the origin to the nodes on the sphere. A larger radius may affect the time to reach equilibrium.
    radius: bpy.props.FloatProperty(
        name="Distance from Origin",
        default=1.0,
        min=0.1,
        description="The distance from the origin to the nodes on the sphere."
    )
    # The maximum number of iterations to run the electrostatic repulsion algorithm. Increase if nodes are not stabilizing within the default limit.
    iterations: bpy.props.IntProperty(
        name="Iteration Limit",
        default=500,
        min=1,
        description="The maximum number of iterations to run the electrostatic repulsion algorithm."
    )
    # A threshold for the mean variation in max force over the last 100 iterations. A smaller value requires tighter convergence.
    convergence_threshold: bpy.props.FloatProperty(
        name="Convergence Threshold",
        default=0.005,
        min=0,
        max=1,
        description="A threshold for the mean variation in max force over the last 100 iterations."
    )

    # The size or radius of each node on the sphere. Adjust for visual clarity and spacing between nodes.
    sphere_size: bpy.props.FloatProperty(
        name="Node Girth",
        default=0.02,
        min=0.01,
        description="The size or radius of each node on the sphere."
    )

    # Toggle to print the coordinates of each node after stabilization. Useful for debugging and manual integration into other applications.
    print_coords: bpy.props.BoolProperty(
        name="Print Coords",
        default=False,
        description="Toggle to print the coordinates of each node after stabilization."
    )

    # Ensure this matches or is close to the 'Distance from Origin' property if using 'Print Coords'
    radius_print: bpy.props.FloatProperty(
        name="Printed Sphere Size",
        default=1.0,
        min=1.0,
        description="Set the distance from the origin for which the coordinates of the nodes will be printed."
    )

class OBJECT_PT_electrical_repulsion(bpy.types.Panel):
    bl_label = "Electrical Repulsion"
    bl_idname = "OBJECT_PT_electrical_repulsion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        props = context.scene.electrical_repulsion_props
        
        layout.prop(props, "num_points")
        layout.prop(props, "radius")
        layout.prop(props, "iterations")
        layout.prop(props, "convergence_threshold")
        layout.prop(props, "sphere_size")
        layout.prop(props, "print_coords")
        
        # If checkbox is checked, display the sub-panel
        if props.print_coords:
            layout.label(text="Coordinate Details:")
            layout.prop(props, "radius_print")

        # The button
        layout.operator("wm.electrical_repulsion_operator")

class WM_OT_ElectricalRepulsionOperator(bpy.types.Operator):
    bl_idname = "wm.electrical_repulsion_operator"
    bl_label = "Apply Repulsion"

    def execute(self, context):
        props = context.scene.electrical_repulsion_props
        num_points = props.num_points
        radius = props.radius
        iterations = props.iterations
        convergence_threshold = props.convergence_threshold
        sphere_size = props.sphere_size
        print_it = props.print_coords
        radius_print = props.radius_print if print_it else radius

        bpy.context.scene.frame_current = 1  # rewind to first frame
        points = np.array([random_point_on_sphere(radius) for _ in range(num_points)])
        spheres = create_spheres(points, sphere_size)

        # Run the repulsion with animation
        final_points = electrostatic_repulsion(points, spheres, radius, iterations=iterations, convergence_threshold=convergence_threshold)
        
        if print_it:
            print_coords = print_points(final_points, spheres, radius_print)
            print_coords_str = str(print_coords)
 
            if "GeneratedCoords" in bpy.data.texts:
                bpy.data.texts["GeneratedCoords"].clear()
                bpy.data.texts["GeneratedCoords"].write("The Coordinates (again):\n")
                bpy.data.texts["GeneratedCoords"].write(print_coords_str)
                bpy.data.texts["GeneratedCoords"].write("\n\nTip Jar: IBAN: LT34 3250 0824 5093 4149\n")
            else:
                bpy.data.texts.new("GeneratedCoords")
                bpy.data.texts["GeneratedCoords"].write("The Coordinates:\n")
                bpy.data.texts["GeneratedCoords"].write(print_coords_str)
                bpy.data.texts["GeneratedCoords"].write("\n\nTip Jar: paypal.me/twinpictures\n")

            # Automatically set this text block to be active in the Text Editor
            for area in bpy.context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    break
            area.spaces[0].text = bpy.data.texts["GeneratedCoords"]

            self.report({'INFO'}, "Coords have been written to the Text Editor!")

        else:
            self.report({'INFO'}, "Electrostatic Repulsion Applied!")
        
        return {'FINISHED'}

classes = [ElectricalRepulsionProperties, OBJECT_PT_electrical_repulsion, WM_OT_ElectricalRepulsionOperator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.electrical_repulsion_props = bpy.props.PointerProperty(type=ElectricalRepulsionProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.electrical_repulsion_props

if __name__ == "__main__":
    register()
