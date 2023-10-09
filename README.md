
## Blender Script: Electrostatic Repulsion

**A Blender Add-on for evenly distributing nodes on a sphere using Electrostatic Repulsion.**
![demo](ep_sim.gif)
### Installation & Usage:

1. **Install the Add-on**:
   - Download the `electrical_repulsion_addon.py` script.
   - Open Blender.
   - Go to Edit > Preferences > Add-ons > Install, and select the downloaded script.
   - Enable the add-on by checking the checkbox next to "Electrostatic Repulsion".

2. **Configure and Run the Add-on**:
   - Once the add-on is activated, navigate to the 3D Viewport. The panel for the add-on can be found under `View3D > Tool Shelf > Tool`.
   - Adjust the parameters as needed.
   - Run the add-on to start the electrostatic repulsion simulation.

3. **Configure the Simulation**:
   - Adjust the following parameters in the add-on panel:

     | Parameter                 | Description |
     |---------------------------|-------------|
     | Number of Nodes           | The total number of nodes to distribute on the sphere. More nodes may require more iterations for a stable configuration. |
     | Distance from Origin      | The distance from the origin to the nodes on the sphere. A larger radius may affect the time to reach equilibrium. |
     | Initial Position          | Select the method to be used for initial point distribution. |
     | Iteration Limit           | The maximum number of iterations to run the electrostatic repulsion algorithm. Increase if nodes are not stabilizing within the default limit. |
     | Convergence Threshold     | A threshold for the mean variation in max force over the last 100 iterations. A smaller value requires tighter convergence. |
     | Node Girth                | The size or radius of each node on the sphere. Adjust for visual clarity and spacing between nodes. |
     | Print Coords              | Toggle to print the coordinates of each node after stabilization. Useful for debugging and manual integration into other applications. |
     | Printed Sphere Size       | Set the distance from the origin for which the coordinates of the nodes will be printed. Ensure this matches or is close to the 'Distance from Origin' property if using 'Print Coords'. |

4. **Run the Simulation**:
   - The add-on will generate nodes around the origin at the specified distance.
   - The nodes undergo an electrostatic repulsion simulation until equilibrium is achieved.
   - Each loop updates the node locations, saving their positions as a keyframe and advancing the timeline with each iteration.
   - If you chose to print the coordinates:
     - The final locations will be output to the Text Window in Blender.
     - To view the generated coordinates, navigate to the Text Editor area in Blender and select "GeneratedCoords" from the list of text blocks.

### Future Improvements (TODO):
- Toggle the button label from 'Apply Repulsion' to 'Abort Repulsion' while the script is processing, providing clearer user feedback.
- Modify the function to allow the user to manually abort the process when 'Abort Repulsion' is clicked, adding more user control during execution.
- Display a progress indicator or bar while the function is processing, giving users a real-time update on the simulation's progress.
- Enhance the add-on with a user-friendly UI panel for parameter configuration.

### Other Methods to Place n Nodes on a Sphere

#### 1. Random Distribution
- **Brief:** Simple random placement using azimuthal and polar angles.
- **Description:** Nodes are placed using random azimuthal and polar angles. This method is simple but can lead to clustering and uneven distribution.
- **Mathematical Description:** Nodes are placed using random azimuthal ( $\phi$ ) and polar ( $\theta$ ) angles:

 $\theta = 2 \pi \times \text{random number between 0 and 1}$
 $\phi = \arccos(2 \times \text{random number between -1 and 1} - 1)$

#### 2. Fibonacci Lattice (Golden Spiral)
- **Brief:** Uniform distribution using the golden ratio.
- **Description:** The Fibonacci Lattice method generates points on a sphere based on the properties of the Fibonacci sequence and the golden ratio. This method aims to distribute points approximately uniformly across the surface of the sphere.
- **Mathematical Description:**
1. **Golden Ratio**:
    - The golden ratio, often denoted as $\phi$, is calculated as:
   $$\phi = \frac{1 + \sqrt{5}}{2}$$

2. **Spherical Coordinates Calculation**:
    - For each point `i` from 0 to $N-1$ (where $N$ is the number of points):
        - Inclination Angle $\theta$:
       $$\theta = \arccos\left(1 - 2 \times \frac{i + 0.5}{N}\right)$$
        - Azimuthal Angle $\phi$:
       $$\phi = 2\pi \times \frac{i}{\text{golden ratio}}$$

