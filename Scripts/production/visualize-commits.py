from git import Repo

repositoryURL = 'http://github.com/gferreira/amstelvar-avar2/'

R = Repo(repositoryURL)
assert not R.bare

print(R)
