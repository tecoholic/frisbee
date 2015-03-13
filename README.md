# Frisbee Player Tracking
=========================

The purpose of this document is to track the frisbee as the game progresses through the hands of the players.

## Player Identification
========================

Each player is represented with a 3 letter identifier, which is usually the first three letters of their name.

For a bigger tournament I think the jersy numbers would be more appropriate.

## Tracking
===========

The frisbee is tracked by writing the identifier followed by a dash(-) and the code of the player who gets the pass.

A [\*] is added right after the player's name if the player has dropped the catch and wasted the pass by making a blind throw.

A [F] is added after the player's name if he has made a **foul** by moving with the frisbee in hand or by man-handling the opposite team's player.

A [S] is added after the player's identifier, if it was a sucessful **snatch** from the opposite team.

A [P] is added after the player's identifier, if the pass has resulted in the scoring of the **point**.


## Economy
==========
*Only considering the offence*

Points are the money. They are earned by passes and spent by drops and fouls.
    * Each sucessful pass results in a positive [+] outcome and each drop results in a [-] outcome.
    * In a pass - the thrower has multiple work like evading the opponents, finding the appropriate team mate and the timing and space to place the frisbee.
    * In a pass - the catcher doesn't have any decision making to do, still involves positioning oneself free of the opponents, and having to deal with opponents when recieving the frisbee.
    * Considering the decision making involved, 2/3rd the credits for a pass is awarded to thrower and 1/3rd of the credit to the catcher.

With the above costs in place:
    * When a thrower throws and the catcher catches (a sucessful pass) - thrower +2/3 and catcher +1/3
    * When a thrower throws to a specific player and the player drops - thrower +2/3 and catcher -1/3
    * When a thrower makes a blind throw without placing it anywhere - thrower -2/3
    * When a blind throw such as above is snatched - snatcher +1
    * When a blind throw is saved - thrower +1/3 and catcher +2/3

## Effectiveness
================

The whole team's effectiveness is decided by the amount of points they have earned in the end.

Each person's effective contribution is calculated by cumulative addition of the cost involved in each action througout the game and equating it to the points.

Sum of work = Points
2/3x+1/3x-2/3x+1x = 1
4/3x = 1
x = 3/4 = 0.75

Now multiplying this effectiveness to each person's work, we get the person's offence contribution.
Person 1 = 2/3 * 0.75
Person 2 = 1/3 * 0.75
Person 3 = -2/3 * 0.75
Person 4 = 1 * 0.75


