import unittest
from src.questions import question_bank
from src.utils import shuffle_questions, calculate_score

class TestQuizApp(unittest.TestCase):
    def test_question_bank_not_empty(self):
        self.assertTrue(len(question_bank) > 0)
        
    def test_shuffle_questions(self):
        shuffled = shuffle_questions(question_bank)
        self.assertEqual(len(shuffled), len(question_bank))
        # Check that all original questions are present
        original_questions = {q['question'] for q in question_bank}
        shuffled_questions = {q['question'] for q in shuffled}
        self.assertEqual(original_questions, shuffled_questions)
        
    def test_calculate_score(self):
        self.assertEqual(calculate_score(8, 10), 80.0)
        self.assertEqual(calculate_score(0, 10), 0.0)
        self.assertEqual(calculate_score(5, 5), 100.0)

if __name__ == '__main__':
    unittest.main()