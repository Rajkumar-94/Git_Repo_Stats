"""
This is a sample script which connects to GitHub account using token and collect today's stats such as Clone, Unique Clone, Visitors, Unique Vistors, number of Starts and Forks for specified Repository
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
            
    #Writing the latest Github Stats to the csv file which is in the lambda temp folder.
    with open("mycsv.csv", 'a+', newline='') as f:
        write = csv.writer(f,delimiter=',')
        if f.tell() == 0:
            write.writerow(['Date','Today\'s Clone', 'Today\'s Unique Clone', 'Today\'s Vistors', 'Today\'s Unique Visitors', 'Starts', 'Forks', 'Last 14 days Clone', 'Last 14 days Unique Clone', 'Last 14 days Views','Last 14 days unique Views'])
        write.writerow([datetime.datetime.today(), clone_count, unique_clone_count, view_count, unique_visitors,stars,forks,clone_value['count'],clone_value['uniques'],visitors_value['count'],visitors_value['uniques']])


#----START OF SCRIPT---

if __name__ == "__main__":
    github_user = conf.github_username
    token = Github(conf.token)
    store_github_stats(github_user,token)