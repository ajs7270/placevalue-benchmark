from unittest import TestCase
from core import convert_and_caching_prob
from datasets.dataset import Problem


class Test(TestCase):
    def test_convert_and_caching_prob(self):
        case1 = {
            "ID": "chal-1",
            "Body": "Each pack of dvds costs 76 dollars. If there is a discount of 25 dollars on each pack",
            "Question": "How much do you have to pay to buy each pack?",
            "Equation": "( 76.0 - 25.0 )",
            "Answer": 51.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case1['Body'], question=case1['Question'], answer=case1['Answer']), inplace=False)

        self.assertEqual(passage, 'Each pack of dvds costs number0 dollars. If there is a discount of number1 dollars on each pack')
        self.assertEqual(question, 'How much do you have to pay to buy each pack?')
        self.assertEqual(cache, 'number0 = 76\nnumber1 = 25\n')

        case2 = {
            "ID": "chal-12",
            "Body": "They decided to hold the party in their backyard. If they have 11 sets of tables and each set has 13 chairs",
            "Question": "How many chairs do they have in the backyard?",
            "Equation": "( 11.0 * 13.0 )",
            "Answer": 143.0,
            "Type": "Multiplication"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case2['Body'], question=case2['Question'], answer=case2['Answer']), inplace=False)

        self.assertEqual(passage, 'They decided to hold the party in their backyard. If they have number0 sets of tables and each set has number1 chairs')
        self.assertEqual(question, 'How many chairs do they have in the backyard?')
        self.assertEqual(cache, 'number0 = 11\nnumber1 = 13\n')

        case3 = {
            "ID": "chal-13",
            "Body": "In a school there are 458 more girls than boys. If there are 690 girls",
            "Question": "How many pupils are there in that school?",
            "Equation": "( ( 690.0 + 690.0 ) - 458.0 )",
            "Answer": 926.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case3['Body'], question=case3['Question'], answer=case3['Answer']), inplace=False)

        self.assertEqual(passage, "In a school there are number0 more girls than boys. If there are number1 girls")
        self.assertEqual(question, "How many pupils are there in that school?")
        self.assertEqual(cache, "number0 = 458\nnumber1 = 690\n")

        case4 = {
            "ID": "chal-126",
            "Body": "Kelly has 22 nintendo games.",
            "Question": "How many does she need to buy so that she will have 140 games left?",
            "Equation": "( 140.0 - 22.0 )",
            "Answer": 118.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case4['Body'], question=case4['Question'], answer=case4['Answer']), inplace=False)

        self.assertEqual(passage, "Kelly has number0 nintendo games.")
        self.assertEqual(question, "How many does she need to buy so that she will have number1 games left?")
        self.assertEqual(cache, "number0 = 22\nnumber1 = 140\n")

    def test_convert_and_caching_prob_inplace(self):
        case1 = {
            "ID": "chal-1",
            "Body": "Each pack of dvds costs 76 dollars. If there is a discount of 25 dollars on each pack",
            "Question": "How much do you have to pay to buy each pack?",
            "Equation": "( 76.0 - 25.0 )",
            "Answer": 51.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case1['Body'], question=case1['Question'], answer=case1['Answer']), inplace=True)

        self.assertEqual(passage,
                         'Each pack of dvds costs 76(number0) dollars. If there is a discount of 25(number1) dollars on each pack')
        self.assertEqual(question, 'How much do you have to pay to buy each pack?')
        self.assertEqual(cache, 'number0 = 76\nnumber1 = 25\n')

        case2 = {
            "ID": "chal-12",
            "Body": "They decided to hold the party in their backyard. If they have 11 sets of tables and each set has 13 chairs",
            "Question": "How many chairs do they have in the backyard?",
            "Equation": "( 11.0 * 13.0 )",
            "Answer": 143.0,
            "Type": "Multiplication"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case2['Body'], question=case2['Question'], answer=case2['Answer']), inplace=False)

        self.assertEqual(passage,
                         'They decided to hold the party in their backyard. If they have 11(number0) sets of tables and each set has 13(number1) chairs')
        self.assertEqual(question, 'How many chairs do they have in the backyard?')
        self.assertEqual(cache, 'number0 = 11\nnumber1 = 13\n')

        case3 = {
            "ID": "chal-13",
            "Body": "In a school there are 458 more girls than boys. If there are 690 girls",
            "Question": "How many pupils are there in that school?",
            "Equation": "( ( 690.0 + 690.0 ) - 458.0 )",
            "Answer": 926.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case3['Body'], question=case3['Question'], answer=case3['Answer']), inplace=False)

        self.assertEqual(passage, "In a school there are 458(number0) more girls than boys. If there are 690(number1) girls")
        self.assertEqual(question, "How many pupils are there in that school?")
        self.assertEqual(cache, "number0 = 458\nnumber1 = 690\n")

        case4 = {
            "ID": "chal-126",
            "Body": "Kelly has 22 nintendo games.",
            "Question": "How many does she need to buy so that she will have 140 games left?",
            "Equation": "( 140.0 - 22.0 )",
            "Answer": 118.0,
            "Type": "Subtraction"
        }

        passage, question, cache = convert_and_caching_prob(
            Problem(passage=case4['Body'], question=case4['Question'], answer=case4['Answer']), inplace=False)

        self.assertEqual(passage, "Kelly has 22(number0) nintendo games.")
        self.assertEqual(question, "How many does she need to buy so that she will have 140(number1) games left?")
        self.assertEqual(cache, "number0 = 22\nnumber1 = 140\n")

