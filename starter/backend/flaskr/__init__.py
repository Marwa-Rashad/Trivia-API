import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  
  @app.route('/categories')
  def get_categories():
    try:
      categories = list(map(Category.format, Category.query.all()))
      categoriesList = {category['id']:category['type'] for category in categories}

      result = {
              "success": True,
              "categories": categoriesList
          }
      return jsonify(result)
    except:
      abort(400)
    finally:
      db.session.close()


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
  data = db.session.query(Show).join(Artist).filter(Artist.id == artist.id).join(Venue).all()

  '''
  @app.route('/questions')
  def get_questions():
    try:
      search_term=request.form.get('searchTerm', '')
      if not search_term and request.method == 'GET':
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions ] 
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        categories = list(map(Category.format, Category.query.all()))
        categoriesList = {category['id']:category['type'] for category in categories}
        if formatted_questions[start:end]:
          return jsonify({
                    'success': True,
                    'questions': formatted_questions[start:end],
                    'total_questions': len(formatted_questions),
                    'categories': categoriesList
                })
        else:
          abort(404)
    except:
      abort(404)
    finally:
      db.session.close()  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      Question.delete(question)
      return jsonify({
        'success': True,
        'id': question_id
      })
    except:
      db.session.rollback()
      abort(404)
    finally:
      db.session.close()
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''



  @app.route('/add', methods=['POST'])
  def add_question():
    try:
      question = Question(
        question = request.get_json()['question'],
        answer = request.get_json()['answer'],
        category = request.get_json()['category'],
        difficulty = request.get_json()['difficulty']
      )
      Question.insert(question)
      added_question = question.format()
      result = jsonify(
     {   'success': True,
         'id': added_question['id'],
      'question': added_question['question'],
      'answer': added_question['answer'],
      'category': added_question['category'],
      'difficulty': added_question['difficulty']
             })
      return result 
    except:
      abort(422)
    finally:
      db.session.close()

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_questions():
    try:
      if request.method == 'POST':
        search_term = request.get_json()['searchTerm']
        search = "%{}%".format(search_term)
        data = db.session.query(Question).filter(Question.question.ilike(search)).all()
        formatted_questions = [question.format() for question in data ] 
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        if formatted_questions[start:end]:
          return jsonify({
                  'success': True,
                  'questions': formatted_questions[start:end],
                  'total_questions': len(formatted_questions),
              })
        else:
          abort(404)
    except:
      abort(404)
    finally:
      db.session.close()

  


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_Category(category_id):
    try:
      questions = Question.query.filter(Question.category == category_id).all()
      formatted_questions = [question.format() for question in questions ]
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      if formatted_questions[start:end]:
        result = jsonify({
                  'success': True,
                  'questions': formatted_questions[start:end],
                  'total_questions': len(formatted_questions),
                  'current_category': category_id
              })
        return result
      else:
        abort(404)
    except:
      abort(404)
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
  @app.route('/quizzes', methods=["POST"])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions", [])
    quiz_category = body.get("quiz_category", None)
    try:
        if quiz_category:
            if quiz_category["id"] == 0:
                quiz = Question.query.all()
            else:
                quiz = Question.query.filter_by(category=quiz_category["id"]).all()
        if not quiz:
            return abort(422)
        selected = []
        for question in quiz:
            if question.id not in previous_questions:
                selected.append(question.format())
        if len(selected) != 0:
            result = random.choice(selected)
            return jsonify({"success": True, "question": result})
        else:
            return jsonify({"success": False, "question": False})
    except:
        abort(422)
    finally:
      db.session.close()

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
  def unprocessable_entity(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unable to process the contained instructions"
        }), 422
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "The server cannot or will not process the request due to something that is perceived to be a client error"
        }), 400
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "The server encountered an unexpected condition that prevented it from fulfilling the request"
        }), 500
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405
  return app

    