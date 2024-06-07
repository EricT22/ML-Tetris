# Overall objective of ML agent

To evaluate all possible actions from the action set to maximize the reward given the current environment state

## ML Keyword definitions for the scope of this problem

### Action Set

Consists of the entire moveset of tetris:

1. Move left
2. Move right
3. Move down
4. Auto-down
5. Rotate right (clockwise)
6. Rotate left (counterclockwise)
7. **Hold piece (not implemented yet)**

### Environment State

Consists of the main board layout, current piece + orientation (and maybe its location on the board), and next piece (maybe, idk the role of the next piece yet)

### Reward

Found by the action value (Q) function

### Q function

Evaluates the action taken in a given state and determines the expected reward

For tetris this evaluation will take in a multitude of factors, including the score obtained by an action, the number of lines cleared by the action, the number of unfilled spots under the piece when its placed (less the better), and the overall shape of the resulting state (don't want it to make a tower)

*might need a neural network for this, making it a deep q model*