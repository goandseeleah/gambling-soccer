# gambling-soccer
DS-GA-1003 project

## Some problems observed from logistic prediction
* Draw games are seldom predicted correctly (almost 100 percent wrong)
* Model seldom predicts a outcome to be draw
* Beta feature rectify one game prediction to be correct, reason?

## Next inspection step
* Consider the teams occupied in each wrong prediction

## Idea
* Add player information, e.g. which players have played in a given game, might use embedding roster (like CBOW)
* for nonlinear model, just use a bit value to label teams is fine
