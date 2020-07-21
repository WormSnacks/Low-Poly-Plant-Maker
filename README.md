# Low-Poly Plant Maker Addon (Blender 2.83)

This is an addon for Blender 2.83 desgined to quickly make stem-based plants that can be applied to curves made with a hair particle system. As this is my first foray into Blender scripting the code is a bit messy and makes a lot of assumptions about the workflow being used (explained down below). If you would like to make some edits to the script to make it a bit cleaner or more universal, feel free to submit a pull request or reach out to me here or on Twitter @wormsnacks with any code organization questions!

## Workflow
A number of these assumptions are baked into the code, and so deviating from them might cause issues while using the addon

1. Install the addon zip file into your Blender Addons
2. To begin, make a stem using Object Add > Mesh > Plant Maker Stem, it will be at the bottom of the menu where you would add in a new mesh primitive normally
    2. **Do not edit this mesh beyond UVs** this will be the base stem of your plant, editing the the mesh itself (in edit mode) will probably cause a number of issues with stem randomization.
3. Set stem UVs. The addon assumes that you will be using gradient texturing of some kind (more information about low poly gradient texturing [here](https://www.patreon.com/posts/7715616)). The top and bottom ring UVs are the only ones kept on stem randomization, the middle rings will be linear interpolations of the two.
4. Set Plant Maker parameter in the Plant Maker panel. The panel can be found towards the bottom of the Object Properties tab (yellow square on the right).
    4. Most settings are self-explanatory. Object parameters point to what will eventually be leaves (placed around sides of stem), flowers (placed at the top), and the hair particle object (which the stem will be copied and curved along). Hitting the "Randomize Stem" button will rerandomize the selected stem according to its current parameters, mess around to see what works! Keep in mind that Leaf and Flower objects will be parented to the Stem object on randomization.
5. Set up your hair particle object, and link to it in the option in the Plant Maker Panel on the stem
6. Hit "Apply Stem to Particle System" and the stem will be duplicated and applied to the hairs of the particle system (which will be converted to Bezier Curves)
7. Play around and see what you can make!

