# Low-Poly Plant Maker Addon (Blender 2.83)

This is an addon for Blender 2.83 desgined to quickly make stem-based plants that can be applied to curves made with a hair particle system. As this is my first foray into Blender scripting the code is a bit messy and makes a lot of assumptions about the workflow being used (explained down below). If you would like to make some edits to the script to make it a bit cleaner or more universal, feel free to submit a pull request or reach out to me here or on Twitter @wormsnacks with any code organization questions!

## Workflow
A number of these assumptions are baked into the code, and so deviating from them might cause issues while using the addon

1. Install the addon zip file into your Blender Addons
2. To begin, make a stem using Object Add > Mesh > Plant Maker Stem, it will be at the bottom of the menu where you would add in a new mesh primitive normally
