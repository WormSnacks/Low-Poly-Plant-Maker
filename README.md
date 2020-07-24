# Low-Poly Plant Maker Addon (Blender 2.83)

This is an addon for Blender 2.83 desgined to quickly make stem-based plants that can be applied to curves made with a hair particle system. As this is my first foray into Blender scripting the code is a bit messy and makes a lot of assumptions about the workflow being used (explained down below). If you would like to make some edits to the script to make it a bit cleaner or more universal, feel free to submit a pull request or reach out to me here or on Twitter @wormsnacks with any code organization questions!

## Workflow
A number of these assumptions are baked into the code, and so deviating from them might cause issues while using the addon

1. Install the addon zip file into your Blender Addons
2. To begin, make a stem using Object Add > Mesh > Plant Maker Stem, it will be at the bottom of the menu where you would add in a new mesh primitive normally
    * **Do not edit this mesh beyond UVs** this will be the base stem of your plant, editing the the mesh itself (in edit mode) will probably cause a number of issues with stem randomization.
3. Set stem UVs. The addon assumes that you will be using gradient texturing of some kind (more information about low poly gradient texturing [here](https://www.patreon.com/posts/7715616)). The top and bottom ring UVs are the only ones kept on stem randomization, the middle rings will be linear interpolations of the two.
4. Set Plant Maker parameters in the Plant Maker panel. The panel can be found towards the bottom of the Object Properties tab (yellow square on the right).
   * Most settings are self-explanatory. Object parameters point to what will eventually be leaves (placed around sides of stem), flowers (placed at the top), and the hair particle object (which the stem will be copied and curved along). Hitting the "Randomize Stem" button will rerandomize the selected stem according to its current parameters, mess around to see what works! Keep in mind that Leaf and Flower objects will be parented to the Stem object on randomization, and that they are not expected to have children (it kept crashing when I tried adding in recursion, if anyone wants to tackle that they're welcome to).
5. Set up your hair particle object, and link to it in the option in the Plant Maker Panel on the stem
6. Hit "Apply Stem to Particle System" and the stem will be duplicated and applied to the hairs of the particle system (which will be converted to Bezier Curves)
   * Look into how hair systems work to get the shape you'd like! Also be cautious of how many hair particles there are, the number of particles in the system drives how many stems will be duplicated, so changing it from its default 1000 might be a good idea.
7. Play around and see what you can make!

## Tips
1. Make sure to test a single stem with the Randomize Stem button before applying to the hair system a bunch of times!
2. After applying the stem to the hair system, moving the hair system around will reposition all of the duplicated stems without having to reapply them to the hairs, which can be a bit slow!
3. Plants with multiple different types of stems (some with flowers, some without, etc.) can be reproduced with multiple stems and hair systems, just make some variations!
4. Modifiers on the stem object, as long as they aren't applied, should not mess too much with the addon's operation. Play around and see if there are any cool effects to be had!
5. The addon produces a lot of orphaned data, if you find that things are running slow after applying a bunch of stems a bunch of times, try purging orphaned data (it will be ok! Thats all just deleted stuff)

Go ahead and use this in anything you would like! Credit is appreciated but obviously not required.