3. **Conversion to Cartesian Coordinates**:
    - The spherical coordinates are converted to Cartesian coordinates using the following transformations:
        - X-coordinate:
       $$x = \text{radius} \times \sin(\theta) \times \cos(\phi)$$
        - Y-coordinate:
       $$y = \text{radius} \times \sin(\theta) \times \sin(\phi)$$
        - Z-coordinate:
       $$z = \text{radius} \times \cos(\theta)$$

The final output is a set of Cartesian coordinates (x, y, z) representing points on the sphere with the desired radius.
- **Code Example**
```python
import numpy as np

def fibonacci_lattice_on_sphere(radius, num_points):
    """
    Generate points on a sphere using a Fibonacci lattice.

    Parameters:
    - radius: The desired radius of the sphere on which points will be generated.
    - num_points: The number of points to generate on the sphere.

    Returns:
    - A list of tuples containing the Cartesian coordinates of the generated points on the sphere of the given radius.
    """
    
    # The golden ratio, often denoted as φ, is a mathematical constant that appears in various fields, 
    # including art, architecture, and nature. In this context, it helps in achieving an approximately 
    # uniform distribution of points on the sphere.
    golden_ratio = (1 + 5 ** 0.5) / 2  # Golden Ratio
    
    points = []

    # Loop through the number of points to be generated
    for i in range(num_points):
        # Calculate the inclination angle (theta) for the current point. This angle represents the 
        # angle between the positive z-axis and the line connecting the origin to the point. The formula 
        # ensures that the points are distributed uniformly from the top to the bottom of the sphere.
        theta = np.arccos(1 - 2 * (i + 0.5) / num_points)
        
        # Calculate the azimuthal angle (phi) for the current point. This angle represents the angle 
        # between the positive x-axis and the projection of the point onto the xy-plane. The use of 
        # the golden ratio ensures that points are spaced out uniformly in the horizontal direction.
        phi = 2 * np.pi * i / golden_ratio
        
        # Convert the spherical coordinates (theta, phi) to Cartesian coordinates (x, y, z) using 
        # standard spherical to Cartesian transformations. These formulas place the point on a unit 
        # sphere and then scale it outwards by the desired radius.
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        
        # Append the calculated Cartesian coordinates to the points list
        points.append((x, y, z))

    # Return the list of generated points on the sphere
    return points
```
#### 3. Regular Polyhedra
- **Brief:** Uses vertices of regular shapes like cubes or tetrahedra.
- **Description:** Uses the vertices of regular polyhedra (e.g., tetrahedron, cube, icosahedron) as node positions. This approach provides a uniform initial distribution for a small number of points.
- **Mathematical Description:** Nodes are placed at the vertices of regular polyhedra. The mathematical description varies based on the chosen polyhedron.

#### 4. T-designs
- **Brief:** Mathematical designs for uniformity.
- **Description:** Mathematical designs that guarantee certain uniformity levels. They can be hard to construct but offer very uniform distributions.
- **Mathematical Description:** T-designs guarantee that any set of$T$ points is in roughly the same configuration as any other set of$T$ points on the sphere. The exact mathematical formulation depends on the chosen T-design.

#### 5. Iterative Refinement
- **Brief:** Refines initial placements through iterations.
- **Description:** Starts with a basic distribution (e.g., random) and refines node positions iteratively. Nodes are moved to reduce system energy, such as electrostatic repulsion.
- **Mathematical Description:** The method starts with an initial distribution and iteratively moves the points based on a chosen energy function (e.g., electrostatic repulsion). The mathematical details depend on the specific energy function and refinement criteria.

#### 6. Spherical Cap Packing
- **Brief:** Packs spherical caps uniformly.
- **Description:** Packs spherical caps of a certain size on the sphere. This method is complex but can offer uniform distributions for specific node counts.
- **Mathematical Description:** Nodes are placed based on the packing of spherical caps on the sphere. The exact mathematical formulation depends on the size and arrangement of the caps.

#### 7. HEALPix Grid
- **Brief:** Divides sphere into equal-area pixels.
- **Description:** Divides the sphere into equal-area pixels. This method is commonly used in astrophysics, and nodes can be placed at pixel centers.
- **Mathematical Description:** The HEALPix method divides the sphere into equal-area pixels. The mathematical formulation is complex and involves hierarchical equal area isolatitude pixelization.

