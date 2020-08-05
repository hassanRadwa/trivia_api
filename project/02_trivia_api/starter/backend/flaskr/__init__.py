import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from operator import itemgetter 
import math

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def getCategories():
    categories_list = Category.query.all()
    if len(categories_list) == 0:
      abort(404)
    categories_dict = listToDict_Category(categories_list)
    return jsonify({
      'success': True,
      'categories':categories_dict
    }),200

  def listToDict_Category(list):
    tempDict={}
    #convert list of data to dictionary
    for listitem in list:
      tempDict.update({listitem.id: listitem.type})
    return tempDict

  def paginateSelection(request,selection):
    page             = request.args.get('page' , 1 , type = int)
    no_of_items      = len(selection)
    totalPages       = math.ceil(no_of_items / QUESTIONS_PER_PAGE)
    if page > totalPages:
      abort(404)
    start            = (page - 1) * QUESTIONS_PER_PAGE
    end              = start + QUESTIONS_PER_PAGE
    selection_list   = [sel.format() for sel in selection]
    return selection_list[start:end]

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def getQuestions():
    #get questions from db
    questions = Question.query.all()
    #get categories from db and convert it to dict because of frontend design
    categories  = listToDict_Category(Category.query.all())
    return jsonify({
      'success'        : True,
      'questions'      : paginateSelection(request,questions),
      'totalQuestions' : len(questions),
      'categories'     : categories
    }),200
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def deleteQuestion(id):
    try:
      selQues = Question.query.filter(Question.id == id).one_or_none()
      if selQues is None:
        abort(404)
      selQues.delete()
      return jsonify({
        'success': True
      }),200
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions' , methods = ['POST'])
  def AddNewQuestion():
    data        = request.get_json()
    question    = data.get('question')
    answer      = data.get('answer')
    category    = data.get('category')
    difficulty  = data.get('difficulty')
    if (question == '' or answer == '' or category == '' or difficulty == ''):
      abort(400)
    try:
      newQuestion = Question(
        question     = question,
        answer       = answer,
        category     = category,
        difficulty   = difficulty
        )
      newQuestion.insert()
      return jsonify({
        'success': True
      }), 200
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['GET','POST'])
  def searchQuestions():
    data       = request.get_json()
    searchTerm = data.get('searchTerm')
    if searchTerm == '':
      abort(400)
    try:
      results = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
      if len(results) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'questions': paginateSelection(request,results),
        'total_questions': len(results)
      }),200
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def getQuestionsByCategoryId(category_id):
    try:
      selectedCategory = Category.query.filter(Category.id == category_id).one_or_none()
      if selectedCategory is None:
        abort(404)
      else:
        questions_by_catId=Question.query.filter(Question.category == category_id).all()
        if len(questions_by_catId) == 0:
          abort(404)
        else:
          return jsonify({
            'success'   : True,
            'questions' : paginateSelection(request,questions_by_catId),
            'totalQuestions' : len(questions_by_catId),
            'currentCategory': category_id
            }),200
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['GET','POST'])
  def getRandomQuestionByCatIdAndPrevQues():
  
    #get category id and previous questions
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category      = data.get('quiz_category')
    #print('previous_questions ',previous_questions)
    #print('quiz_category ',quiz_category)
    if (quiz_category == {}):
      abort(400)
    #print('after first abort')
    #print('quiz_category[\'id\'] ',quiz_category['id'])
    #get all Questions
    if (quiz_category['id'] == 0): 
      selection = Question.query.all()
      #print('selection ',selection)
    else:
      try:
        #check if the selected category exists
        cat_selection = Category.query.filter(Category.id == quiz_category['id']).one_or_none()
        if (cat_selection is None):
          abort(404)
        else:
          #get questions by category id
          selection = Question.query.filter(Question.category == quiz_category['id']).all()
          if (len(selection) == 0):
            abort(404)
      except:
        abort(422)
    #convert questions dict to list
    selectedQuestions = [sel.format() for sel in selection]
    # print('selectedQuestions ',selectedQuestions)
    #extract all questions ids in a list
    id_list = list(map(itemgetter('id'), selectedQuestions)) 
    #print('id_list ',id_list)
    #generate random number to select one random question id of the selected list
    generated = False
    while not generated:
      #select random number from a list
      randomQuestionId = random.choice(id_list)
      #print('randomQuestionId ',randomQuestionId)
      #check if the randomly selected question ID exists in the previous_questions
      if randomQuestionId not in previous_questions:
        generated = True 
    #get the question with the selected id
    i=0
    for d in selectedQuestions:
      if d['id'] == randomQuestionId:
        question = selection[i].format()
        break
      i+=1
    #print('question ',question)
    return jsonify({
        'success'   : True,
        'question' : question
        }),200 
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422
    
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400  
    
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500
  
  return app

    