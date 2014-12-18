Installation
============

To install UrbanFootprint install these steps.

Document Conventions
--------------------

Code that you would type in on the command line will look like:
::
  sudo mkdir new_directory

These commands can generally be cut and pasted into the command line. 

**Hint:** windows user using putty can select the text and then paste it into the terminal window by right clicking.

*Each line that appears in a section of code should be entered as an individual line, executed, and then the next line should be entered and executed.*

Setup
-----
These instructions assume that you've got an Ubuntu 14.04LTS server that has just been created. They have been tested on Amazon Web Services EC2 instances.

System requirements
___________________

There are no set system requirements and performance has not been tested across a wide variety of hardware.

To date the common EC2 instance used for running UrbanFootprint has been a "m3.2xlarge" instance. These have 8 avaliable CPUs, 30GB of memory, and 2 80GB SSD storage drives associated with them by default as of 11/14/2014.

Access to the repository
________________________
You will need to create a free bitbucket account at http://bitbucket.org
After creating the account you will need to request access to the repository from Evan Babb.

Using Amazon
____________

AWS Account
+++++++++++
Set up an Amazon Web Service account. This will require a credit card to cover costs.
http://aws.amazon.com/



Install PuTTY (Windows)
++++++++++++++++++++++++

http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html

PuTTY is a commonly used set of utilities for remote connection to Linux and Ubuntu computers from windows.
I recommend using the Windows installer that installs "everything except PuTTYtel." As of this writing the version is PuTTY v0.63. 

SSH Key
+++++++

Follow Amazon's instructions for creating a SSH key pair.

http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html

AWS Security Profile
++++++++++++++++++++

Inbound traffic: 
Type		Protocol	Port Range	Source
SSH		TCP		22		0.0.0.0/0
HTTP		TCP		80		0.0.0.0/0
Custom TCP	TCP		8081		0.0.0.0/0

These settings are worth reviewing with your system administrator.
It would be a good idea to restrict the SSH sources to an IP range that exists within your organization for improved security. The same is true of the Custom TCP o n Port 8081 if you're assigning an IP address directly to the machine or paying for a fixed one from Amazon. 

the HTTP port 80 is the standard port that almost all web traffic uses and as such needs to be left open to all sources that may want to use UrbanFootprint. You could use this to limit access to only your organization.


Outbound traffic:
All traffic and all protocols on all ports to all destinations are open. i.e. there's no restrictions on outbound traffic.

Create Instance
+++++++++++++++

Ubuntu 14.04LTS 64 Bit

A *m3.2xlarge* instance seems to work well, and at present has a cost of $0.56 per hour (which may change).

Note: I have run it on a m3.large instance and the reduced number of cpus and ram. It is possible, and is cheaper, but is not as effective as the larger instance if you need to run any of the complex analytical modules.  

No extra storage (it could be added later). 

Select the security profile set up in the previous step.

Initialize the instance.
 

Installation
------------

What follows are the instructions for installing the software components of UrbanFootprint. It does not yet include loading data into it to create a fully operational installation

Step 1: Log in
______________

Log in to your server using a SSH terminal connection. Make sure that you have "sudo" (administrative) permissions.

Step 2: Install git
___________________
The first significant installation step is to make sure that you have the "git" installed. Git will be used to connect to the the source of all of the code for operating UrbanFootprint and the instructions for its configuration.
::
  sudo apt-get install git

You will be asked to approve the installation. Enter Y+return to do so.

Step 3: Clone the repository
____________________________

This will create a local copy of the source code and instructions used by the computer to install it on your local computer.
::
  git clone https://bitbucket.org/calthorpe/urbanfootprint.git 

You will be asked for your bitbucket account name and password

If you type:
::
  ls

You will now see an additonal item listed in the "home" folder of the account you're logged in with called "urbanfootprint"


Step 4: Run the installation script
___________________________________

This step will run the installation of UrbanFootprint. It will take ~1hour to run, but will need some input from you near the beginning.
::
  cd urbanfootprint

This will change your directory to the urbanfootprint directory created in the previous step.
::
  sudo ./setup.sh

This will start the script.

The script first runs an update on the system's software and will ask you to approve several installations and modifications. For each of these type Y+return.

You will then be asked to create a name for your server. Enter a logical name for it. For example: uf_ice

You will need to then enter your bitbucket account name and password. What happens here is that your server is registering itself with the bitbucket account using a SSH key. This will enable it to complete the rest of the software installation without needing further use of the user name and password.

You will know it's done when the text stops scrolling by and you see something that looks like:
::
  ubuntu@ip-172-31-36-172:~/urbanfootprint$

At this point you can go get coffee, it will probably take about an hour to complete (on an EC2 m3.2xlarge instance, other systems may vary significantly).


Step 5: Configuration
_____________________

After the installation completes, you will need to do some initial configuration of the installation.

Set the user and virtual environment
++++++++++++++++++++++++++++++++++++

Do the following steps:
To log in as the "calthorpe" user under which most of the server is setup.
::
  su calthorpe

You'll be able to tell that this worked if you see your command line looking something like:
::
  calthorpe@....$


To move to the folder holding the configuration settings.
::
  cd /srv/calthorpe/urbanfootprint/footprint

To make a copy of the default settings file for customization
::
  cp local_settings.py.default local_settings.py.mycopy

To create a link between the configuration settings copy we made and the file name expected by UrbanFootprint.
::
  ln -sf local_settings.py.mycopy local_settings.py

Step 6: Add yourself as an administrator
________________________________________
We need to edit the local_settings.py file to add you as an administrator.
::
  nano local_settings.py

