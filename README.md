# A python code to collect GitHub repository statistics.

You can use this code to collect everyday Git stats for a GitHub repository. Since the Git traffic stats will be available for the last 14 days, you can use this to keep tack for every day's git stat details.
This code uses PyGitHub library which is used to fetch the Git repository stats such as clone, visitors, stars, forks, and store it in CSV file.
Here we have 2 codes, one to run locally and another is to run in AWS lambda function. The reason we tried AWS lambda function is that we can trigger the lambda function to run every day at a specific time by using the AWS CloudWatch service. So every day at the specified time the required data can be collected and stored without human interventions.

------
Setup to run the code locally:
------

The setup is fairly simple:

a) Install Python 3.x

b) Add Python 3.x to your PATH environment variable

c) If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)

d) Clone this repository

d) pip install -r requirements.txt to install dependencies

e) Log in to GitHub and generate Token with repo permission checked to read Git Stats.

f) Update the conf file, with your details.
Note: To fetch public repository's details, make sure you have the collaborative access for that repository.

d) Run test_to_run_locally.py code, a csv file with GitHub stats will be generated on the same path where the code is available.

Setup to run the code in AWS lambda function:
------

__1. Prerequisites__

a) Create an AWS account, make sure you are using the IAM user preferably (or root user) with the listed access permissions:
i) Full access to S3.
ii) Full access to Lambda
iii) Full access to CloudWatch
iv) Access to create IAM Role creation

b) Create a new bucket in AWS S3 where you would like to store the collected csv file. Record the path for the bucket.

__2. Setup for AWS Lambda function__ 

a) Create an AWS Lambda function that uses Python language.

b) In Lambda function we won't be able to install any python libraries, so install the required libraries like PyGitHub, pytz in local folder by using 
    pip install <package> -t <directory>

c) Copy the conf.py and test_to_run_on_lambda_function.py files to the same directory as above.

d) Select all the file and zip it.

e) In the Lambda function, in Code entry type, choose "Upload a .zip file" to upload your zip folder which consists of code and required libraries to Lambda function. Make sure Handler name is provided correctly. The test file should populate on the Lambda function window.

f) Update the conf file with the details.

g) Save the file which makes that the Lambda function is ready. Test the file and make sure the test runs without any error. If there is no error, the lambda function should create a csv file in the given S3 bucket and the collected data should be present on the csv file.

__3. Setup for AWS CloudWatch Events__ 

a) On top of the AWS Lambda function, there is a option to attach trigger. Select AWS CloudWatch Events with required rules. We can declare when the test should run by using rate/cron. Once the trigger is set to the Lambda function, based on the given condition the Lambda function gets executed. I chose to run the function everyday 11:59 pm Indian time so that the function collects everyday's data at the end of the day.
