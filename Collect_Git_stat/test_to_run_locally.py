"""
This is a sample script which connects to GitHub account via PyGithub library using token and get details about repository.
"""
from github import Github
import csv
import datetime
import conf

def store_github_stats(username,token):
    user = token.get_user(username)
    repo_name = conf.repo_name
    date = datetime.date.today()
    for repo in user.get_repos():
        if repo_name in repo.name:

            # Fetch today's clone details by comparing with today date. 
            clone_value = repo.get_clones_traffic()
            clones = clone_value['clones']
            for clone in clones:
                if str(date) in str(clone.timestamp):
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
                if str(date) in str(view.timestamp):
                    view_count = view.count
                    unique_visitors = view.uniques
                    break
                else: 
                    view_count = 0
                    unique_visitors = 0

            # Fetch number of stars and forkes for the repo
            stars = repo.stargazers_count
            forks = repo.forks
            
    #Writing the latest Github Stats to the csv file.
    with open("mycsv.csv", 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')
        if f.tell() == 0:
            write.writerow(['Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])
        write.writerow([datetime.datetime.today(), stars, forks, clone_count, unique_clone_count, view_count, unique_visitors, clone_value['count'], clone_value['uniques'], visitors_value['count'], visitors_value['uniques']])

    print('{} has {} stars'.format(repo_name,stars))
    print('{} has {} forks'.format(repo_name,forks))
    print('{} has {} clones for the day'.format(repo_name,clone_count))
    print('{} has {} unique clones for the day'.format(repo_name,unique_clone_count))
    print('{} has {} views for the day'.format(repo_name,view_count))
    print('{} has {} unique visitors for the day'.format(repo_name,unique_visitors))
    print('{} has {} clones for last 14 days'.format(repo_name,clone_value['count']))
    print('{} has {} unique clones for last 14 days'.format(repo_name,clone_value['uniques']))
    print('{} has {} views for last 14 days'.format(repo_name,visitors_value['count']))
    print('{} has {} unique visitors for last 14 days'.format(repo_name,visitors_value['uniques']))

#----START OF SCRIPT---
if __name__ == "__main__":
    github_user = conf.github_username
    token = Github(conf.token)
    store_github_stats(github_user,token)