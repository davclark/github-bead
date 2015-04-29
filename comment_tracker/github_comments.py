import requests
import json

class GitHubComments:
    key = '63f38f069567d2468f1be592301eb096acb2682b'
    
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        parameters = {'state': 'all', 'per_page': 100}
        self.request_issues = requests.get('https://api.github.com/repos/' + self.owner +
                         '/' + self.repo + '/issues', auth=(GitHubComments.key, 'x-oauth-basic'), params=parameters).json()
        parameters = {'per_page': 100, 'direction': 'desc', 'sort': 'created'}
        self.request_repo_comments = requests.get('https://api.github.com/repos/'
                                + self.owner + '/' + self.repo + '/issues/comments', auth=(GitHubComments.key, 'x-oauth-basic'), params=parameters).headers
        self.all_comments = self.__get_all_comments()

    def __get_all_comments(self):
        # Returns a list with all comments in dictionaries (most recent to oldest). 
        parameters = {'state': 'all', 'per_page': 100}
        comments_page = self.request_repo_comments['link'].split(';')[1].split(',')[1][2:-1]
        comments_page_URL = comments_page[:-1]
        last_page_number = int(comments_page[-1:])
        all_comments = []
        for i in range(1, last_page_number + 1):
            comments_URL = comments_page_URL + str(i)
            all_comments += requests.get(comments_URL, params=parameters).json()
        return all_comments

    def get_issue_with_index(self, i):
        # Returns the number assigned to the issue when made. 
        return str(self.request_issues[i]['number'])

    def get_issue_with_title(self, title):
        # Returns the number assigned to the issue when made.
        for i in range(len(self.request_issues) - 1):
            if title == str(self.request_issues[i]['title']):
                return str(self.request_issues[i]['number'])




    def get_all_creators(self):
        creators = []
        for i in range(len(self.all_comments)):
            if self.get_creator(i) not in creators:
                creators.append(self.get_creator(i))
        return creators

    def get_comments_issue(self, num):
        # GET request to get the all the comments specific to an issue.
        parameters = {'per_page': 100, 'direction': 'desc', 'sort': 'created'}
        return requests.get('https://api.github.com/repos/' + self.owner +
            '/' + self.repo + '/issues/' + str(num) + '/comments', auth=(GitHubComments.key, 'x-oauth-basic'),
            params=parameters).json()
    

    def get_creator(self, i):
        # Returns who created the comment for a specific comment.
        return str(self.all_comments[i]['user']['login'])

    def get_message(self, i):
        # Returns what the comment says.
        return str(self.all_comments[i]['body'])

    def get_comments_creator(self, creator):
        # Returns the indices of the comments that has a specific creator.
        index = []
        for i in range(len(self.all_comments)):
            if self.get_creator(i) == creator:
                index.append(i)
        return index





 