Then use the arrow keys to scroll all the way to the bottom. Insert the following after the last line in the file.
::
  ADMINS = (
    ('Your Name', 'you@example.com'),
  )

use the arrow keys to update your name and email leaving the quotes.

Exit by using Ctrl+x, and then typing Y when asked to save the file.

Your user name is your name, and default password is <username>@uf

Step 7: Check the services
__________________________

Run:
::
  sudo supervisorctl status

You should then see the following:
:: 
  ubuntu@ip-172-31-2-7:~$ sudo supervisorctl status
  calthorpe_www                    RUNNING    pid 7336, uptime 0:30:17
  celery_flower                    RUNNING    pid 7340, uptime 0:30:17
  celery_worker                    RUNNING    pid 7339, uptime 0:30:17
  celerybeat                       RUNNING    pid 7342, uptime 0:30:17
  node_socketio                    RUNNING    pid 7341, uptime 0:30:17
  tilestache                       FATAL      Exited too quickly (process log may have details)

Tilestache will be unable to run until we give it some mapping data to work with.

This concludes the primary installation of UrbanFootprint.

If you would like, you can now remove the urbanfootprint directory in /home/ubuntu by:
::
  rm -rf urbanfootprint


Step 8: Transfer base data to server
____________________________________

I recommend using FileZilla (or similar SFTP capable FTP Client) to get your data onto the server.

Establish a connection profile, and specify the use of the username (ubuntu for an EC2 instance) and making sure that your pageant install is loading the ssh key. 

Transfer the <filename>.dump file to the server

Step 9: Create a staging database
_________________________________

Switch your user name to the calthorpe user and activate the virtual environment that UrbanFootprint runs in. You will need to do activate the virtual environment any time you're making changes to UrbanFootprint's configuration from the commandline.

if you don't see the start of the command prompt looking like:
::
  calthorpe@....$

Switch to the calthorpe user.
::
  su calthorpe

And enter the calthorpe password: Calthorpe123

Activate the virtual environment
::
  cd /srv/calthorpe/urbanfootprint/
  source /srv/calthorpe_env/bin/activate

After activating the virtual environment your command prompt should look like:
::
  (calthorpe_env)calthorpe@...$


Create a staging database
::
  createdb stage_db

If you get an error stating that the database "calthorpe" does not exist, create the calthorpe database for convenience.
::
  createdb calthorpe

Then:
::
  createdb stage_db

Add the postgis extension to stage_db
::
  psql -d stage_db -c "CREATE EXTENSION postgis;"

Then import the database dump to the staging database.
::
  pg_restore -d stage_db /home/ubuntu/UF_yolo_data.dump

This is assuming the data you're loading is in a file called UF_yolo_data.dump and that it is in the home directory of the ubuntu user. Adjust the path to the dump file as needed.

Step 10. Prepare for data import 
________________________________

First, a work around that is needed on Amazon instances to work within the security system.

Note: If you're doing a non-amazon installation then you'llw ant to substitute "local_prod" in place of "amazon_local" and can skip past the next few lines to "configuring the connection to the staging database".

Copy the PEM file that you're using to connect to the server to the /home/calthorpe/.ssh

First upload it the same way you did the data dump file to /home/ubuntu/ 

Then do the following which will move the pem file to the calthorpe user folders and set permissions so that it can be used as a ssh key.
::
  cd /home/calthorpe/.ssh
  sudo mv /home/ubuntu/<name>.pem <name>.pem
  sudo chmod 600 <name>.pem
  sudo chown calthorpe:calthorpe <name>.pem

Update the fabric host files so that they recognize that key/pem file
::
  cd /srv/calthorpe/urbanfootprint/fabfile/hosts
  nano __init__.py

In the def amazon_local(): section, update the path at:
::
  env.key_filename = '/home/calthorpe/.ssh/pemfile.pem'

To point to the pem file you just copied into place.

Then save the changes with Ctrl+X and Y to save the changes.

Next we need to make sure that the file is not over written the next time we pull an update of the code (which will happen shortly).
::
  git commit -a -m "adjusted local settings"

This records our changes into the local copy of the git repository so that they are not over written.

Connecting to the staging database
++++++++++++++++++++++++++++++++++

Last, we need to tell UrbanFootprint how it is going to connect to the staging database.

This tutorial is built around the SACOG data model so we'll use that now.
::
  cd /srv/calthorpe/urbanfootprint/footprint/client/configuration/sacog
  nano sacog_init.py

Look for a section that like: (approximatley line 45, use Ctrl+C to show the line number where the cursor is at present).
::
  def import_database(self):
    if settings.USE_LOCAL_SAMPLE_DATA_SETS:
      ...
    else:
      return dict(
        host = 'localhost',
        database = 'stage_db',
        user = 'calthorpe',
        password = 'Calthorpe123'
      )

Edit the host = and database = to point to 'localhost', and the name of your staging database resepectively (so they may look like the example above)

And then commit our changes to git.
::
  git commit -a -m "adjusted staging database settings"


Step 11. Build UrbanFootprint
_____________________________

Some of these steps may take a long time to complete

Switch back to the main urbanfootprint folder.
::
  cd /srv/calthorpe/urbanfootprint

Specify the client name and settings (takes about 2min.)
::
  fab amazon_local client:sacog

Import the staging database settings (takes about 2min.)
::
  fab amazon_local local_settings:stage

Do a code update. This is an abbreviated version of the installation that we did earlier. (takes about 2 min.)
::
  fab amazon_local deploy

Do the data import and system setup. (takes 30min+)
::
  fab amazon_local recreate_dev

You will be asked twice if you want to continue because if you have an existing UrbanFootprint database of the same name it will be completely overwritten by this step.  



