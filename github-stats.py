import datetime
import functools
import pprint
import requests
import sys

REPOS = [
    'hyperledger/indy-node',
    'hyperledger/indy-sdk',
    'hyperledger/indy-plenum',
    'hyperledger/indy-hipe',
    'hyperledger/indy-crypto',
    'hyperledger/indy-anoncreds',
    'hyperledger/indy-agent',
    'hyperledger/indy-post-install-automation',
    'hyperledger/indy-jenkins-pipeline-lib',
    'hyperledger/indy-test-automation',
    'hyperledger/ursa',
    'hyperledger/ursa-rfcs',
    'bcgov/von',
    'bcgov/von-network',
    'bcgov/TheOrgBook',
    'bcgov/von-bc-registries-agent',
    'bcgov/von-personal-agent',
    'bcgov/permitify',
    'bcgov/von-connector',
    'bcgov/von-ledger-explorer',
    'sovrin-foundation/Responsible-Disclosure-Deep-Learning-Fingerprinting-Attack',
    'sovrin-foundation/libsovtoken',
    'sovrin-foundation/cloudconfigs',
    'sovrin-foundation/saltstack',
    'sovrin-foundation/steward-tools',
    'sovrin-foundation/token-plugin',
    #'sovrin-foundation/sov-docs-conf',
    'sovrin-foundation/ledger-monitoring-server',
    'sovrin-foundation/jenkins-shared',
    'sovrin-foundation/sovrin',
    'sovrin-foundation/community-tools',
    'sovrin-foundation/aws-codebuild-pipeline-plugin',
    'sovrin-foundation/sovrin-packaging',
    'sovrin-foundation/connector-app',
    'sovrin-foundation/vc-data-model',
    'sovrin-foundation/sovrin-sip',
    'sovrin-foundation/sovrin-test-automation',
    'sovrin-foundation/sshuttle-helper',
    'sovrin-foundation/protocol',
    'sovrin-foundation/agent-sdk',
    'sovrin-foundation/sovrin_bot',
    'sovrin-foundation/sovrin-connector-preview',
    'sovrin-foundation/pipeline-test',
    'sovrin-foundation/ssi-protocol',
    'sovrin-foundation/sovrin.org',
    'sovrin-foundation/launch',
    'sovrin-foundation/old-sovrin',
    'sovrin-foundation/sovrin-agent',
    'sovrin-foundation/sovrin-client-c',
    'sovrin-foundation/rust-curvecp-poc'
]

username = sys.argv[1]
token = sys.argv[2]

stats = {
    'unique_contributors': {},
    'weekly_contributions': {},
    'total_contributions': 0
}

