import requests
import sys
import datetime

repo_contributors = dict()
repo_contributions = dict()
repo_contributions_last_year = dict()
unique_contributors = set()
total_contributions = 0

# week_id: total_commits
weekly_contributions = dict()

# Can be collected through GitHub API but it is easier this way
indy_repos = [
'indy-node',
'indy-sdk',
'indy-plenum',
'indy-hipe',
'indy-crypto',
'indy-anoncreds',
'indy-agent',
'indy-post-install-automation',
'indy-jenkins-pipeline-lib',
'indy-test-automation'
]

for repo in indy_repos:
    print('Working on {}'.format(repo))

    repo_contributions_last_year[repo] = 0
    repo_contributors[repo] = 0
    repo_contributions[repo] = 0

    # STATS
    stats_url = 'https://api.github.com/repos/hyperledger/{}/stats/commit_activity'.format(repo)

    stats_resp = requests.get(url=stats_url)

    if not stats_resp.ok:
        print('Rate limit probably reached')
        sys.exit(123)

    stats = stats_resp.json()
    print(stats)

    for week in stats:
        repo_contributions_last_year[repo] += week['total']
        week_id = week['week']
        if weekly_contributions.get(week_id):
            weekly_contributions[week_id] += week['total']
        else:
            weekly_contributions[week_id] = week['total']

    # CONTRIBUTIONS
    contrib_url = 'https://api.github.com/repos/hyperledger/{}/contributors'.format(repo)

    head_resp = requests.head(url=contrib_url)

    if not head_resp.ok:
        print('Rate Limit probably reached')
        sys.exit(123)

    link_header = head_resp.headers.get('link')
    if link_header:
        last_page = link_header.split(';')[1][-2:-1]
    else:
        last_page = 1

    for x in range(1, int(last_page)+1):
        params = {'page': x}
        contributors_resp = requests.get(url=contrib_url, params=params)
        contributors = contributors_resp.json()
        print(contributors_resp.text)

        for contributor in contributors:
            repo_contributors[repo] += 1
            unique_contributors.add(contributor['login'])
            total_contributions += contributor['contributions']
            repo_contributions[repo] += contributor['contributions']

    # CONTRIBUTORS (see extended version of this script for further development (this was the initial cut and does not work
#    exit(0)
#    contrib_stats_url = 'https://api.github.com/repos/hyperledger/{}/stats/contributors'.format(repo)
#
#    contrib_stats_resp = requests.get(url=contrib_stats_url)
#
#    if not contrib_stats_resp.ok:
#        print('Rate limit probably reached')
#        sys.exit(123)
#
#    contrib_stats = contrib_stats_resp.json()
#
#    for author in stats:
#        repo_contributions_last_year[repo] += week['total']
#        week_id = week['week']
#        if weekly_contributions.get(week_id):
#            weekly_contributions[week_id] += week['total']
#        else:
#            weekly_contributions[week_id] = week['total']
#

    # Report
print('#############################################################################################')

print('Contributors per repo:')
for repo in repo_contributors:
    print('\tRepo: {}, contributors: {}'.format(repo, repo_contributors[repo]))

print('#############################################################################################')

print('Contributions per repo:')
for repo in repo_contributions:
    print('\tRepo: {}, contributions: {}'.format(repo, repo_contributions[repo]))

print('#############################################################################################')

print('Number of Unique Contributors is: {}'.format(len(unique_contributors)))
print('Unique contributors are: ')
for uc in unique_contributors:
    print('\tUsername: {}'.format(uc))

print('#############################################################################################')

print("Number of Total Commits is: {}".format(total_contributions))

print('#############################################################################################')

print('Contributions per repo in Last Year')
for repo in repo_contributions_last_year:
    print('\tRepo: {}, contributions: {}'.format(repo, repo_contributions_last_year[repo]))

print('#############################################################################################')

print('Weekly contributions:')
for week in sorted(weekly_contributions.keys()):
    if weekly_contributions[week] != 0:
        print("\t{} | {}".format(datetime.datetime.fromtimestamp(week).strftime('%Y-%m-%d'), weekly_contributions[week]))

print('#############################################################################################')
