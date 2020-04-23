from github import Github
import csv
import datetime
import boto3
import conf

#----START OF SCRIPT in Lambda function---
def lambda_handler(event,context):

    # Actual Lamda code 
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
    for repo in user.get_repos():
        if repo_name in repo.name:
            
            no_of_clone = repo.get_clones_traffic()
            no_of_visitors = repo.get_views_traffic()
            stars = repo.stargazers_count
            forks = repo.forks
            
    #Writing the latest Github Stats to the csv file which is in the lambda temp folder.
    with open(lambda_temp_file, 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')
        if f.tell() == 0:
            write.writerow(['Date','Clone', 'Unique Clone', 'Vistors', 'Unique Visitors', 'Starts', 'Forks', 'Last 14 days Clone details', 'Last 14 days View details'])
        write.writerow([datetime.datetime.today(),no_of_clone['count'],no_of_clone['uniques'],no_of_visitors['count'],no_of_visitors['uniques'],stars,forks,no_of_clone['clones'],no_of_visitors['views']])