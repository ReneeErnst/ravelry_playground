# Ravelry Playground
Place to play with data from the Ravelry API

## Intro
To start this project I've built a few functions that can be used for pulling 
data from the Ravelry API. I'm trying to be cautious to not pull too much data 
at once, putting a load on their systems. 

### Project 1: Sweaters - What makes a sweater pattern popular?
As of today, Ravelry has 121,293 sweater patterns. I'd like to pull the data 
for those patterns to learn what makes a pattern popular. 

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
- Can well I predict the number of projects a pattern will have based on those 
  features?

# General notes: 

## Could be of interest and do not require auth:
GET /people/{username}/comments/list.json

GET /people/{username}/fiber/{id}/comments.json
Retrieve a stashed fiber's comments

GET /forum_posts/unread.json
Get list of unread posts, across all forums

GET /groups/search.json
Search the group directory

GET /pattern_attributes/groups.json
List the current pattern attributes

GET /pattern_categories/list.json
List the current pattern categories

GET /pattern_sources/search.json
Search pattern source database

GET /pattern_sources/{id}.json
Get pattern source details

GET /patterns/{id}/comments.json
Retrieve a pattern's comments

GET /patterns.json
Get pattern details for multiple patterns

GET /patterns/{id}/projects.json
Retrieve the list of projects that are linked to this pattern

GET /patterns/search.json
Search pattern database

GET /patterns/{id}.json
Get pattern details

GET /projects/{username}/{id}/comments.json
Retrieve a project's comments

GET /projects/search.json
Search the project database

GET /shops/search.json
Search yarn shop database

GET /shops/{id}.json
Get shop details

GET /people/{username}/stash/{id}/comments.json
Retrieve a stashed yarn's comments

GET /stash/search.json
Search the project database

GET /stores/list.json
List the current user's pattern stores

GET /stores/#{store_id}/products.json
List the products in a user's stores

GET /yarn_companies/search.json
Search the yarn company directory

GET /yarns/search.json
Search yarn database

GET /yarns/{id}.json
Get yarn details

GET /yarns.json
Get yarn details for multiple yarns



## requires auth:
GET /designers/{id}.json
Get designer details

GET /people/{username}/favorites/list.json
Get favorite list

GET /forums/{forum_id}/topics.json
Get topic list for a specific forum, personalize for the authenticated user

GET /people/{id}.json
Get user profile

POST /projects/crafts.json
Get list of crafts that are valid for use within projects

GET /projects/{username}/list.json
Get project list

GET /projects/{username}/{id}.json
Get project detail

GET /people/{username}/queue/list.json
Get queued project list

GET /people/{username}/queue/order.json
Get queue ordering (list of all names, ids, and positions)

GET /people/{username}/queue/{id}.json
Get queued project detail

GET /people/{username}/stash/list.json
Get stash list

GET /people/{username}/stash/{id}.json
Get stash list

# Run Cauldron in container on PC
Build docker image included in this repo, adjusting packages in 
requirements.txt as needed. 

Ensure requirements used are the same in both the remotely running container 
and the one on your PC

### Build the local docker image:

`docker build -t ravelry_playground:latest .`

### Start container with it starting Cauldron:

```
docker run -it -rm 
    --workdir=/project 
    --volume=<location_of_repo>/project 
    -p=5010:8000 
    <image_name>
```

Example directory: C:/Users/gxxxxxx/repos/ravelry_playground
Example Image Name: ravelry_playground:latest

Or use the start_container.py file passing in that you want to run the 
container with cauldron started:

`python start_container.py --container cauldron`

Connect to cauldron in your browser (use Chrome):

Go to:
`http://localhost:5010/`

### Start container with command line interface:
```
docker run -it -rm 
    --workdir=/project 
    --volume=<location_of_repo>/project 
    <image_name>
    /bin/bash
```

Or use the start_container.py file passing in that you want to run the 
container with command line control:

`python start_container.py --container command_line`

# Connect Cauldron running on container on PC to remote container for execution
