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
        self.database_name = "trivia"
        self.database_path = "postgresql://postgres:radwa@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
    
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
    
    def test_404_get_questions_not_valid_page(self):
        res = self.client().get('/questions?page=50')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not found')
    
    def test_delete_question_with_id(self):
      newQuestion = Question(
        question     = "question",
        answer       = "answer",
        category     = '1',
        difficulty   = '1'
        )
      newQuestion.insert()
      res = self.client().delete(f'/questions/{newQuestion.id}')
      data = json.loads(res.data)
      self.assertEqual(res.status_code,200)
      self.assertEqual(data['success'],True)
    
    def test_422_delete_question_with_nonexisting_id(self):
      res = self.client().delete(f'/questions/100')
      data = json.loads(res.data)
      self.assertEqual(res.status_code,422)
      self.assertEqual(data['success'],False)
      self.assertEqual(data['message'],'unprocessable')
    
    def test_create_question(self):
        res = self.client().post('/questions',json = {
            'question'    : 'testing question',
            'answer'      : 'answering test question',
            'difficulty'  : '1',
            'category'    : '1'
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_400_create_question_with_empty_answer(self):
        res = self.client().post('/questions',json = {
            'question'    : 'testing question',
            'answer'      : '',
            'difficulty'  : '1',
            'category'    : '1'
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')
    
    def test_search_questions_by_searchTerm(self):
        res = self.client().post('/questions/search',json = {
            'searchTerm' : 'title'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']),2)
        self.assertTrue(data['total_questions'])

    def test_400_search_questions_with_empty_searchTerm(self):
        res = self.client().post('/questions/search',json = {
            'searchTerm' : ''
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')

    def test_422_search_questions_with_nonExisting_searchTerm(self):
        res = self.client().post('/questions/search',json = {
            'searchTerm' : 'hhhhhhhhhhhhhhhhhh'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')

    def test_get_Questions_By_CategoryId(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_422_get_questions_with_nonExisting_CategoryId(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')

    def test_quizzes_get_question_by_CategoryId(self):
        res = self.client().post('/quizzes',json = {
            'previous_questions' : [16,17],
            'quiz_category'      : {'type':'Art' , 'id':2}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'],16)
        self.assertNotEqual(data['question']['id'],17)

    def test_400_quizzes_questions_with_empty_inputs(self):
        res = self.client().post('/quizzes',json = {
            'previous_questions' : [],
            'quiz_category'      : {}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()