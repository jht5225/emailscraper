import imaplib, email, os
from email.header import decode_header

class Email:
    def __init__(self, raw_email, email_from=None, email_to=None):
        self.msg = email.message_from_bytes(raw_email[1])
        self.email_from = email_from
        self.email_to = email_to
        self.parse_email_header()
        self.parse_email_body()
    
    def __str__(self):
        email_string = "subject: " + self.subject + "\n body: \n" + self.body 
        if self.email_from:
            email_string = "from: " + self.email_from + "\n" + email_string
        if self.email_to:
            email_string = "to: " + self.email_to + "\n" + email_string
        return email_string
    def parse_email_header(self):
        subject = decode_header(self.msg["Subject"])[0][0]
        if type(subject) is bytes:
            subject = subject.decode('UTF-8')
        self.subject = subject

    def parse_email_body(self):
        if self.msg.is_multipart():
            self.handle_multipart()
        else:
            self.body = self.parse_body_part()
    
    def handle_multipart(self):
        self.body = []
        self.attachments = []
        for part in self.msg.walk():
            self.body.append(self.parse_body_part(part))

    def parse_body_part(self, part=None):
        if part is None:
            part = self.msg
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        try:
            body = part.get_payload(decode=True).decode()
        except:
            pass
        
        if "attachment" in content_disposition:
            self.attachments.append(part)
        else:
            return body