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
To start this project I've built a few functions that can be used for pulling 
data from the Ravelry API. I'm now working on building this out to pull enough 
data for Data Science modeling. Below I've included information on how to 
get set up to use the Ravelry API, including different authentication methods. 

#### Cauldron Notebooks
This code is utilizing Cauldron Notebooks. Cauldron Notebooks are similar to 
Jupyter Notebooks, except that what would normally be a cell in Jupyter 
is now a Step in Cauldron, and each step is it's own Python file. In Cauldron 
you edit your code in your code editor of choice (I prefer PyCharm), and then 
you run your steps and see results in the browser. 

One important difference between Cauldron and Jupyter is the way 
information is kept in memory. In Jupyter all variables get kept in memory 
unless explicitly removed. This can create issues with memory consumption or 
not realizing that variables are being changed. In Cauldron you need to 
explicitly define what variables you want to be kept in memory for sharing 
between steps. For example, you you want all steps to be able to use the 
df_data variable, in the step where df_data is created you need to specify 
cd.shared.df_data = df_data, and then in later steps you get df_data by 
including df_data = cd.shared.df_data. 

For more information on Cauldron Notebooks go to http://www.unnotebook.com

**General Note:** As this code will be developed to pull more than just a 
couple items at a time, I'll add functionality that will ensure I'm not 
pulling too much data at once, causing unfair load on Ravelry. Please be aware 
and responsible when pulling data from any API such as the Ravelry one. 

## Ravelry API Info
Documentation on the Ravelry API can be found here: 

https://www.ravelry.com/api

### Authenticating to the Ravelry API
A lot of data is available while only needing Basic Auth. However, I found 
some data that I'd like for my use that required OAuth access, such as pulling 
the projects associated with a specific pattern. As a result, I've set up 
the code to use either authentication method. In S01-setup you will need to 
specify what authentication method you are using for the rest of the 
Cauldron notebook to work. Given that OAuth is likely new to most data 
scientists, I've also document my approach to getting an OAuth token using 
Postman in the OAuth section below. 

To use the Ravelry API you need a free Pro account:

https://www.ravelry.com/pro/developer

If you are already a Ravelry user, you can use this to upgrade your existing 
account or create a new one specifically for using the API. 

Once you have your pro account, you then need to create an App in the apps 
area of your pro account. Once you are on the apps page select **create 
a new app**.

You will now need to select what type of credentials you need. If you only 
want to access data that can be pulled via Basic Auth, select 
'Basic Auth: read only access'. If you want to access data that requires 
being "authenticated" as per the ravelry documentation, select 'OAuth 2.0'. 
Your App will then be created in Ravelry and you will need to select 
**edit app profile** to finish setting it up. 

#### Set up Basic Auth: 
For Basic Auth the only thing you should need to update in the app profile 
is the name of your app. This can be whatever you want, and it would 
technically still work even if you leave it untitled. I also recommend filling 
out the short description. I **do not** recommend selecting the box to create 
a Public Directory Listing since your App is just for personal use. 
Select Save Changes at the bottom of the page and you will be brought back to
your My Apps page.

Here you can see your username and select "show" to see your password. Be 
careful with these credentials! To use these in the code as set up in this 
repo, create a user.txt file at the top level of the repo and include the 
username in that file. Then create a pwd.txt file and put the password in that 
file. Please be careful to not track these in git. This repo already 
includes user.txt and pwd.txt in the gitignore. You can also set up more 
sophisticated approaches to storing your credentials for use in your code. 

Assuming you followed the steps above, you should now be good to use the code 
in this repo to access Ravelry data allowed via Basic Auth!

#### Set up OAuth 2.0:
For accessing any Ravelry data that is indicated as Authenticated in the 
Ravelry documentation, you will need to create an OAuth token rather than 
using the Basic Auth method above. There are many approaches to doing this, 
but I'll outline the most simple one I found that works well for our use 
case - exploring the Ravelry API data for personal use. 

