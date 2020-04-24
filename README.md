# A python code to collect Git Statistics.

You can use this code to collect everyday Git stats for a GitHub repository. Since the Git traffic stats will be available for the last 14 days, you can use this to keep tack for every day's git stat details.
This code uses PyGitHub library which is used to fetch the Git repo stats such as clone, visitors, starts, forks, and store it in CSV file.
Here we have 2 codes, one to run locally and another is to run in AWS lambda function. Here we use GitHub token to connect and fetch Git repo stat details.
The purpose of executing in AWS lambda is we can keep a CloudWatch trigger, so that everyday the function runs on the specied time and collected csv file will be stored on Amazon S3 bucket.

------
Setup 
------

The setup is fairly simple:

a) Install Python 3.x

b) Add Python 3.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) Clone this repository

d) pip install -r requirements.txt to install dependencies

e) Log in to GitHub and generate Token to read Git Stats.

f) Update the conf file, with your details.

d) Run the git_stat.py code, a csv file with GitHub stats will be generated on the same path where the code is available.
