"""
This file holds all the class functions which uses github module and collect the required stats and returns the value.
"""
from github import Github


class Repo_Stat():

    def __init__(self, token):
        self.github_obj = Github(token)


    def get_repo_stars(self, repository):
        "Return the number of stars the repo contains"
        repo = self.github_obj.get_repo(repository)
        stars = repo.stargazers_count

        return stars


    def get_repo_forks(self, repository):
        "Return the number of forks the repo contains"
        repo = self.github_obj.get_repo(repository)
        forks = repo.forks_count

        return forks


    def get_repo_clone(self, repository, today_date):
        "Return the number of clones and unique clones the repo contains"
        repo = self.github_obj.get_repo(repository)
        clone_dict = repo.get_clones_traffic()
        clones = clone_dict['clones']
        for clone in clones:
            if str(today_date) in str(clone.timestamp):
                clone_count = clone.count
                unique_clone_count = clone.uniques
                break
            else:
                clone_count = 0
                unique_clone_count = 0

        return clone_dict, clone_count, unique_clone_count


    def get_repo_views(self, repository, today_date):
        "Return the number of visitors and unique views the repo contains"
        repo = self.github_obj.get_repo(repository)
        visitors_dict = repo.get_views_traffic()
        views = visitors_dict['views']
        for view in views:
            if str(today_date) in str(view.timestamp):
                view_count = view.count
                unique_visitors = view.uniques
                break
            else:
                view_count = 0
                unique_visitors = 0

        return visitors_dict, view_count, unique_visitors