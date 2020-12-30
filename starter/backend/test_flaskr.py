import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        DB_USER = os.getenv('DB_USER', 'postgres')  
        DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')  
        DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
#test get all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
    def test_405_method_not_allowed(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test get questions (per page)
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['questions']), 10)

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    
    #delete question
    def test_delete_question(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 10)
        self.assertEqual(res.status_code, 200)
        question = Question.query.get(10)
        self.assertFalse(question)
    
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
        
    #add question    
    def test_add_question(self):
        res = self.client().post('/add', json={
        'question' :'What is the best movie ever?',
        'answer' :'The God Father',
        'category' : 5,
        'difficulty' : 4}
        )
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], 'What is the best movie ever?')
        self.assertEqual(data['answer'], 'The God Father')
        self.assertEqual(data['category'], 5)
        self.assertEqual(data['difficulty'],4 )
        self.assertTrue(data['id'])
        self.assertEqual(res.status_code, 200)

    def test_422_if_question_not_added(self):
        res = self.client().post('/add', json={
        'question' :'What is the best movie ever?',
        'answer' :'The God Father',
        'difficulty' : 4}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions')
        
    #test search
    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)

    def test_404_if_searchTerm_has_no_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'za3balawi'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    #test get by category

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(data['current_category'], 4)

    def test_404_if_category_does_not_exist(self):
        res = self.client().get('/categories/85/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

#test play quiz
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
     'previous_questions': [17], 'quiz_category': {'id': 2, 'type': 'Art'}
        })
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 17)
        self.assertEqual(res.status_code, 200)

    def test_422_if_category_not_valid(self):
        res = self.client().post('/quizzes', json={
     'previous_questions': [17], 'quiz_category': {'id': 40}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the contained instructions')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()