I've made a copy of dreidel_game.py called 8-bit_dreidel.py. The new version should keep the same logic/flow in as much as possible, but should use bitmaps exclusively for the graphics.

To aid you with that conversion I've provided 9 images:

Top of screen (135x164):

- images/dreidel/intro.bmp - The "title" intro image feature the game logo and title

- images/dreidel/left.bmp - A blank dreidel lit from the left
- images/dreidel/right.bmp - A blank dreidel lit from the right

You can alternate between left and right at the top of the screen to create a spinning effect.

- images/dreidel/shin.bmp - A dreidel displaying Shin and the caption "(put in)"
- images/dreidel/gimel.bmp - A dreidel displaying Gimel and the caption "(everything)"
- images/dreidel/hey.bmp - A dreidel displaying Hey and the caption "(half)"
- images/dreidel/nun.bmp - A dreidel displaying Nun and the caption "(nothing)"

- Bottom of the screen (135x76):

- images/dreidel/base.bmp - The default base image
- images/dreidel/prompt.bmp) - The base with an additional prompt to "Push to Spin"

You can alternate between base and prompt at the bottom of the screen to create a blinking text effect.

Please use these images to update 8-bit_dreidel.py and convert it into an image-based game.
