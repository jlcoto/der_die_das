
## Der, die, das game

This games offer a simple interface with which to test your der, die das skills.


## Requirements

The game uses the following libraries:

- `numpy`
- `pandas`
- `matplotlib` 
- `jinja2` and `weasyprint` for pdf report.

## Description 

I have provided two ways of playing the game. The most interactive one is with the IPython notebook. You can also play it directly with the python scripts. `noun_game.py` implements the testing, It also offers the possibility of reporting once the game is completed. 

I scraped the list I am using from [here](http://www.byki.com/lists/german/greg%27s-german-nouns-part-1.html). Still, there is some work to do, modifying spelling and, perhaps taking out some non-sense vocabulary there. Feel free to personalize your own list or make modifications. For that you can use the `final_data.csv`. Your entries only need to match the given format.

### Track your progress

The most interesting part for learners is the possibility of tracking your progress. I added the possibility of reporting once the testing is done. This possibility is only available when running `noun_game.py`, not for `IPython Notebook`.  The pdf report looks like this:

![der_die_das report](https://cloud.githubusercontent.com/assets/7328852/16083475/5aaa4954-3315-11e6-8fb1-57a612f22301.png)

### To do

There are still several ways in which this project can me extended. Those that come to mind are:

- Correct printing function. --> Urgent
- Extend / Improve current word list.
- Offer a report with current progress after program is run (this could be a pdf report, e.g.)

In the long term, I want to work in some kind of recommendation system that will give users a proper balance of words that they should learn in order to maximize recall of genders. --> Long term project.


