# Kabufuda Solitare Bot
A bot made to speedrun Kabufuda Solitare from Last Call BBS

## How to Use
### Prerequisites
1. [Python 3.9](https://www.python.org/downloads/release/python-390/) (Other Python versions should also work)
2. Copy of Last Call BBS

### Setup
1. Clone or download this source code
2. Install requirements
   * From the command line, cd into the source code folder, then run `pip install -r requirements.txt`
3. Configure the following settings in Last Call BBS
   * Resulution 1920x1080 (Fullscreen or windowed are both fine)
   * Screen Effect Disabled
   * Pixel Scaling Perfect

### Run
1. Install and launch Kabufuda Solitare
2. Make sure the in-game window is entirely visible
3. Run main.py through the GUI of your choice, or through the command line by changing directory into the project folder and running `python main.py`
4. The bot will wait for 5 seconds. In that time, click in the game window to focus on it
5. Enjoy!

Note that this bot is not capable of solving all expert puzzles. I don't know whether this is due to some of the shortcuts I took when writing the code to solve the game, or whether some puzzles are truly impossible. If you'd like to investigate, there are screenshots of puzzles the game thinks are impossible in the images folder. If the bot can't solve a puzzle, it will automatically start a new one.
