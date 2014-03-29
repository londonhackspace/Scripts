#!/usr/bin/env python
import re
import simplejson as json
import socket
import requests

LASTIDFILE = '/usr/local/bin/Scripts/wikilastid.txt'

def ellipsize(s, maxlen=80):
    if len(s) > maxlen:
        # + 1 in case it cuts perfectly at a word boundary
        end = s.rfind(' ', 0, maxlen - len('...') + 1)
        s = s[:end]

        # Fix letters that look bad before an ellipsis
        if s[-1] in (' .,;:-+=&?!'):
            s += ' ' # Yes, I know this breaks MAXLEN

        s += '...'
    return s


with open(LASTIDFILE) as f:
    last_id = int(f.read())

params = {
    'action':       'query',
    'prop'  :       'revisions',
    'generator':    'recentchanges',
    'grcnamespace': '0|1',
    'grcshow':      '!bot|!minor',
    'grclimit':     50,
    'format':       'json',
}

r = requests.get('https://wiki.london.hackspace.org.uk/w/api.php', params=params, verify=False)
data = json.loads(r.text)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))

max_id = last_id
for page_no, page in data['query']['pages'].items():
    if int(page_no) < 0:
        # missing page
        continue

    rev = page['revisions'][0]
    rev_id = int(rev['revid'])

    if rev.has_key('minor'):
        # grcshow doesn't seem to work
        continue

    if rev_id <= last_id:
        # should already have been shown
        continue

    max_id = max(rev_id, max_id)

    title = page['title']
    user = rev['user']
    comment = rev['comment']

    msg = []
    msg.append(u'#london-hack-space-dev {0} changed {1}'.format(user, title))
    if comment:
        # Format section like the mediawiki history page
        comment = re.sub(r'(?:/\* *(.*?) *\*/) *(.*) *', ur'\2 \u2192\1', comment)
        msg.append(u'({0})'.format(ellipsize(comment.strip(), 40)))

    msg.append('http://hack.rs/w/?diff={0}\r\n'.format(rev_id))
    msg = ' '.join(msg)
    s.send(msg.encode('utf-8'))

if max_id > last_id:
    with open(LASTIDFILE, 'w') as f:
        f.write(str(max_id))

s.close()

