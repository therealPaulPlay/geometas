from django.test import TestCase
from quiz.models import QuizSession, Quiz, Fact, QuizSessionFact
from quiz.tests.seed_test_database import seed_test_database, create_facts

class QuizSessionTestCase(TestCase):
    
    def setUp(self):
        seed_test_database()
    
    def test_load_facts(self):
        quiz = Quiz.objects.filter(category_id = 1).first()
        create_facts(10)
        
        # First session - 10 new facts, expecting 7 random new ones
        session = QuizSession.objects.create(user_id=1, quiz=quiz)
        session_1_list = session.load_facts()
        session.mark_cancelled()
        self.assertEqual(len(session_1_list), 7)
        fact_ids = [fact.uuid for fact in session_1_list]
        fact_ids_not_included = [fact.uuid for fact in Fact.objects.all() if fact.uuid not in fact_ids]
        
        # Mark all quizsessionfacts from session 1 as .set_correct()
        quiz_session_facts = QuizSessionFact.objects.filter(quiz_session=session)
        for quiz_session_fact in quiz_session_facts:
            quiz_session_fact.set_correct()
        
        # Second session - 3 new facts plus 4 old ones
        session = QuizSession.objects.create(user_id=1, quiz=quiz)
        session_2_list = session.load_facts()
        session.mark_cancelled()
        self.assertEqual(len(session_2_list), 7)
        # Assert that fact_ids_not_included are in session_2_list
        session_2_fact_ids = [fact.uuid for fact in session_2_list]
        for fact_id in fact_ids_not_included:
            self.assertIn(fact_id, session_2_fact_ids)
        
        # Mark all quizsessionfacts from session 2 as .set_false()
        quiz_session_facts = QuizSessionFact.objects.filter(quiz_session=session)
        for quiz_session_fact in quiz_session_facts:
            quiz_session_fact.set_correct()
            
        
        # Third session - no new facts plus 4 old ones
        session = QuizSession.objects.create(user_id=1, quiz=quiz)
        session.load_facts()
        session.mark_cancelled()
        quiz_session_facts = QuizSessionFact.objects.filter(quiz_session=session)
        for quiz_session_fact in quiz_session_facts:
            quiz_session_fact.set_correct()
            
        # Fourth session
        session = QuizSession.objects.create(user_id=1, quiz=quiz)
        session.load_facts()
        session.mark_cancelled()
        quiz_session_facts = QuizSessionFact.objects.filter(quiz_session=session)
        for quiz_session_fact in quiz_session_facts:
            quiz_session_fact.set_correct()
        
        # Fifth session
        session = QuizSession.objects.create(user_id=1, quiz=quiz)
        session.load_facts()
        session.mark_cancelled()
        quiz_session_facts = QuizSessionFact.objects.filter(quiz_session=session)
        for quiz_session_fact in quiz_session_facts:
            quiz_session_fact.set_correct()
        
        