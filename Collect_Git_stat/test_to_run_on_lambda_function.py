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
    github_obj = Github(conf.token)
    repositories = conf.repositories
    
    # Calling GitHub function to get the Dunzo Repository stats.
    store_github_stats(github_obj,repositories)

    # upload the lambda temp file to s3 bucket
    s3.upload_file(lambda_temp_file, my_s3_bucket, s3_csv_file)
    
    return {
        'message': 'success!!'
    }

def store_github_stats(github_obj,repositories):
    
    # Converting GMT date time to IST date time
    date = datetime.datetime.today()
    zone = pytz.timezone('Asia/Kolkata')
    date_ist = date.astimezone(zone)
    today_date = date_ist.strftime("%Y-%m-%d")
    date_time = date_ist.strftime("%Y-%m-%d %H:%M:%S")
    
    #Opening csv file to write the collected Github Stats.
    with open(lambda_temp_file, 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')

        #If header row is not available, write the header row.
        if f.tell() == 0:
            write.writerow(['Repository','Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])
        
        #Loop for the each listed repositories
        for repository in repositories:
            repo = github_obj.get_repo(repository)

            #Collect the number of stars the repo contains
            stars = repo.stargazers_count

            #Collect the number of forks the repo contains
            forks = repo.forks

            #Collect the clone details and fetch today's clones by comparing with date.
            clone_value = repo.get_clones_traffic()
            clones = clone_value['clones']
            for clone in clones:
                if str(today_date) in str(clone.timestamp):
                    clone_count = clone.count
                    unique_clone_count = clone.uniques
                    break
                else: 
                    clone_count = 0
                    unique_clone_count = 0

            #Collect the view details and fetch today's views by comparing with date.
            visitors_value = repo.get_views_traffic()
            views = visitors_value['views']
            for view in views:
                if str(today_date) in str(view.timestamp):
                    view_count = view.count
                    unique_visitors = view.uniques
                    break
                else: 
                    view_count = 0
                    unique_visitors = 0
                    
            #Writing the collected values to csv file
            write.writerow([repository, date_time, stars, forks, clone_count, unique_clone_count, view_count, unique_visitors, clone_value['count'], clone_value['uniques'], visitors_value['count'], visitors_value['uniques']])