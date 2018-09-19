# -*- coding: utf-8 -*-
import requests
import requests_cache
import re

requests_cache.install_cache('github_cache')


class GitHub():
    BASE_URL = "https://api.github.com"
    repoinfo = "/repos/{user}/{repo}"

    def __init__(self, url):
        self.user, self.repo = self.parse_github_url(url)

    def search_for_url(self, word, return_keys=False):
        path = self.repoinfo.format(user=self.user, repo=self.repo)
        r = requests.get(self.BASE_URL + path)

        if r and r.status_code == 200:
            urls = r.json()
            query = re.compile(r'{word}.*_url'.format(word=word))
            keys = list(filter(query.match, urls.keys()))

            if return_keys:
                return [key.split("_url")[0] for key in keys]
            else:
                return [[key.split("_url")[0], urls[key]] for key in keys]

    def parse_github_url(self, url):
        """ Extracts user and repo from url """
        parts = url.split("github.com")[1].split("/")
        return parts[1], parts[2]

    def get_repo_url(self):
        return "https://github.com/{user}/{repo}".format(
            user=self.user,
            repo=self.repo
        )

    def url_for(self, endpoint):
        return self.get_repo_url() + "/" + endpoint


def test_parse_github_url():
    url = "https://github.com/technocake/goto"

    api = GitHub(url)
    assert api.user == "technocake", "user is not correct"
    assert api.repo == "goto", "repo is not correct"


def test_search_for_url():
    url = "https://github.com/technocake/goto"
    api = GitHub(url)
    url = api.search_for_url("issues")
    print(url)
    url = api.search_for_url("pu")
    print(url)
    url = api.search_for_url("c")
    print(url)
    url = api.search_for_url("Å")
    print(url)


if __name__ == '__main__':
    test_parse_github_url()
    test_search_for_url()
