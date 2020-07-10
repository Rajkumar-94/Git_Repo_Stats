"""
This is a sample script that connects to the GitHub account via PyGithub library using token and collect repository details such as number of stars, forks, clones, unique clones, view and unique visitors.
The methods are written on repo_stats.py file and called via the test file
The collected details are stored on csv file.
"""
import datetime, csv
from github_module_methods.repo_stats import Repo_Stat
import conf.git_stat_conf as conf


def collect_repo_stat(test_obj):
    "Run the test"
    today_date = datetime.date.today()
    repositories = conf.repositories

    #Open the csv file
    with open("mycsv.csv", 'a+', newline='') as f:
        write = csv.writer(f, delimiter=',')
        #If header row is not available, write the header row.
        if f.tell() == 0:
            write.writerow(['Repository', 'Date', 'Starts', 'Forks', 'Today\'s Clones', 'Today\'s Unique Clones', 'Today\'s Views', 'Today\'s Unique Visitors', 'Fortnight Clones', 'Fortnight Unique Clones', 'Fortnight Views', 'Fortnight unique Views'])

        #For each listed repository collect the repo stats, store in the csv file and print the results as well.
        for repository in repositories:
            stars = test_obj.get_repo_stars(repository)
            forks = test_obj.get_repo_forks(repository)
            clone_dict, clone_count, unique_clone_count = test_obj.get_repo_clone(repository, today_date)
            visitors_dict, view_count, unique_visitors = test_obj.get_repo_views(repository, today_date)

            #Print the repo stats
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

#----START OF SCRIPT----
if __name__ == "__main__":
    #Creating an instance of the class
    test_obj = Repo_Stat(conf.token)
    collect_repo_stat(test_obj)