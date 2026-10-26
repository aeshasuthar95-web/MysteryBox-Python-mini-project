"""
data/exam.py - case: The Leaked Exam Paper

One case = story, culprit, places, suspects, clues and final questions.
See data/__init__.py for an explanation of every field.
"""

CASE = {
    "title": "The Leaked Exam Paper",
    "story": "Sunrise College, Friday 7:30 PM. Tomorrow is the final Computer "
             "Science exam. But the question paper is gone from the locked "
             "cupboard in Room 204, and a photo of it is already in a student "
             "chat group! You are Detective Sam. Find who did it before "
             "the exam starts!",
    "culprit": "kiran",
    "locations": {
        "room204": "Room 204 (Exam Room)",
        "lab": "Computer Lab",
        "office": "College Office",
        "library": "Library",
        "canteen": "Canteen",
    },
    "suspects": {
        "mehta": {
            "name": "Prof. Mehta", "role": "Exam Head",
            "intro": "Strict teacher. He wrote the paper himself.",
            "testimony": [
                {"id": "p1", "requires": [],
                 "text": "I locked the paper in the cupboard at 5:00 PM. "
                         "I wrote every question myself.",
                 "unlocks": None},
                {"id": "p2", "requires": ["minutes"],
                 "text": "Yes, I was in the staff meeting. I only wish to protect "
                         "the hard work of the students.",
                 "unlocks": None},
            ],
        },
        "neel": {
            "name": "Neel", "role": "Office Clerk",
            "intro": "Looks after all the keys and papers.",
            "testimony": [
                {"id": "o1", "requires": [],
                 "text": "I only look after papers and keys. I sat at my desk until 7 PM.",
                 "unlocks": None},
                {"id": "o2", "requires": ["lock"],
                 "text": "My key never left my pocket. Check the key register to see "
                         "who used the third key.",
                 "unlocks": "neel_tip"},
            ],
        },
        "kiran": {
            "name": "Kiran", "role": "Lab Assistant",
            "intro": "Quiet and always helpful in the lab.",
            "testimony": [
                {"id": "k1", "requires": [],
                 "text": "I was fixing computers in the lab all evening.",
                 "unlocks": None},
                {"id": "k2", "requires": ["keybook"],
                 "text": "Yes, I took the Room 204 key to fix the projector. "
                         "It took me one hour.",
                 "unlocks": None},
                {"id": "k3", "requires": ["projector"],
                 "text": "(he looks away) Maybe the projector was fine... "
                         "I do not remember why I went there.",
                 "unlocks": None},
            ],
        },
        "dev": {
            "name": "Dev", "role": "Class Topper",
            "intro": "Always first in class. He looks tired.",
            "testimony": [
                {"id": "d1", "requires": [],
                 "text": "I studied all evening. A leak is unfair to students who "
                         "work hard!",
                 "unlocks": None},
                {"id": "d2", "requires": ["studylog"],
                 "text": "Yes, I was in the library. Ask the librarian if you "
                         "do not believe me.",
                 "unlocks": None},
            ],
        },
        "sara": {
            "name": "Sara", "role": "Class Representative",
            "intro": "Runs the class chat group.",
            "testimony": [
                {"id": "s1", "requires": [],
                 "text": "I run the class chat group, but I only share notes there.",
                 "unlocks": None},
                {"id": "s2", "requires": ["labpc"],
                 "text": "The first photo came from an unknown number at 6:20 PM. "
                         "It was not a student from our class.",
                 "unlocks": "sara_tip"},
            ],
        },
    },
    "clues": {
        "lock": {"place": "room204", "requires": [],
                 "text": "The cupboard lock is not broken. Someone opened it with a real key."},
        "labcap": {"place": "room204", "requires": ["lock"],
                   "text": "A blue pen cap with the words 'Comp Lab' on it lies under the cupboard."},
        "projector": {"place": "room204", "requires": ["keybook"],
                      "text": "The projector in Room 204 works perfectly. Nobody needed to fix it."},
        "keybook": {"place": "office", "requires": ["neel_tip"],
                    "text": "Key register: Prof. Mehta and Neel kept their own keys. The third key was signed out by Kiran at 5:30 PM 'to fix the projector' and returned at 6:30 PM."},
        "minutes": {"place": "office", "requires": [],
                    "text": "Meeting notes: Prof. Mehta was in the staff meeting from 5:30 to 7:00 PM."},
        "labpc": {"place": "lab", "requires": [],
                  "text": "Lab PC 7 was used at 6:20 PM. Its history shows a photo was sent to a chat group."},
        "labdoor": {"place": "lab", "requires": ["labpc"],
                    "text": "Lab door card log: Kiran's card opened the lab at 6:10 PM. Nobody else came in until 7:00 PM."},
        "studylog": {"place": "library", "requires": [],
                     "text": "Library sign-in sheet: Dev studied here from 5:00 to 8:00 PM."},
        "canteenbill": {"place": "canteen", "requires": [],
                        "text": "The canteen owner's notebook: Kiran owes 6,000 rupees for food and tea. 'Pay by Monday' is written next to his name."},
        "rumour": {"place": "canteen", "requires": ["sara_tip"],
                   "text": "A student whispers: 'The person who sold me the paper wore a lab coat and wanted 500 rupees.'"},
        "neel_tip": {"place": None, "requires": [],
                     "text": "Neel says the key register will show who used the third key."},
        "sara_tip": {"place": None, "requires": [],
                     "text": "Sara says the first photo of the paper came from an unknown number at 6:20 PM."},
    },
    "questions": [
        {"question": "How was the cupboard opened?",
         "options": ["With a real key", "With a hammer",
                     "With a secret code", "By breaking the lock"],
         "answer": "With a real key"},
        {"question": "What was found under the cupboard?",
         "options": ["A blue pen cap from the Computer Lab", "A red student card",
                     "A torn exam page", "A mobile phone"],
         "answer": "A blue pen cap from the Computer Lab"},
        {"question": "Why did Kiran say he took the Room 204 key?",
         "options": ["To fix the projector", "To clean the room",
                     "To meet Prof. Mehta", "To water the plants"],
         "answer": "To fix the projector"},
        {"question": "What did you find out about the projector?",
         "options": ["It worked perfectly", "It was broken",
                     "It was missing", "It was very old"],
         "answer": "It worked perfectly"},
        {"question": "At what time was the photo sent from Lab PC 7?",
         "options": ["4:00 PM", "6:20 PM", "8:30 PM", "10:00 PM"],
         "answer": "6:20 PM"},
        {"question": "Whose card opened the Computer Lab door at 6:10 PM?",
         "options": ["Kiran's", "Dev's", "Sara's", "Neel's"],
         "answer": "Kiran's"},
        {"question": "Where was Dev from 5:00 to 8:00 PM?",
         "options": ["In the library", "In the canteen", "In Room 204", "In the lab"],
         "answer": "In the library"},
        {"question": "Who told you to check the key register?",
         "options": ["Neel the clerk", "Sara the class representative",
                     "Dev the topper", "Prof. Mehta"],
         "answer": "Neel the clerk"},
        {"question": "What did the canteen owner's notebook say about Kiran?",
         "options": ["He owes 6,000 rupees and must pay by Monday",
                     "He won a prize",
                     "He is a new student",
                     "He never eats there"],
         "answer": "He owes 6,000 rupees and must pay by Monday"},
        {"question": "Where was Prof. Mehta from 5:30 to 7:00 PM?",
         "options": ["In a staff meeting", "In the lab", "In the library", "At home"],
         "answer": "In a staff meeting"},
    ],
}
