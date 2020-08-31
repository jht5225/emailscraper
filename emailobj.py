import imaplib, email, os
from email.header import decode_header

class Email:
    def __init__(self, raw_email):
        self.msg = email.message_from_bytes(raw_email)
        self.has_attachments = False
        self.parse_email()
    
    def __str__(self):
        email_string = "Subject: " + self.subject + "\n Recieved at: " + self.time + " \n Has attachments: " + str(self.has_attachments)
        if self.email_from:
            email_string = "Email from " + self.email_from + '\n' + email_string
        return email_string
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        
        return self.time == other.time and self.email_from == other.email_from and self.subject == other.subject

    def parse_email(self):
        self.parse_email_header()
        self.parse_email_from()
        self.parse_email_time()
        self.parse_email_body()

    def parse_email_header(self):
        subject = decode_header(self.msg["Subject"])[0][0]
        if type(subject) is bytes:
            subject = subject.decode('UTF-8')
        self.subject = subject
    
    def parse_email_from(self):
        email_from = self.msg.get('from', [])
        self.email_from = email_from

    def parse_email_time(self):
        self.time = self.msg['Date']

    def parse_email_body(self):
        self.body = []
        if self.msg.is_multipart():
            self.handle_multipart()
        else:
            self.body.append(self.parse_body_part())

    def handle_multipart(self):
        for part in self.msg.walk():
            self.body.append(self.parse_body_part(part))

    def make_part_dict(self, part_type, part):
        return {"type": part_type, "content": part}

    def parse_body_part(self, part=None):
        if part is None:
            part = self.msg
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        error = False
        try:
            body = part.get_payload(decode=True).decode()
        except:
            error = True
            body = "Could not parse"
        if "attachment" in content_disposition:
            self.has_attachments = True
            return self.handle_attachment(part)
        elif content_type in "text/html":
            return self.make_part_dict("html", body)
        elif content_type == 'text/plain':
            return self.make_part_dict("text", body)
        elif error:
            return self.make_part_dict("Error", "Could not parse")
        else: 
            return self.make_part_dict("other", body)
    
    def handle_attachment(self, part):
        filename = part.get_filename()
        if filename:
            if not os.path.isdir(self.email_from):
                os.mkdir(self.email_from)
            filepath = os.path.join(self.email_from, filename)
            open(filepath, 'wb').write(part.get_payload(decode=True))
            return self.make_part_dict("attachment", "filepath")
        else:
            return self.make_part_dict("attchment", "Could not load")

    def get_time(self):
        return self.time

    def get_subject(self):
        return self.subject
    
    def get_body(self):
        return self.body

    def get_text_content(self):
        text_content = []
        for part in self.body:
            if part['type'] == "text" or part['type'] == "html":
                text_content.append(part)
        return text_content
    
    def get_attachments(self):
        attachments = []
        for part in self.body:
            if part['type'] == "attachment" or part['type'] == "other":
                attachments.append(part)
        return attachments
    
    def recieved_from(self, sender):
        if sender in self.email_from:
            return True
        else:
            return False
                