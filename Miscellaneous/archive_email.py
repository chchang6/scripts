#!/usr/bin/env python
# Script to archive folders of e-mail from an IMAP-compatible provider
#   Tuned for GMX.

import imaplib
import ssl
import re, datetime

RE1 = re.compile('Date: \w{3}, (?P<day>[0-9]{1,2})(?P<rest> \w{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} [+-][0-9]{4})')

def connect_imap_server(user_email, user_password, imap_server_domain):
    print('Connecting to IMAP server')
    imaplib.IMAP4.debug=1
    tls_context = ssl.create_default_context()
    imap_server = imaplib.IMAP4_SSL(imap_server_domain, ssl_context=tls_context, timeout=10)
    print('Logging in...')
    imap_server.login(user_email, user_password)
    return imap_server

def close_imap_server_connection(imap_server):
    imap_server.close()
    imap_server.logout()
    imap_server = None
    return

def get_mailbox_list(imap_server):
    # Print list of mailboxes on server
    code, mailboxes = imap_server.list()
    for mailbox in mailboxes:
        print(mailbox.decode("utf-8"))
    return

def query_folder(imap_server, mailbox):
    # Select mailbox
    imap_server.select(mailbox, readonly=True)
    t, msgindices = imap_server.search(None, 'ALL')
    for i in msgindices[0].split():
        t, msg = imap_server.fetch(i, '(UID BODY[HEADER.FIELDS (Date)])')
        t = RE1.search(str(msg[0][1]))
        if len(t.group('day')) == 1:
            day = '0' + t.group('day')
        else:
            day = t.group('day')
        timestamp = datetime.datetime.strptime(day + t.group('rest'), '%d %b %Y %H:%M:%S %z')
        filename = datetime.datetime.strftime(timestamp, '%Y%m%d_%H%M%S.eml')
        t, msg = imap_server.fetch(i, '(RFC822)')
        with open(filename, 'wb') as f:
           f.write(msg[0][1])
    return

user_email = ''  # E-mail address
user_password = input('Please enter password: ')  # App password
imap_server_domain = 'imap.gmx.com'
imap_server = connect_imap_server(user_email, user_password, imap_server_domain)
# Use following command to print list of mailboxes. Either this or next two commands active.
#get_mailbox_list(imap_server)
# Following two commands are run together. If just getting mailbox list, no need to close.
query_folder(imap_server, '"path to/target/mailbox"')
close_imap_server_connection(imap_server)

