"""
This is a sample script which connects to to GitHub account via PyGithub library using token and collect repository details into a csv file and store/append the csv file on the AWS bucket.
"""
import boto3, csv, datetime, pytz
from github_module_methods.repo_stats import Repo_Stat
import conf.git_stat_conf as conf


#----START OF SCRIPT in Lambda function---
def lambda_handler(event, context):
    s3 = boto3.client('s3')

    #Collecting paths and bucket name from conf file
    global lambda_temp_file
    lambda_temp_file = conf.lambda_temp_file
    my_s3_bucket = conf.s3_bucket_name
    s3_csv_file = conf.s3_csv_file

    #Download s3 csv file to lambda tmp folder. If csv is not exist in s3, create a csv file in temp folder
    response = s3.list_objects_v2(Bucket=my_s3_bucket, Prefix=s3_csv_file)
    if response.get('Contents'):
        s3.download_file(my_s3_bucket, s3_csv_file, lambda_temp_file)
    else:
        csv.writer(open(lambda_temp_file, "w+"))

    #Creating an instance of the class
    git_obj = Repo_Stat(conf.token)
    repositories = conf.repositories

    #Converting GMT date time to IST date time since the lambda function uses GMT time standard
    date = datetime.datetime.today()
    zone = pytz.timezone('Asia/Kolkata')
    date_ist = date.astimezone(zone)
    today_date = date_ist.strftime("%Y-%m-%d")
    date_time = date_ist.strftime("%Y-%m-%d %H:%M:%S")

    #Opening csv file from lambda tmp folder.
    with open(lambda_temp_file, 'a+', newline='') as f:
        write = csv.writer(f, delimiter=',')

        #If header row is not available, write the header row.
        if f.tell() == 0:
            write.writerow(['Repository', 'Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])

        for repository in repositories:
            stars = git_obj.get_repo_stars(repository)
            forks = git_obj.get_repo_forks(repository)
            clone_dict, clone_count, unique_clone_count = git_obj.get_repo_clone(repository, today_date)
            visitors_dict, view_count, unique_visitors = git_obj.get_repo_views(repository, today_date)

            #Writing the collected values to csv file
            write.writerow([repository, date_time, stars, forks, clone_count, unique_clone_count, view_count, unique_visitors, clone_dict['count'], clone_dict['uniques'], visitors_dict['count'], visitors_dict['uniques']])

    #Upload the lambda temp file to s3 bucket
    s3.upload_file(lambda_temp_file, my_s3_bucket, s3_csv_file)

    return {
        'message': 'success!!'
    }