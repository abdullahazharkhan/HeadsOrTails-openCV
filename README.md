# HeadsTails - with ComputerVision
A popular hand-gesture-based game known as HeadsTails, built with Python and OpenCV.

### Demo
[HeadsTails.webm](https://github.com/abdullahazharkhan/HeadTail-openCV/assets/109475658/c24edb51-3f1b-4de9-bbac-edc6921312cf)

### How to Play
HeadsTails is played between two players. The game involves choosing between Heads or Tails and then using hand gestures to represent runs, similar to cricket but with hands.

**Wait for the timer to turn 3 to take your move (hand gesture) as an input.**

**Press SPACE to go to the next step.**

#### Start
- At the start of the game, each player chooses either Heads or Tails.
- A toss is conducted to determine the starting player.
#### Toss
- Both players show one hand with a number of fingers extended (between 1 and 5).
- If the sum of both players' fingers is even, the player who chose Tails wins the toss.
- If the sum is odd, the player who chose Heads wins the toss.
- The toss winner decides whether to bat or bowl first.
#### Gameplay
- Both players show hand gestures to represent runs:
- 1 finger = 1 run
- 2 fingers = 2 runs
- 3 fingers = 3 runs
- 4 fingers = 4 runs
- 5 fingers = 5 runs
- Thumb = 6 runs
- No fingers (closed fist) = 10 runs
- If the batter and bowler show the same hand gesture, the batter is out.
#### Switching Roles:
- When a batter is out, the roles switch. The bowler becomes the batter and vice versa.
- The new batter tries to chase the target set by the previous batter.
#### Winning the Game:
- If the new batter successfully completes the target, he wins.
- If the new batter fails to meet the target i.e. gets out, the opponent wins.