#### 8. Equidistant Archimedean Spiral
- **Brief:** Projects an Archimedean spiral onto the sphere.
- **Description:** Uses the Archimedean spiral properties in the plane and projects them onto the sphere. This approach provides a fairly uniform initial distribution.
- **Mathematical Description:**
1. **Theta Calculation**:
    - The spiral is defined by the angle $\theta$, which varies linearly from 0 to a maximum value, $`\text{max\_theta}`$.
    - The $`\text{max\_theta}`$ value is determined based on the desired number of points, $N$, and can be adjusted to ensure the spiral wraps around the sphere sufficiently:
   $`\text{max\_theta} = \sqrt{N} \times \pi`$
    
2. **Radius Calculation**:
    - For each value of $\theta$, a corresponding radius $r$ is computed in polar coordinates:
   $$r = \theta$$

3. **Spherical Coordinates**:
    - Convert the polar radius $r$ and angle $\theta$ to spherical coordinates (R, $\alpha$, Z):
        - Z-coordinate (height on the sphere):
       $`Z = \text{radius} \times \left(1 - \frac{r}{\text{max\_theta}} \times 2\right)`$
        - R-coordinate (distance from the center of the sphere to a point on its surface at a given height Z):
       $$R = \sqrt{\text{radius}^2 - Z^2}$$
        - $\alpha$ is the azimuthal angle and is reused from the $\theta$ value.

4. **Cartesian Coordinates**:
    - Convert the spherical coordinates to Cartesian coordinates:
        - X-coordinate:
       $$X = R \times \cos(\alpha)$$
        - Y-coordinate:
       $$Y = R \times \sin(\alpha)$$
    - The Z-coordinate remains the same from the spherical coordinates.

The final output is a set of Cartesian coordinates (X, Y, Z) representing points on the sphere with the desired radius.

- **Code Example**
```python
import numpy as np

def archimedes_points_on_sphere(radius, num_points):
    """
    Generate points on a sphere using an Archimedean spiral.

    Parameters:
    - radius: The desired radius of the sphere on which points will be generated.
    - num_points: The number of points to generate on the sphere.

    Returns:
    - A list of tuples containing the Cartesian coordinates of the generated points on the sphere of the given radius.
    """
    
    # Maximum theta value determines the extent of the spiral.
    # This value is based on the number of points and can be adjusted to ensure the spiral wraps around the sphere sufficiently.
    max_theta = np.sqrt(num_points) * np.pi
    
    # Generate theta values linearly from 0 to max_theta.
    # This ensures that the points are spaced evenly along the spiral.
    thetas = np.linspace(0, max_theta, num_points)
    
    points = []

    for theta in thetas:
        # Use the simplified Archimedean Spiral equation.
        # This produces a linear spiral in polar coordinates.
        r = theta
        
        # Convert r and theta to spherical coordinates.
        # Z is calculated linearly based on the current theta value, ensuring that the points span the height of the sphere.
        Z = radius * (1 - (r / max_theta) * 2)
        
        # R is the distance from the center of the sphere to a point on its surface at a given height Z.
        R = np.sqrt(radius**2 - Z**2)
        
        # Reuse the theta value for the azimuthal angle, alpha.
        # This makes the points spiral around the Z-axis.
        alpha = theta
        
        # Convert the polar coordinates (R, alpha) to Cartesian coordinates (X, Y) in the XY plane.
        X = R * np.cos(alpha)
        Y = R * np.sin(alpha)
        
        # Append the Cartesian coordinates to the points list.
        points.append((X, Y, Z))
    
    return points
```

