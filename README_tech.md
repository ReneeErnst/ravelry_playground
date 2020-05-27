# Technical documentation
Below I'm including various technical documentation and how-tos related 
to the code in this repo. It's still in development and being organized, 
but should have most of the info needed to replicate what has been done
in this repo. 

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

#### Cauldron Notebooks
Cauldron Notebooks are similar to Jupyter Notebooks, except that what 
would normally be a cell in Jupyter is now a Step in Cauldron, and each 
step is it's own Python file. In Cauldron you edit your code in your code 
editor of choice (I prefer PyCharm), and then you run and see results of 
steps in the browser. 

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
COMING SOON

# General notes/tips: 

### Printing json:
```
import json
print(json.dumps(patterns[0], indent=2))
```

### Remote execution into GCP instance (execution in GCP rather than locally)
If you are wanting to edit your code locally, but have the code execute in
GCP (using GCP resources), you can follow the below steps for Cauldron. 
I have another repo which includes instructions for other types of 
remote execution as well, including using Jupyter and via JetBrains 
products such as PyCharm here:

https://github.com/ReneeErnst/end-to-end-model-test-gcp

Connecting Cauldron to compute instance in GCP:
- Start your instance in GCP (I'm using an AI Platform Notebook Instance)
    - I did this via the console, but you can also do this via 
      gcloud commands
    - If you are using an AI Platform Notebook instance I suggest 
      installing your packages using the built in Jupyter Notebook 
      functionality.
        - Once the instance starts in the console, select OPEN JUPYTER LAB
        - Clone the repo 
        - Open a terminal in Jupyter lab and `pip3 install -r requirements.txt`
- SSH into that running instance - note that if you don't indicate a zone 
  one will be picked for you in whatever region you specified for the 
  instance. 
  
    ```
    gcloud compute ssh <instance-name>
      --project <project-id>
      --zone <zone>
      -- 
      -L 5010:localhost:5010 
    ```
- A putty window will open if you are on windows (I haven't tried this 
  on a different OS, but instructions should be similar). Any commands 
  you run in this window will execute in your instance. Note that the 
  default python version (as of today's date) is 2.7, make sure that you 
  specify python3 and pip3 for those commands
- Start a Cauldron Kernel in the PuTTY instance:

    `cauldron kernel --port=5010`
    
- In your command line tool of choice, launch cauldron on your 
  machine connecting to that now open port:
    
    `cauldron ui --connect=127.0.0.1:5010`
    
- Cauldron will now open in your browser and you are ready to go!
    - Note: If you have troubles I recommend using Chrome

### GCP authentication when Running Locally but Saving to GCP
If interacting with Google Cloud Platform for anything other than saving data 
to BigQuery via pandas-gbq, you will need to follow the below authentication 
steps. 

If only using pandas-gbq, you will get instructions on 
authenticating the first time you run it. Go to the terminal where you 
kicked off Cauldron for when that happens as you will need to go to 
the url provided and then enter the credentials info. 

For all other authentication needs, you will need to authenticate to GCP. 
If you are running your code in a local container, this will need to be 
done from inside the container. The following steps assume you are doing 
this within a container, but can be used for auth generally. 

If you started the container to immediately run cauldron, you need to exec into 
that running container and auth to GCP:
- In a new terminal window use this command to get the name of your running 
  container:
  
  `docker container ls`
  
- Exec into that container for running commands:

  `docker exec -it <container_name> bash`

- Once exec'ed into the container, follow these steps: 
    - Authenticate to GCP: 
        `gcloud auth application-default login`

You should now be set up to interact with GCP from your running container! 
You can now exit by simply entering 'exit'.
