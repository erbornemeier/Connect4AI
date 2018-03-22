Easton Bornemeier - 10690015

Prog Lang used:
Python 2.7

OS used:
Tested on Linux and Windows systems

Structure: 
The maxConnect4.py houses the argument parsing and the upper level 
game state handling, while Connect4Game.py deals with the AI decisions, 
board scoring and printing, and writing to file.

Methods:
The code currently implements the minimax alpha-beta pruning on the AI player.
Depth is reasonable to play with at values less than or equal to 10. The AI
typically beats random players consistantly at a depth of 3 or 4

How to run the code:
1. Obtain Python2 if needed
2. Open a terminal window (Powershell/GitBash for Windows)
3. Navigate to where the maxConnect4.py and Connect4Game.py files are stored
4. Run the command "python maxConnect4.py interactive [input_file] [computer-next/human-next] [depth]" for interactive mode with optional input file and dynamic depth 
or "python maxConnect4.py one-move [input_file] [output_file] [depth]" for one-move mode with required input and output files and dynamic depth

Example executions:
python maxConnect4.py interactive no-input human-next 8
python maxConnect4.py one-move testInput.txt testOutput.txt 6
