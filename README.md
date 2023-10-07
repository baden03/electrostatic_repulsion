
## Blender Script: Electrostatic Repulsion

**A Blender Add-on for evenly distributing nodes on a sphere using Electrostatic Repulsion.**

### Installation & Usage:

1. **Launch Blender from the Command Line**:
   - For Mac users:
     ```bash
     /Applications/Blender.app/Contents/MacOS/Blender
     ```

2. **Load the Script into Blender**:
   - Open a Text window in Blender.
   - Choose Text > Open.
   - Select the `electrical_repulsion.py` file.

3. **Run the Script**:
   - In the Text window, select Text > Run Script.

4. **Configure the Simulation**:
   - Provide the following parameters in the command console:

     | Parameter | Description |
     |-----------|-------------|
     | Number of Nodes | Define how many nodes you'd like placed on the sphere. |
     | Distance from Origin for Calculation | Specify how many units away from the origin the nodes should be positioned for calculations. |
     | Print Final Coordinates | Choose 0 for 'No' or 1 for 'Yes'. If 'Yes', the final array of node coordinates will be printed to the command console. |
     | Distance from Origin for Coordinates | If you've opted to print the final coordinates, define the desired unit distance from the origin for each coordinate. |

5. **Run the Simulation**:
   - The script will generate nodes around the origin at the specified distance.
   - It undergoes an electrostatic repulsion simulation until equilibrium is achieved.
   - Each loop updates the node locations, saving their positions as a keyframe and advancing the timeline with each iteration.
   - If you chose to print the coordinates, the final locations will be output to the command console.

### Future Improvements (TODO):
- Add user input for iteration limit.
- Allow customization of the `max_force_magnitude` used to determine equilibrium.
- Provide user control over sphere size.
- Enhance the script to become a full-fledged Blender Add-on, complete with a user-friendly UI panel.
