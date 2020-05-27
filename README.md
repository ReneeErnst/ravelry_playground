# Ravelry Playground
A place to play with data from the Ravelry API! 

https://www.ravelry.com/ 

https://www.ravelry.com/api

From the About Us section of the Ravelry site: 

"Ravelry is a place for knitters, crocheters, designers, spinners, weavers 
and dyers to keep track of their yarn, tools, project and pattern information, 
and look to others for ideas and inspiration. The content here is all 
user-driven; we as a community make the site what it is. Ravelry is a great 
place for you to keep notes about your projects, see what other people are 
making, find the perfect pattern and connect with people who love to play 
with yarn from all over the world in our forums."

## Intro
To start this project I've built functionality for pulling data from the 
Ravelry API. As of 5/26/2020, the code in the sweaters_play_data Cauldron 
notebook pulls in the following data (S01 sets up config for the later steps):
- S02-attribute_data: Basic (minimal) data on possible color and yarn 
  attributes that are re-used throughout Ravelry
- S03-sweater_patterns: Pulls all sweater patterns from Ravelry (just 
  over 100k) patterns. This gets a lot of data and pulls it in chunks 
  appropriately. 
- S04-pull_chunks_pattern_details: Pulls the detailed pattern info for all
  pattern ids obtained in S03. This is an even larger amount of data. Data
  is saved in chunks (either locally or to GCS). Provides the level of info
  that should make the modeling ideas below possible, such as number of 
  projects that use the pattern and pattern reviews. 
- S05-save_pattern_details_data: Save out the aggregated results from S04
  either locally or to GCS
- S06-pattern_projects_details: Sample code for pulling project level data 
  for given patterns. Currently requires OAuth to run. 
- S07-yarn_from_projects: Sample code pulling the detailed yarn info for
  the yarn used in a given project. 

Please see the README_tech.md file for more detailed technical information, 
including info on how to use the Ravelry API. 

Documentation on the Ravelry API can be found here: 

https://www.ravelry.com/api

This project is utilizing Cauldron notebooks. For more info on these, 
see the the README_tech. 

**Note:** This code has become quite detailed as I've dealt with 
complexities around pulling significant chunks of data rather than one 
off requests. In a later update I'll add a notebook for the more
simple/one off requests, in addition to the more complex code for handling 
larger data pulls. 

Additionally, as this code has been developed to pull more than just a 
couple items at a time, I've regularly monitored how much data I'm pulling, 
and how fast, to ensure I'm not pulling too much data at once, causing 
unfair load on Ravelry. Please be aware and responsible when pulling data 
from any API such as the Ravelry one. 

### Planned Project 1: Sweaters - What makes a sweater pattern popular?
As of today, Ravelry has 121,293 sweater patterns. I'd like to pull the data 
for those patterns to learn what makes a pattern popular. 

At this point I've just been working on the data pull. Models to come! 

Ways we could define popularity:
- Number of projects using the pattern
    - Number of started, finished, frogged (started but ripped out)
- Number of Queues the pattern is in
- Number of Ratings of the pattern
- Average Rating of the pattern
- Number of comments on the pattern
- Number of forum posts tagging the pattern

In this case, I'm going to define popularity by the number of projects 
using the given pattern. Other ways we could look at popularity is the average 
rating of the pattern, number of comments on the pattern, number of forum 
posts tagging the pattern

Using the data available, I'd like to start by looking at:
- What features are most important to determining the number of projects 
  using the pattern?
- How well I predict the number of projects a pattern will have based on those 
  features?
