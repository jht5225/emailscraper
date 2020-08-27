import imaplib, email

class EmailScrapper:
    def __init__(self, username, password, imap='imap.gmail.com'):
        self.username = username
        self.password = password
        self.imap = imap
        init_connection()

    def init_connection(self):
        self.con = imaplib.IMAP4_SSL(self.imap)
        self.con.login(self.username, self.password)
        self.con.select('Inbox')
    
    def search(self, key, val):
        result, data = self.con.search(None, key, '"{}"'.format(value))
        return data

    def find_body(self):
        if self.msg.is_multipart():
            self.msg = self.msg.get_payload(0)
            self.get_body()
        else: 
            self.body = self.msg.get_payload(None, True)
    
    def find_messages_from(self, email_from):
        search_from = self.search('FROM', email_from)
        self.msgs = []
        for num in search_from[0].split():
            typ, data = self.con.fetch(num, '(RFC822)')
            self.msgs.append(data)





        