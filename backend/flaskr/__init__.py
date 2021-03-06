import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
          )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
          )
      return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route("/categories", methods=['GET'])
  def get_categories():
      categories = Category.query.all()
      categories_dict = {category.id: category.type for category in categories}

      if len(categories) == 0:
          abort(404)

      return jsonify(
          {
              "success": True,
              "categories": categories_dict
          }
      )


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
  @app.route("/questions")
  def get_questions():
      try:
          selection = Question.query.order_by(Question.id).all()
          if len(selection) == 0:
              abort(404)
          current_questions = paginate_questions(request, selection)
          categories = Categories.query.all()
          categories_dict = {category.id: category.type for category in categories}

          return jsonify(
              {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": categories_dict,
                #"current_category":
                })
      except Exception as e:
          print(e)
          abort(400)


  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.filter_by(id=id).one_or_none()
          if question is None:
              abort(404)
          question.delete()

          return jsonify(
              {
                "success": True,
              })
        except Exception as e:
            print(e)
            abort(400)


  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()
      new_question = body.get('question', None)
      answer = body.get('answer', None)
      category = body.get('category', None)
      difficulty = body.get('difficulty', None)

      try:
          question = Question(question= new_question, answer= answer,
                              category= category, difficulty=difficulty)
          question.insert()
          selection = Question.query.order_by(Question.id).all()
          if len(selection) == 0:
              abort(404)
          current_questions = paginate_questions(request, selection)
          categories = Categories.query.all()
          categories_dict = {category.id: category.type for category in categories}

          return jsonify(
              {
                  "success": True,
                  "questions": current_questions,
                  "total_questions": len(selection),
                  "categories": categories_dict,
                  #"current_category": []
              }
          )

      except Exception as e:
          print(e)
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
  @app.route('/questions/search', methods=['POST'])
  def search():
      body = request.get_json()
      search_term = body.get('searchTerm')
      questions = Question.query.filter(Question.question.ilike('%'+search+'%')).all()

      if len(questions) = 0:
          abort(404)
      current_questions = paginate_questions(request, questions)
      return jsonify(
          {
              "success": True,
              "questions": current_questions,
              "total_questions": len(questions)
         }
    )

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_id(id):
      category = Category.query.filter_by(id=id).one_or_none()
      if category is None:
          abort(404)
      category_questions = Questions.query.filter_by(category=str(id)).all()
      current_questions = paginate_questions(request, category_questions)
      return jsonify({
          "success": True,
          "questions": current_questions,
          "total_questions": len(category_questions),
          "current_category": category.type
      })

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
 @app.route('/quizzes', methods=['POST'])
 def quiz():
     body = request.get_json()
     quiz_category = body.get('quiz_category')
     previous_questions = body.get('previous_questions')

     try:
         if (quiz_category['id']==0):
             questions = Question.query.all()
         else:
             questions = Question.query.filter_by(category=quiz_category['id']).all()

         random_number = random.randint(0, len(questions)-1)
         random_number_list = []
         while random_number not in random_number_list:
             next_question =questions[random_number]
             if next_question.id not in previous_questions:
                 return jsonify({
                     "success": True,
                     "question": {
                         "answer": next_question.answer,
                         "category": next_question.category,
                         "difficulty": next_question.difficulty,
                         "id": next_question.id,
                         "question": next_question.question
                         },
                     "previousQuestions": previous_questions
                     })
         random_number_list.append(random_number)
         random_number = random.randint(0, len(questions)-1)


     except Exception as e:
         print(e)
         abort(404)
  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_recource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable recource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method!"
        }), 405


  return app
