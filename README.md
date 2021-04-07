# reversi
A simple ai using MCTS in the classic reversi board game



1.Game Rule:
  
  1.1:Move sequentially,Black tile first
  
  1.2:Each move filps all the tiles stands between your move and your other tile
  
  1.3:Thinking time is limited to 60 seconds
  
  1.4:For each move,you have to flip at least 1 enemy tile,otherwise you can't move,and your enemy moves continously until you can move
  
  1.5:If both sides isn't able to make a move,the game is over



2.Parameters:
  
  2.1:C:A constant which decide the main policy,increase makes the algorithm more likely to try undiscovered nodes,whereas decrease it makes the algorithm more conservative
  
  2.2:Time: A constant limiting the running time of the ai,decrease it if you want to have some fun



Notice:
  The pygame interface of reversi comes from https://github.com/BestOreo/MCTS-AI-Reversi, however,their MCTS algorithm wasn't finished.you can check it out as your will.
