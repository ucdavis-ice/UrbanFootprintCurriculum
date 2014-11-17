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

Do the following steps:
::
  sudo su calthorpe

To log in as the "calthorpe" user under which most of the server is setup.
::
  cd /srv/calthorpe/urbanfootprint/footprint

To move to the folder holding the configuration settings.
::
  cp local_settings.py.default local_settings.py.mycopy

To make a copy of the default settings file for customization
::
  ln -sf local_settings.py.mycopy local_settings.py

To create a link between the configuration settings copy we made and the file name expected by UrbanFootprint.

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







