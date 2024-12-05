## Overview

**Project Title**: Py_Tetris

**Project Description**: Create a Tetris style game in Python

**Project Goals**: Have a playable Tetris game with background music

## Instructions for Build and Use

Steps to build and/or run the software:

1. import arcade, random, and PIL
2. Set the dimensions of the screen
3. Set the size of each grid square
4. Set the margin size between cells
5. Calculate the screen dimensions and store those in variables
6. Create the color palate dictionary
7. Create the tetris shapes dictionary
8. Create the textures function to make the shapes
9. Write the rotation function to rotate the shapes
10. Write the check_collision function to detect in pieces hit each other
11. Write the remove_row function to move the pieces down the screen
12. Write the join_matrixes function for merging pieces together on collision
13. Write the new_board function to create the grid to play on
14. Create the MyGame class
15. Write the init function to initialize the game
16. Write the new_stone function to randomly grab a new piece and place it at the top of the grid upon collision.
17. Write the setup function to initialize the game state
18. Write the drop function to move the game pieces down
19. Write the rotate_stone function to allow for rotation functionality
20. Write the on_update function to update the game state at regular intervals
21. Write the move function to allow for horizontal move functionality
22. Write the on_key_press function to allow for keyboard playability
23. Write the draw_grid function to create the game board
24. Write the update board function to sync the visual sprites with the logical board state
25. Write the on_draw function to render game visuals
26. Write the main function to start the game loop

Instructions for using the software:

1. Use the command 'py tetris.py' to start the program 
2. Use the left and right arrow keys to move the pieces in those directions
3. Press the up arrow key to rotate the piece counterclockwise
4. Press the down arrow key to move the piece down

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* VSCode

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [ChatGPT](chatgpt.com)
* [Real Python](https://realpython.com/arcade-python-game-framework/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Allow the user to pause the game state
* [ ] When the game ends, allow the user to restart
