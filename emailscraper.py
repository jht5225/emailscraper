import imaplib, email, os
from email.header import decode_header
from emailobj import Email

class EmailScraper:
    def __init__(self, username, password, imap='imap.gmail.com'):
        # Establish connection to email account
        self.username = username
        self.password = password
        self.imap = imap
        self.init_connection()

        # Init member vars 
        self.raw_emails_from = {}
        self.processed_emails_from = {}

    def init_connection(self):
        self.con = imaplib.IMAP4_SSL(self.imap)
        self.con.login(self.username, self.password)
        self.con.select('Inbox')
    
    def search(self, key, val):
        result, data = self.con.search(None, key, '"{}"'.format(val))
        return data
    
    def add_sender(self, sender=None):
        if sender is None:
            sender = self.email_from
        if sender not in self.raw_emails_from:
            self.raw_emails_from[sender] = []
        if sender not in self.processed_emails_from:
            self.processed_emails_from[sender] = []

    def get_raw_emails(self,sender=None):
        if sender is None:
            sender = self.email_from
        if sender not in self.raw_emails_from:
            search_from = self.search('FROM', sender)
            self.raw_emails_from[sender] = []
            for num in search_from[0].split():
                typ, data = self.con.fetch(num, '(RFC822)')
                self.raw_emails_from[sender].append(data)

    def update_raw_emails(self, sender=None):
        if sender is None:
            sender = self.email_from
        

    def find_emails_from(self, email_from):
        self.email_from = email_from
        self.get_raw_emails()
        for raw_emails in self.raw_emails_from[email_from]:
            for raw_email in raw_emails:
                if type(raw_email) is tuple:
                    self.processed_emails_from[email_from] = Email(raw_email)

    def get_emails_from(self, email_from):
        if email_from not in self.processed_emails_from:
            self.find_emails_from(email_from)
        return self.processed_emails_from[email_from]


    


        