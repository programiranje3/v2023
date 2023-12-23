from datetime import datetime
from random import randint
from sys import stderr
import json_tricks
from pathlib import Path

class Post:

    dt_format = "%d-%m-%Y %H:%M:%S"

    def __init__(self, username, content):
        self.username = username
        self.content = content
        self.timestamp = datetime.now()
        self.id = randint(100000, 1000000)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if (isinstance(value, str) and len(value) >= 4 and
                value[0].isalpha() and all([ch.isalnum() for ch in value[1:]])):
            self.__username = value
        else:
            self.__username = None
            raise RuntimeError(f"Input argument ({value}) for username setter is invalid -> cannot set username\n")

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value):
        if isinstance(value, datetime) and value <= datetime.now():
            self.__timestamp = value
            return
        if isinstance(value, str):
            try:
                value_dt = datetime.strptime(value, Post.dt_format)
            except ValueError:
                stderr.write(f"Incorrect input for timestamp attribute ({value}). Excepted format {Post.dt_format}\n")
                return
            else:
                if value_dt <= datetime.now():
                    self.__timestamp = value_dt
                else:
                    stderr.write(f"Incorrect input, the date and time should not be a moment in the future\n")

    def __str__(self):
        post_str = f"Post ID={self.id}\n"
        post_str += f"by user: {self.username if self.username else 'unknown'}\n"
        post_str += f"content: {self.get_content_str()}\n"
        post_str += f"timestamp: {datetime.strftime(self.timestamp, Post.dt_format)}"
        return post_str


    def get_content_str(self):
        words = self.content.split()
        return self.content if len(words) <= 10 else (" ".join(words[:10]) + "...")


class Question(Post):

    def __init__(self, title, tags=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.tags = tags if tags else list()
        self.responses = list()

    def __str__(self):
        post_str = super().__str__()
        lines = post_str.split('\n')
        lines[0] = lines[0].replace('Post', 'Question')
        lines.insert(2, f"title: {self.title}")
        lines.append(f"tags: {', '.join(self.tags) if len(self.tags) > 0 else 'none'}")
        lines.append(f"responses: {self.get_responses_as_str()}")
        return '\n'.join(lines)

    def get_responses_as_str(self):
        return ('\n' + "\n".join([str(r) for r in self.responses])) if len(self.responses) > 0 else 'none yet'


    # %d/%m/%Y
    def generate_response_sequence(self, date):
        selected_responses = None
        try:
            dt = datetime.strptime(date, '%d/%m/%Y')
            selected_responses = [response for response in self.responses if response.timestamp > dt]
            if len(selected_responses) == 0:
                stderr.write("No response arrived after the given date -> will use the available responses\n")
                selected_responses = self.responses
        except ValueError:
            stderr.write(f"The input date ({date}) is not in the expected format (%d/%m/%Y)\n. Will use all responses\n")
            selected_responses = self.responses

        selected_responses.sort(key=lambda r: r.votes, reverse=True)

        for response in selected_responses:
            yield response


class Answer(Post):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = 0
        self.accepted = False

    def __str__(self):
        post_str = super().__str__() + '\n'
        post_str = post_str.replace("Post", "Answer")
        post_str += f"votes: {self.votes}\n"
        post_str += f"accepted: {'yes' if self.accepted else 'no'}"
        return post_str

    @property
    def accepted(self):
        return self.__accepted

    @accepted.setter
    def accepted(self, value):
        if isinstance(value, bool):
            self.__accepted = value
        else:
            raise ValueError(f"Invalid input value ({value}) for the accepted attribute\n")


def questions_to_json(questions, fpath):
    try:
        with open(fpath, 'w') as fobj:
            json_tricks.dump(questions, fobj, indent=4)
    except OSError as err:
        stderr.write(f"OS error occurred when trying to serialise questions to json file:\n{err}\n")


def from_json(fpath):
    try:
        with open(fpath, 'r') as fobj:
            return json_tricks.load(fobj, cls_lookup_map=globals())
    except OSError as err:
        stderr.write(f"OS error occurred when trying to deserialise questions from json file {fpath}:\n{err}\n")
        return None


if __name__ == '__main__':

    p1 = Post('user1', 'Can you recommend me a good tutorial on classes and inheritance in python?')
    # print(p1)
    # print()

    q1 = Question(username='user1',
                  content="How to extract date time from a string value? Is there a function for that?",
                  title='Extracting datetime from string',
                  tags=['datetime', 'string'])

    q2 = Question(username='user2',
                  content='What is the simplest way to write objects to a json file?',
                  title='Serialisation to json',
                  tags=['json', 'serialisation'])

    a1 = Answer(username='user3',
                content='You can use strptime function from the datetime module')

    a2 = Answer(username='user4',
                content='You can try searching for a method in the datetime or date module, there should something for parsing')

    a1.votes = 5
    a1.accepted = True

    a2.votes = 2

    q1.responses.extend([a1, a2])

    # print(q1)
    # print()
    #
    # print(q2)
    # print()

    # g = q1.generate_response_sequence('24/12/2023')
    # for response in g:
    #     print(response)

    # serialising questions to a json file
    questions_to_json([q1, q2], Path.cwd() / 'questions.json')

    # deserialising questions from a json file and printing them
    questions = from_json(Path.cwd() / 'questions.json')
    if questions:
        for q in questions:
            print(q)
            print()