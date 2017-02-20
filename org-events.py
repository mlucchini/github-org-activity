from github import Github
import os
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s organization' % sys.argv[0])

organization_name = sys.argv[1]
only_members = []
token = os.getenv('GITHUB_API_TOKEN')

if token is None:
    sys.exit('You must specify a GITHUB_API_TOKEN environment variable. ' +
             'Generate a token at: "https://github.com/settings/tokens".')

g = Github(token)
organization = g.get_organization(organization_name)
members = [m for m in organization.get_members() if len(only_members) == 0 or m.login in only_members]
events = [e for m in members for e in m.get_events()]

events.sort(key=lambda e: e.created_at)
for e in events:
    print("%s: %s %s on %s" % (e.created_at, e.actor.login, e.type, e.repo.name))
