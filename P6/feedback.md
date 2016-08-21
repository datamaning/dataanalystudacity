### P6: Make Effective Data Visualization


#### Versioning details:

#### 0.1

* added live search bar
* added shoe info box with image
* added scatterplot with shoe size as y-axis and price as x-axis
* added clickable legend
* added clickability to scatterplot dots

#### 0.2

* changed live search results to a smaller font
* added new and used median price for query results
* added button to search for another shoe
* added brief descriptions 
* added ebay item box with full details
* improved responsiveness and overall aesthetics
* added responsiveness to scatterplot
* fixed issue where dots lose clickability when redrawn with legend filtering
* fixed issue where chosen dot loses styling when redrawn with legend filtering
* moved legend from top right to top left and lowered scatterplot

#### 0.3

* text changed for second set of instructions
* set fixed viewport height to scatterplot
* added loading bar
* added average price by size as barplot

#### Summary:

##### Phil:
> Find Jordan shoes and see quickly what sizes are available and what prices they are selling for

##### Serena
> find specific shoes with specific qualification in both used and new shoe market and the opportunity to buy and sell.

##### Chris
> Find air jordan shoes and quickly understand current market conditions by scatter plot of size by price

#### Versioning feedback:

##### 0.1

##### Phil:
* The search bar is awesome, maybe make the results smaller they are hard to read when they wrap up, especially on mobile
* Is there a way to give some price summaries?
* The plot gets cut off when you resize the size of the window
* The legend and the plot also overlap when window gets smaller
* The shoe sizes don’t always make sense, could be some euro sizing in there
* Took me a little to figure out that the legends and dots were clickable
* Doesn’t work for every shoe

##### Serena:
* Easy to navigate and overall layout was clear.
* Bug occur when you filter status of the shoe on the right bar “click to show/hide” section. The re-direct link of shoes does not update accordingly once filter has been applied.
* Quantity could be an useful element on data visualization section. Possible presentation could be similar to Graph 1. (see below)
* Personally would prefer to see all re-direct links to be shown (perhaps sorted by price/condition/payment method...ect) when the filter for status of the on the right bar “click to show/hide” section applies. It would save time and efforts for the users.

##### Chris:
* Really like the way search responds in real time, nicely done
* Sometimes it freezes, must be a bug
* The plot captures the basics well, the layout is intuitive. The use of color and the axes is clear, is there a way to convey more by means of size and/or movement?
* I am sure you are aware but it should become responsive
* The selected element loses styling when the legends are clicked. The elements that disappear and reappear become unclickable, might want to check on that.
* Some instructions might help

##### 0.2

##### Phil
* Niiiice, it looks much better now, much more website like
* Good price summary on new and used
* The plot now changes to fit the screen, but legend still overlaps

##### Serena
* Bug was fixed in regards to the links failed to update with new selection issue. 
* For mobile version, suggest to made the instruction of “Click on legend or scatterplot for more, mobile device please double tap” more noticeable. Perhaps split them in two sentences? Double tap isn’t obvious.
* Wonder if all the links for items related to the same size could be shown at the same time for comparison purpose?
* Overall I thought version 0.2 had a huge improvement in visual, website response and user’s experience.

##### Chris
* Good use of responsive design. However, the plot doesn’t display properly on my device (iphone 6)
* The plot can run a bit tall when there are many sizes available, try setting a maximum height
* The selected element maintains style and unclickable bug is fixed, seems to be in working order
* Add a loading bar, the loading time exceeds 5 seconds in some instances. Users might be turned off
* For some high volume shoes the scatters can overplot
* Great job!