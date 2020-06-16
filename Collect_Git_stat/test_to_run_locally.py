"""
This is a sample script that connects to the GitHub account via PyGithub library using token and collect repository details such as number of stars, forks, clones, unique clones, view and unique visitors.
The collected details are stored on csv file.
"""
from github import Github
import csv
import datetime
import conf

def get_repo_stars(github_obj,repository):
    "Return the number of stars the repo contains"
    repo = github_obj.get_repo(repository)
    stars = repo.stargazers_count

    return stars

def get_repo_forks(github_obj,repository):
    "Return the number of forks the repo contains"
    repo = github_obj.get_repo(repository)
    forks = repo.forks_count

    return forks 

def get_repo_clone(github_obj,repository):
    "Return the number of clones and unique clones the repo contains"
    repo = github_obj.get_repo(repository)
    clone_dict = repo.get_clones_traffic()
    clones = clone_dict['clones']
    for clone in clones:
        if str(date) in str(clone.timestamp):
            clone_count = clone.count
            unique_clone_count = clone.uniques
            break
        else: 
            clone_count = 0
            unique_clone_count = 0

    return clone_dict,clone_count,unique_clone_count

def get_repo_views(github_obj,repository):
    "Return the number of visitors and unique views the repo contains"
    repo = github_obj.get_repo(repository)
    visitors_dict = repo.get_views_traffic()
    views = visitors_dict['views']
    for view in views:
        if str(date) in str(view.timestamp):
            view_count = view.count
            unique_visitors = view.uniques
            break
        else: 
            view_count = 0
            unique_visitors = 0
    return visitors_dict,view_count,unique_visitors

#----START OF SCRIPT---
if __name__ == "__main__":
    date = datetime.date.today()
    github_obj = Github(conf.token)
    repositories = conf.repositories

    #Opening csv file
    with open("mycsv.csv",'a+',newline='') as f:
        write = csv.writer(f,delimiter=',')
        #If header row is not available, write the header row.
        if f.tell() == 0:
            write.writerow(['Repository', 'Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])

        for repository in repositories:
            stars = get_repo_stars(github_obj,repository)
            forks = get_repo_forks(github_obj,repository)
            clone_dict,clone_count,unique_clone_count = get_repo_clone(github_obj,repository)
            visitors_dict,view_count,unique_visitors = get_repo_views(github_obj,repository)

            print('{} has {} stars'.format(repository, stars))
            print('{} has {} forks'.format(repository, forks))
            print('{} has {} clones for the day'.format(repository, clone_count))
            print('{} has {} unique clones for the day'.format(repository, unique_clone_count))
            print('{} has {} views for the day'.format(repository, view_count))
            print('{} has {} unique visitors for the day'.format(repository, unique_visitors))
            print('{} has {} clones for last 14 days'.format(repository, clone_dict['count']))
            print('{} has {} unique clones for last 14 days'.format(repository, clone_dict['uniques']))
            print('{} has {} views for last 14 days'.format(repository, visitors_dict['count']))
            print('{} has {} unique visitors for last 14 days'.format(repository, visitors_dict['uniques']))

            #Writing the collected values to csv file
            write.writerow([repository, datetime.datetime.today(), stars, forks, clone_count, unique_clone_count, view_count, unique_visitors, clone_dict['count'], clone_dict['uniques'], visitors_dict['count'], visitors_dict['uniques']]) 