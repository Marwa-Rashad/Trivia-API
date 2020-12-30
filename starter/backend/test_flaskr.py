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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    
    #delete question
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], '5')
        self.assertEqual(res.status_code, 200)
        question = Question.query.get(5)
        self.assertFalse(question)
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
    #test search
    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 1)
    #test get by category

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], 6)
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





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()