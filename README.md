# Sandbox-Caterpillar-Challenge
## This is my solution to the 2026 Spring Semester Sandbox Caterpillar Challenge

This challenge instructed us to manipulate existing data to create a list of participant statistics for all participants in an app called 'Flow in the Field.' 

When approaching my solution, I first outlined the structure of the data given and the end goal. By outlining the end goal, I started to build my main function by first creating a dictionary of participant stats for each participant, which I then worked to fill with manipulated data that was sorted by sessions, language, and rounds. For any blocks of code that I anticipated to logically overlap (ex. average duration for a round vs. session, getting sessions based on a language, etc.) I created helper functions to make my code easier to read, write, and reuse for different purposes. Along the way, I made sure to test my functions with the test data given in the challenege description. 

The primary technical challenge I ran into was in using the 'filter()' function. I wanted to use this since I knew it would be the easiest way to get sessions or rounds of a specific participant or language. However, I did not realize that filter returned a filter object instead of the original data (ex. a session dictionary), which resulted in errors in which I had to convert my filter functions to list objects. Through this, I also learned how to use the 'next()' function when I knew there was only one object to return (ex. a round dictionary from a specific session). 

This solution was created in Python 3 through VS Code. The steps to running the solution are as follows:
1. Clone this repo
2. Install 'requests' library within your virtual environment (type 'pip3 install requests' in terminal)
3. Run the code through an IDE, such as VS Code.

This project took me approximately 5 hours to complete.

