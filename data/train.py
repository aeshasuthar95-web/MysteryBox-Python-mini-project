"""
data/train.py - case: The Night Train Necklace

One case = story, culprit, places, suspects, clues and final questions.
See data/__init__.py for an explanation of every field.
"""

CASE = {
    "title": "The Night Train Necklace",
    "story": "Night Express, 11:00 PM. Mrs. Kapoor's gold necklace is gone from "
             "her cabin while the train runs between two stations! The door was "
             "locked the whole time. You are Detective Sam. "
             "Find the thief before the train reaches the last station!",
    "culprit": "joe",
    "locations": {
        "cabin": "Cabin 4",
        "corridor": "Train Corridor",
        "dining": "Dining Car",
        "luggage": "Luggage Van",
        "guard": "Guard's Room",
    },
    "suspects": {
        "joe": {
            "name": "Joe", "role": "Ticket Checker",
            "intro": "Checks every ticket and walks the whole train.",
            "testimony": [
                {"id": "t1", "requires": [],
                 "text": "I walked the whole train all night checking tickets. "
                         "Nothing strange happened.",
                 "unlocks": None},
                {"id": "t2", "requires": ["keylist"],
                 "text": "Yes, I have a master key, but I never used it tonight.",
                 "unlocks": None},
                {"id": "t3", "requires": ["handle"],
                 "text": "(he hides his hands) Blue ink? I stamp tickets all day. "
                         "It is everywhere!",
                 "unlocks": None},
            ],
        },
        "bella": {
            "name": "Bella", "role": "Mrs. Kapoor's Maid",
            "intro": "She looks tired and worried.",
            "testimony": [
                {"id": "e1", "requires": [],
                 "text": "I was in the dining car with a cup of tea. "
                         "I never went near Cabin 4.",
                 "unlocks": None},
                {"id": "e2", "requires": ["keylist"],
                 "text": "Yes, I have a spare key, but it was in my bag all night. "
                         "Ask Lily.",
                 "unlocks": None},
            ],
        },
        "lily": {
            "name": "Lily", "role": "Dining Car Waitress",
            "intro": "Serves food and remembers every guest.",
            "testimony": [
                {"id": "l1", "requires": [],
                 "text": "It was a very busy night in the dining car.",
                 "unlocks": None},
                {"id": "l2", "requires": ["keylist"],
                 "text": "Bella sat at table 7 from 10 to 11 PM. She drank three "
                         "cups of tea and talked a lot.",
                 "unlocks": "lily_tip"},
            ],
        },
        "arjun": {
            "name": "Arjun", "role": "Young Magician",
            "intro": "Travelling to a big show. Fast, clever hands.",
            "testimony": [
                {"id": "a1", "requires": [],
                 "text": "A magician never tells his secrets. But I never steal!",
                 "unlocks": None},
                {"id": "a2", "requires": ["props"],
                 "text": "My gold chains are fake. They are only toys for my show.",
                 "unlocks": None},
            ],
        },
        "sen": {
            "name": "Mr. Sen", "role": "Businessman",
            "intro": "Travels with a very heavy bag.",
            "testimony": [
                {"id": "n1", "requires": [],
                 "text": "I was in Cabin 6 all night, reading my papers.",
                 "unlocks": None},
                {"id": "n2", "requires": ["keylist"],
                 "text": "Now I remember: at about 10:30 PM I saw Joe near Cabin 4 "
                         "with a key in his hand. I thought he was checking the door.",
                 "unlocks": "sen_witness"},
            ],
        },
    },
    "clues": {
        "lockok": {"place": "cabin", "requires": [],
                   "text": "Cabin 4's door was locked and the lock is not broken. The thief used a key."},
        "emptybox": {"place": "cabin", "requires": ["lockok"],
                     "text": "Only the jewelry box is empty. The thief knew exactly where the necklace was."},
        "dnd": {"place": "corridor", "requires": [],
                "text": "A 'Do Not Disturb' sign hangs on Cabin 4's door. Nobody should have knocked before 11 PM."},
        "handle": {"place": "corridor", "requires": ["keylist"],
                   "text": "A fresh smudge of blue ticket ink is on the door handle of Cabin 4."},
        "teabill": {"place": "dining", "requires": [],
                    "text": "Tea bill: Bella paid for three cups of tea at table 7 at 10:55 PM."},
        "props": {"place": "luggage", "requires": [],
                  "text": "A trunk of gold chains is labeled 'Arjun - Magic Show'. They are only toys."},
        "handkerchief": {"place": "luggage", "requires": ["handle"],
                         "text": "A railway staff handkerchief with blue ink lies near the luggage van door. It smells of Mrs. Kapoor's perfume."},
        "keylist": {"place": "guard", "requires": ["lockok"],
                    "text": "Key list: Bella has a spare key for Cabin 4, and Joe the ticket checker has a master key."},
        "ticketlog": {"place": "guard", "requires": ["keylist"],
                      "text": "Joe's round log is filled for every hour, but the lines from 10:15 to 10:45 PM are empty."},
        "notice": {"place": "guard", "requires": ["sen_witness"],
                   "text": "A letter tells Joe he will lose his job next week because Mrs. Kapoor complained about him."},
        "lily_tip": {"place": None, "requires": [],
                     "text": "Lily says Bella sat in the dining car from 10 to 11 PM."},
        "sen_witness": {"place": None, "requires": [],
                        "text": "Mr. Sen saw Joe near Cabin 4 with a key at about 10:30 PM."},
    },
    "questions": [
        {"question": "How did the thief enter Cabin 4?",
         "options": ["With a key", "Through the window",
                     "By breaking the door", "From the roof"],
         "answer": "With a key"},
        {"question": "Who has a master key for the cabins?",
         "options": ["Joe the ticket checker", "Lily the waitress",
                     "Arjun the magician", "Mr. Sen"],
         "answer": "Joe the ticket checker"},
        {"question": "Where was Bella from 10 to 11 PM?",
         "options": ["In the dining car, drinking tea", "In Cabin 4",
                     "In the luggage van", "In the Guard's Room"],
         "answer": "In the dining car, drinking tea"},
        {"question": "What was found on the door handle of Cabin 4?",
         "options": ["Blue ticket ink", "Red paint", "Black dust", "Gold powder"],
         "answer": "Blue ticket ink"},
        {"question": "What did Mr. Sen see at about 10:30 PM?",
         "options": ["Joe near Cabin 4 with a key", "Bella running away",
                     "Arjun with a gold chain", "Lily in the corridor"],
         "answer": "Joe near Cabin 4 with a key"},
        {"question": "What was strange about Joe's round log?",
         "options": ["The lines from 10:15 to 10:45 PM were empty",
                     "The first page was torn",
                     "His name was missing",
                     "It was written in red ink"],
         "answer": "The lines from 10:15 to 10:45 PM were empty"},
        {"question": "What was inside Arjun's trunk?",
         "options": ["Toy gold chains for his show", "Real gold bars",
                     "Mrs. Kapoor's necklace", "A sleeping bag"],
         "answer": "Toy gold chains for his show"},
        {"question": "Why did the thief take the necklace?",
         "options": ["To take revenge because he was losing his job",
                     "To pay for a new house",
                     "To give it as a gift",
                     "To win a bet"],
         "answer": "To take revenge because he was losing his job"},
        {"question": "What was found near the door of the luggage van?",
         "options": ["A railway handkerchief with blue ink", "A broken watch",
                     "A torn ticket", "A black glove"],
         "answer": "A railway handkerchief with blue ink"},
        {"question": "What sign hung on the door of Cabin 4?",
         "options": ["Do Not Disturb", "Closed for Cleaning", "Welcome", "Out of Order"],
         "answer": "Do Not Disturb"},
    ],
}
