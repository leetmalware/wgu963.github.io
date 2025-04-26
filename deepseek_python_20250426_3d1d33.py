def shuffle_questions(questions):
    """Shuffle the question bank while maintaining question-answer pairs"""
    return random.sample(questions, len(questions))

def calculate_score(correct, total):
    """Calculate and return the percentage score"""
    return round((correct / total) * 100, 2) if total > 0 else 0