#### 9. Kogan's Spiral Method (2017)
- **Brief:** Uses a special spiral for efficient placements.
- **Description:** A computationally efficient method introduced by Jonathan Kogan in 2017. It uses a spiral determined through experimental evidence. The method achieves spacings close to theoretical bounds and is especially efficient for a large number of nodes.
- **Mathematical Description:** The exact mathematical formulation is based on the special spiral introduced by [Jonathan Kogan in his 2017 paper](https://scholar.rose-hulman.edu/cgi/viewcontent.cgi?article=1387&context=rhumj). The provided Python code gives a glimpse into the method's implementation.
- **Code Example**
```python
import math

def spherical_coordinate(x, y):
    """
    Convert given angles to spherical coordinates.
    
    Args:
    - x (float): First angle.
    - y (float): Second angle.
    
    Returns:
    - list: A list containing the 3D coordinates.
    """
    return [
        math.cos(x) * math.cos(y),
        math.sin(x) * math.cos(y),
        math.sin(y)
    ]

def NX(n, x):
    """
    Generate n points based on the method described in Kogan's paper.
    
    Args:
    - n (int): The number of points.
    - x (float): A parameter used in calculating the coordinates.
    
    Returns:
    - list: A list of 3D points.
    """
    pts = []
    
    # Calculate the starting value and increment based on n
    start = (-1. + 1. / (n - 1.))
    increment = (2. - 2. / (n - 1.)) / (n - 1.)
    
    for j in range(n):
        s = start + j * increment
        # Calculate the spherical coordinates for each point
        pts.append(
            spherical_coordinate(
                s * x, 
                math.pi / 2. * math.copysign(1, s) * (1. - math.sqrt(1. - abs(s)))
            )
        )
    return pts

def kogan_sphere_points(samples, radius=1.0):
    """
    Generate points on a sphere using Kogan's method.
    
    Args:
    - samples (int): The number of points.
    - radius (float, optional): The radius of the sphere. Defaults to 1.0.
    
    Returns:
    - list: A list of 3D points on the sphere.
    """
    pts_3D = NX(samples, 0.1 + 1.2 * samples)
    
    # Scale the points by the given radius
    points = [(pt[0] * radius, pt[1] * radius, pt[2] * radius) for pt in pts_3D]
    
    return points
```
#### 10. The Golden Spiral Phyllotaxis
- **Brief:** Distribution method inspired by patterns found in nature.
- **Description:** The Golden Spiral Phyllotaxis method is a way of distributing points evenly over the surface of a sphere. This method is inspired by patterns found in nature, such as the arrangement of seeds on a sunflower head or the scales of a pinecone. The idea is to use the golden ratio to distribute points evenly on a sphere. This method is often preferred over random distribution or other deterministic methods because it tends to provide an even distribution without visible clusters or gaps.

The key property of the golden ratio is that it is "the most irrational number," meaning it provides the best resistance to forming simple fraction approximations. This property helps in avoiding clusters and gaps when distributing points on a sphere.
- **Mathematical Description:**
##### 1. The Golden Angle:
The Golden Angle ( $\phi$ ) is based on the Golden Ratio ( $\Phi$ ), which is approximately $1.61803398875$. The Golden Angle is given by:

$$\phi = 2\pi(1 - \frac{1}{\Phi}) = 2\pi(1 - \frac{1}{1.61803398875})$$

##### 2. Point Placement:
For each point$i$ (starting from $i = 0$ to $n-1$, where $n$ is the total number of points, in this case, 80), the height ( $y_i$ ) and the radius in the xy-plane ( $r_i$ ) are calculated as:

$$y_i = 1 - \frac{i}{n} - \frac{1}{2n}$$
$$r_i = \sqrt{1 - y_i^2}$$

##### 3. Angle Calculation:
The angle for each point is given by:

$$\theta_i = \phi \times i$$

##### 4. Cartesian Coordinates:
Finally, we can convert the cylindrical coordinates ( $r_i, \theta_i, y_i$ ) to Cartesian coordinates:

$$x_i = \cos(\theta_i) \times r_i$$
$$y_i = \sin(\theta_i) \times r_i$$
$$z_i = y_i$$
- **Code Example**
```python
import numpy as np

def phyllotaxis_points_on_sphere(radius, num_points):
    """
    Calculate points on a sphere using the Golden Spiral Phyllotaxis method.
    
    Parameters:
    - radius: Radius of the sphere.
    - num_points: Number of points to be placed on the sphere.
    
    Returns:
    - An array of shape (num_points, 3) containing the x, y, z coordinates of the points.
    """
    
    # Golden ratio
    Phi = (1 + np.sqrt(5)) / 2
    # Golden angle
    phi = 2 * np.pi * (1 - 1/Phi)
    
    # Calculate the coordinates
    theta = phi * np.arange(num_points)
    y = 1 - 2 * (np.arange(num_points) / (num_points - 1))
    r = np.sqrt(1 - y*y)
    
    points = []
    for i in range(num_points):
        x_i = np.cos(theta[i]) * r[i] * radius
        y_i = y[i] * radius
        z_i = np.sin(theta[i]) * r[i] * radius
        points.append((x_i, y_i, z_i))

    return points
´´´
#### 11. Voronoi Relaxation (Spherical Lloyd's Algorithm)
- **Brief:** Voronoi-based iterative refinement.
- **Description:** Starts with a random or structured distribution of nodes on the sphere. A Voronoi diagram is computed for these nodes on the spherical surface, and each node is moved to the centroid of its Voronoi cell. The process is repeated until convergence. This results in a distribution that minimizes the variance of distances between nodes, leading to a more uniform distribution.
- **Mathematical Description:** Nodes are placed based on the Voronoi diagram computed on the spherical surface. Each node is then moved to the centroid of its Voronoi cell. The mathematical details involve the computation of the Voronoi diagram and centroids on the sphere.

- **Voronoi Diagram:** Given a set of seed points, the Voronoi diagram divides the space such that every point in a specific partition is closer to its corresponding seed point than to any other seed point. When applied to a sphere, you get spherical Voronoi cells, each defined by a seed point, and each point on the sphere's surface belongs to the cell of the nearest seed point.

- **Voronoi Relaxation** (Spherical Lloyd's Algorithm): This is an iterative process to optimize the distribution of points on a surface (like a sphere). The steps are as follows:

Start with an initial set of points on the sphere.
Compute the Voronoi diagram for these points on the sphere.
For each Voronoi cell, compute its centroid (or the center of mass).
Move the original point (seed) to the centroid of its Voronoi cell.
Repeat the above steps until convergence (i.e., when the points don't move much between iterations or after a set number of iterations).
This relaxation process spreads the points more uniformly across the sphere, making it a popular method for distributing points on surfaces.

So, while the Voronoi diagram is a method to partition space based on a set of seed points, Voronoi Relaxation (or Spherical Lloyd's Algorithm) is a method that uses the Voronoi diagram iteratively to achieve a more uniform distribution of points.

### Voronoi Relaxation vs Electrical Repulsion 
#### Voronoi Relaxation (Spherical Lloyd's Algorithm):
- **Principle:** Improve point distribution by adjusting points towards the centroids of their Voronoi cells.
- **Mechanism:** In each iteration, the Voronoi diagram is computed based on the current points, and then each point is moved to the centroid of its corresponding Voronoi cell.
Convergence: The process is repeated until the points move minimally between iterations or until a certain number of iterations are reached.

#### Electrical Repulsion:
- **Principle:** Treat each point as a charged particle that repels other points, leading to a more uniform distribution.
- **Mechanism:** In each iteration, for every pair of points, a repulsive force is computed based on their distance (like charged particles repelling each other). Points are then moved based on the resultant forces from all other points.
Convergence: The process is repeated until the resultant forces on the points are below a certain threshold or until a specific number of iterations are reached.

### Comparison: Golden Spiral Phyllotaxis vs. Fibonacci Lattice

1. **Formula for $\theta$ (or $\alpha$)**:
    - **Golden Spiral Phyllotaxis**: 
        - The angle $\alpha$ (or $\theta$ in some descriptions) is determined using the golden ratio:
       $`\alpha = \text{golden\_ratio} \times 2\pi \times \text{counter}`$
    - **Fibonacci Lattice**: 
        - The angle $\theta$ between successive points in the horizontal plane is a constant increment:
       $`\Delta \theta = 2\pi \times \text{golden\_ratio}^{-1}`$

2. **Z Coordinate Calculation**:
    - **Golden Spiral Phyllotaxis**: 
        - The z-coordinate is a simple linear mapping based on the counter:
       $`Z = \frac{2 \times \text{counter}}{N}`$
    - **Fibonacci Lattice**: 
        - The z-coordinate is determined by incrementally moving up the sphere, typically using a fixed vertical step.

3. **Interpretation**:
    - **Golden Spiral Phyllotaxis**: 
        - This method is often visualized as points arranged in a spiral pattern, similar to the arrangement of seeds in sunflowers.
    - **Fibonacci Lattice**: 
        - This method can be visualized as layers of points arranged in spirals, where each layer is a horizontal slice of the sphere. The points in each layer are offset from the layer below, preventing vertical alignment and ensuring better distribution.


In essence, while both methods utilize the properties of the golden ratio to evenly distribute points on a sphere, their specific approaches and resulting patterns can be different. However, in practice, both methods yield very similar distributions, and the differences are often subtle. The choice between them usually depends on the specific application or personal preference.