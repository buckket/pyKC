import json


class Post(object):

    def __init__(self, id, level, cb, posterinfo, name, tripcode, subject, text, files, sage, ban, date):
        self.id = id
        self.level = level
        self.cb = cb
        self.posterinfo = posterinfo
        self.name = name
        self.tripcode = tripcode
        self.subject = subject
        self.text = text
        self.files = files
        self.sage = sage
        self.ban = ban
        self.date = date

    def to_safe_dict(self):
        post = self.__dict__.copy()

        # Enum needs special handling.
        post['level'] = int(post['level'])

        return post

    def to_json(self):
        return json.dumps(self.to_safe_dict())
