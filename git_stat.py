"""
This is a sample script to connect to GitHub and collect stats such as Clone, Unique Clone, Visitors, Unique Vistors, number of Starts and Forks for specified Repository
"""
from github import Github
import csv
import datetime
import conf

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
    with open("mycsv.csv", 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')
        if f.tell() == 0:
            write.writerow(['Date','Clone', 'Unique Clone', 'Vistors', 'Unique Visitors', 'Starts', 'Forks', 'Last 14 days Clone details', 'Last 14 days View details'])
        write.writerow([datetime.datetime.today(),no_of_clone['count'],no_of_clone['uniques'],no_of_visitors['count'],no_of_visitors['uniques'],stars,forks,no_of_clone['clones'],no_of_visitors['views']])


#----START OF SCRIPT---

if __name__ == "__main__":
    github_user = conf.github_username
    token = Github(conf.token)
    store_github_stats(github_user,token)