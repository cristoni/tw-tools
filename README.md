# tw-tools

## Bunkers Calculator
This tool calculate the level of danger of each allied village based on it's position in relation to enemy villages.

To use it you must first create a .env file in it's folder copying the .env.example, and change it to something like this:
```
SERVER=tribalwars.net
WORLD=en133
OUR_TRIBE=AFK
ENEMY_TRIBE=Indian
```

Once that's done, you just have to run it.
```
py .\bunkers-calculator\main.p
```
It will download the list of tribes, players and villages and start computing.

The output is something like:
```
coords  name                  name_player      score
516|555 036                   Luke+and+Luke    1454.676155
512|543 0041+Heads+on+a+spike Kreiz            1452.548020
514|538 0034+Heads+on+a+spike Kreiz            1451.263846
509|541 0037+Heads+on+a+spike Kreiz            1449.596390
516|533 0033+Heads+on+a+spike Kreiz            1449.139247
510|543 0040+Heads+on+a+spike Kreiz            1444.347793
510|540 0036+Heads+on+a+spike Kreiz            1440.041251
511|522 SAND+CASTLES%21       Vamler           1435.266289
498|521 SAND+CASTLES%21       Vamler           1432.576987
508|544 0042+Heads+on+a+spike Kreiz            1426.455409
492|516 0058                  YellowFlash      1418.129938
```

### Scoring function
The score is calculated like this:
The script make a cartesian product of allied villages with enemy villages and for each association make this calculations:
- normalized distance
- normalized enemy village points
- normalized allied village points
- normalized enemy player points

Then the score formula is composed by those 4 values with different weights:
- 50% nearness (1-distance): half the score depends on how close are the two villages
- 25% enemy village points
- 15% allied village points: we take the allied village points into consideration, even if not with a big weight. This way if the village is a newly taken barb it has low priority unless it's in a very key position
- 10% player points: this is the less important value, but nonetheless we take it into consideration

After assigning a score for each allied village in relation to each enemy village we aggregate by allied village e sum the scores.