for repo in REPOS:
    print('Working on {}'.format(repo))
    stats[repo] = {
        'contributions_last_year': 0,
        'contributors': 0,
        'contributions': 0
    }

    # STATS
    stats_url = 'https://api.github.com/repos/{}/stats/commit_activity'.format(repo)

    stats_resp = requests.get(url=stats_url, auth=(username, token))
    if not stats_resp.ok:
        print('Encountered error: ', stats_resp.status_code)
        print(stats_resp.json())
        sys.exit(1)

    stats_resp = stats_resp.json()

    for week in stats_resp:
        stats[repo]['contributions_last_year'] += week['total']
        unix_week = week['week']
        if unix_week in stats['weekly_contributions']:
            stats['weekly_contributions'][unix_week]['total'] += week['total']
        else:
            stats['weekly_contributions'][unix_week] = {
                'total': week['total'],
                'contributors': set(),
                'first_time_contributors': set()
            }


    # CONTRIBUTIONS
    contrib_url = 'https://api.github.com/repos/{}/contributors'.format(repo)

    head_resp = requests.head(url=contrib_url, auth=(username, token))

    if not head_resp.ok:
        print('Encountered error:', head_resp.status_code)
        print(head_resp)
        sys.exit(1)

    link_header = head_resp.headers.get('link')
    if link_header:
        last_page = link_header.split(';')[1][-2:-1]
    else:
        last_page = 1

    for x in range(1, int(last_page)+1):
        params = {'page': x}
        contributors_resp = requests.get(url=contrib_url, params=params, auth=(username, token))
        contributors = contributors_resp.json()

        for contributor in contributors:
            stats[repo]['contributors'] += 1
            if contributor['login'] not in stats['unique_contributors']:
                stats['unique_contributors'][contributor['login']] = {
                    'contributor': contributor['login'],
                    'total_contributions': contributor['contributions'],
                    'contributes_to': [repo],
                    'weeks': []
                }
            else:
                stats['unique_contributors'][contributor['login']]['total_contributions'] += \
                        contributor['contributions']
                stats['unique_contributors'][contributor['login']]['contributes_to'].append(repo)
            stats['total_contributions'] += contributor['contributions']
            stats[repo]['contributions'] += contributor['contributions']

    # CONTRIBUTORS
    contrib_stats_url = 'https://api.github.com/repos/{}/stats/contributors'.format(repo)

    contrib_stats_resp = requests.get(url=contrib_stats_url, auth=(username, token))

    if not contrib_stats_resp.ok:
        print('Encountered err:', contrib_stats_resp.status_code)
        print(contrib_stats_resp.json())
        sys.exit(1)

    contrib_stats = contrib_stats_resp.json()
    for contrib in contrib_stats:
        stats['unique_contributors'][contrib['author']['login']]['weeks'] += contrib['weeks']

def weeks_reduce(acc, week):
    if week['a'] > 0 or week['c'] > 0 or week['d'] > 0:
        acc.append(week['w'])
    return acc

def contrib_week_reduce(acc, contrib):
    weeks = sorted(functools.reduce(weeks_reduce, contrib['weeks'], []))
    del contrib['weeks']
    if not weeks:
        return acc

    for week in weeks:
        if week not in acc:
            acc[week] = {
                'total': 0,
                'contributors': set(),
                'first_time_contributors': set()
            }

        acc[week]['contributors'].add(contrib['contributor'])

    acc[weeks[0]]['first_time_contributors'].add(contrib['contributor'])

    return acc

functools.reduce(contrib_week_reduce, stats['unique_contributors'].values(), stats['weekly_contributions'])

# Report
print('#############################################################################################')

print('Contributors per repo:')
for repo in REPOS:
    print('\tRepo: {}, contributors: {}'.format(repo, stats[repo]['contributors']))

print('#############################################################################################')

print('Contributions per repo:')
for repo in REPOS:
    print('\tRepo: {}, contributions: {}'.format(repo, stats[repo]['contributions']))

print('#############################################################################################')

print('Number of Unique Contributors is: {}'.format(len(stats['unique_contributors'].keys())))
print('Unique contributors are: ')
for uc in stats['unique_contributors'].values():
    print('\tUsername: {}'.format(uc['contributor']))

print('#############################################################################################')

print("Number of Total Commits is: {}".format(stats['total_contributions']))

print('#############################################################################################')

print('Contributions per repo in Last Year')
for repo in REPOS:
    print('\tRepo: {}, contributions: {}'.format(repo, stats[repo]['contributions_last_year']))

print('#############################################################################################')

print('Weekly contributions | contributors added:')
for week, data in sorted(stats['weekly_contributions'].items()):
    if data['total'] != 0:
        print("\t{} | {} | {} | {}".format(
            datetime.datetime.fromtimestamp(week).strftime('%Y-%m-%d'),
            data['total'],
            len(data['first_time_contributors']),
            data['first_time_contributors']
        ))
        #print("\t{} | {} | {} | {}".format(datetime.datetime.fromtimestamp(week).strftime('%Y-%m-%d'), weekly_contributions[week][0], weekly_contributions[week][1], weekly_contributions[week][2]))

print('#############################################################################################')

# Print all the things
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)
