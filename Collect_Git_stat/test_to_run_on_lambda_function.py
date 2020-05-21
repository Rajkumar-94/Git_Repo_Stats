"""
This is a sample script which connects to to GitHub account via PyGithub library using token and collect repository details into a csv file and store/append the csv file on the AWS bucket.
"""
from github import Github
import csv
import datetime
import boto3
import conf
import pytz

#----START OF SCRIPT in Lambda function---
def lambda_handler(event,context):
    s3 = boto3.client('s3')

    # Collecting paths and bucket name from conf file
    global lambda_temp_file
    lambda_temp_file = conf.lambda_temp_file
    my_s3_bucket = conf.s3_bucket_name
    s3_csv_file = conf.s3_csv_file
    
    # Download s3 csv file to lambda tmp folder. If csv is not exist in s3, create a csv file in temp folder
    response = s3.list_objects_v2(Bucket=my_s3_bucket, Prefix=s3_csv_file)
    if response.get('Contents'):
        s3.download_file(my_s3_bucket, s3_csv_file, lambda_temp_file)
    else:
        csv.writer(open(lambda_temp_file, "w+"))
        
    # Assigning GitHub acount username and token
    github_user = conf.github_username
    token = Github(conf.token)
    
    # Calling GitHub function to get the Dunzo Repository stats.
    store_github_stats(github_user,token)

    # upload the lambda temp file to s3 bucket
    s3.upload_file(lambda_temp_file, my_s3_bucket, s3_csv_file)
    
    return {
        'message': 'success!!'
    }

def store_github_stats(username,token):
    user = token.get_user(username)
    repo_name = conf.repo_name

    # Converting GMT date time to IST date time
    date = datetime.datetime.today()
    zone = pytz.timezone('Asia/Kolkata')
    date_ist = date.astimezone(zone)
    today_date = date_ist.strftime("%Y-%m-%d")
    date_time = date_ist.strftime("%Y-%m-%d %H:%M:%S")

    for repo in user.get_repos():
        if repo_name in repo.name:

            # Fetch today's clone details by comparing with today date. 
            clone_value = repo.get_clones_traffic()
            clones = clone_value['clones']
            for clone in clones:
                if today_date in str(clone.timestamp):
                    clone_count = clone.count
                    unique_clone_count = clone.uniques
                    break
                else: 
                    clone_count = 0
                    unique_clone_count = 0

            # Fetch today's view details by comparing with today date.
            visitors_value = repo.get_views_traffic()
            views = visitors_value['views']
            for view in views:
                if today_date in str(view.timestamp):
                    view_count = view.count
                    unique_visitors = view.uniques
                    break
                else: 
                    view_count = 0
                    unique_visitors = 0

            # Fetch number of stars and forkes for the repo
            stars = repo.stargazers_count
            forks = repo.forks
            
    #Writing the latest Github Stats to the csv file which is in the lambda temp folder.
    with open("mycsv.csv", 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')
        if f.tell() == 0:
            write.writerow(['Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])
        write.writerow([datetime.datetime.today(), stars, forks, clone_count, unique_clone_count, view_count, unique_visitors, clone_value['count'], clone_value['uniques'], visitors_value['count'], visitors_value['uniques']])