**Note:** These tokens expire after an hour, so if you want something longer 
running, you will need to adjust your approach. 

Once you have created your app in the My Apps section of your Ravelry Pro 
account, select **edit app profile** and do the following:
- Add an Application name in the first entry (this can be anything you want)
- Add a short description of your App (e.g., playing with ravelry data)
- Add https://localhost:5000/callback to the Authorized Redirect URIs box
- Select Save Changes at the end of the page

This will take you back to your main My Apps page. From here you can now get 
your Client ID and Secret. Use these is Postman (see below) to create your 
authentication token. 

You can get Postman here: 
https://www.postman.com/downloads/


**Follow these steps to get your authentication token via Postman:**
###### ToDo: Add images
- Create a new collection by selecting "New Collection". Call this something 
  you will remember, such as 'Ravelry'
- In the top left corner of Postman where it says "New", select the arrow and 
  then "Request"
    - Use a request name that makes sense to you, such as "oauth".
    - In the "Select a collection folder to save to" section, select the 
      Collection you made above.
- Create an environment to store your credentials info:
    - In Postman go to File -> New -> Environment 
    - Name your environment
    - Add variables to your environment
        - Add client_id variable and set initial and current value to 
          your client id from your API page in Ravelry
        - Add client_secret variable and set initial and current value 
          to your secret from your API page in Ravelry
        - Click Add to save the above
- In the top right section of Postman you can see what Environment you 
  are using (to the left of the gear icon). This will likely say 
  No Environment if you haven't used Postman Environments before. 
  Change that to the Environment you just created.
- Go to the Authorization tab in your request created above
    - Under Type select OAuth 2.0
    - Select Get New Access Token
        - Create a token name (anything you wish)
        - Grant Type: Authorization Code
        - Callback URL: https://localhost:5000/callback (the Authorized 
          Redirect URI setup for your App in your Ravelry Pro account)
        - Auth URL: https://www.ravelry.com/oauth2/auth
        - Auth Token URL: https://www.ravelry.com/oauth2/token
        - Client ID: Use the client ID variable you set up in your 
          Postman Environment. If you named that client_id, that would 
          translate to entering {{client_id}} in this field.
        - Client Secret: Same as above but use {{client_secret}}
        - State: Use a random set of numbers and letters
        - Client Authentication: Send as Basic Auth Header
    - Select Request Token
        - This will pop up a window asking if it is ok to allow your 
          app to view and update your ravelry notebook - Select Authorize
        - You will then be taken back to Postman and it will show you your 
          token
        - Copy and paste this into a file called token.txt at the top 
          level of the repo (make sure this does not go in git!)
          
You have now created your authentication token and should be all set! Note 
this token expires every hour. You will need to create a new one once it 
has expired. However, if you have saved your request in Postman, all 
you have to do is go back to the Authorization tab in your request and 
select Get New Access Token and then Request Token to create a new one. 

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

## Run Cauldron in container on PC
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

## Connect Cauldron container on PC to remote container for execution

# General notes/tips: 

### Printing json:
```
import json
print(json.dumps(patterns[0], indent=2))
```

### GCP Authentication
If saving data out to GCP like is being done in this repo, you will first 
need to authenticate to GCP from your computer if you haven't already. If you 
are running your code from a container, you will need to do this within 
your container. The following steps assume you are doing this within a 
container, but can be used for auth generally. 

If you started the container to immediately run cauldron, you need to exec into 
that running container and auth to GCP:
- In a new terminal window use this command to get the name of your running 
  container:
  
  `docker container ls`
  
- Exec into that container for running commands:

  `docker exec -it <container_name> bash`

- Once exec'ed into the container, follow these steps: 
    - Authenticate to GCP: 
    
        `gcloud auth login`

    - Set default project:
        
        `gcloud config set project <project_id>`
        
    - Set default compute region:
    
        `gcloud config set compute/region <compute_region>`

You should now be set up to interact with GCP from your running container! 
You can now exit by simply entering 'exit'.
