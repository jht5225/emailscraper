import imaplib, email, os, time
from email.header import decode_header
from emailobj import Email

class Mailbox:
    def __init__(self, username, password, imap='imap.gmail.com'):
        # Establish connection to email account
        self.username = username
        self.password = password
        self.imap = imap
        self.__init_connection()
        
        # Init emails 
        self.emails = []
        self.new_emails = []
        self.__add_emails()

    def __init_connection(self):
        self.con = imaplib.IMAP4_SSL(self.imap)
        self.con.login(self.username, self.password)
        self.con.select('Inbox',False)

    def __search(self, key, val):
        result, data = self.con.search(None, key, '"{}"'.format(val))
        return data

    def __add_emails(self):
        typ, ids = self.con.uid('search',None, 'ALL')
        ids = ids[0].decode().split()
        for id in ids:
            typ, raw_email = self.con.uid('fetch', id, '(RFC822)')
            new_email = Email(raw_email[0][1])

            if new_email not in self.emails:
                self.emails.append(new_email)
                self.new_emails.append(new_email)
        # self.__delete_old_emails()

    def __delete_old_emails(self):
        typ,data = self.con.search(None, 'ALL')
        for num in data[0].split():
            self.con.store(num, '+FLAGS', '\\Deleted')


    def get_emails_from(self, sender):
        emails = []
        for mail in self.emails:
            if mail.recieved_from(sender):
                emails.append(mail)
        return emails

    def get_all_emails(self):
        return self.emails

    def update(self):
        self.new_emails = []
        self.__add_emails()
        new_num_emails = len(self.new_emails)
        print("You have " + str(new_num_emails) + " new emails")
        return self.new_emails


        

    


        