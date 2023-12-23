from jun2021 import *

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