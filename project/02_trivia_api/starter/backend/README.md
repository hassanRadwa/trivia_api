# Full Stack Trivia API Backend
# Introduction
 This is an API to manage trivia app and play the game. 
 Using the application you can:
 1- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
 Delete questions.
 2-Add questions and require that they include question and answer text.
 3-Search for questions based on a text query string.
 4-Play the quiz game, randomizing either all questions or within a specific category.
## Getting Started
 Base URL: this app can be run locally. The backend app is hosted at the default, http://localhost:5000/, which is set as proxy in the frontend configuration.
 API Keys /Authentication (if applicable): it doesn't require authentication or keys.
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
## Errors
 errors are returned as JSON objects in the following format:
 {
   "success": False, 
   "error": 422,
   "message": "unprocessable"
 }
 The API will return four types of errors when requests fail:
 .400:bad request
 .422:unprocessable
 .404:Not found
 .500:Internal Server Error

## Resource endpoint library
 .GET '/categories'
  +General: 
   Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
   Request Arguments: None
   Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs, and success key.
  +Sample:
   curl http://localhost:5000/categories
   {
     "categories": {
       "1": "Science",
       "2": "Art",
       "3": "Geography",
       "4": "History",
       "5": "Entertainment",
       "6": "Sports"
     },
     "success": true
   }

 .GET /questions
  +General: 
   returns a list of questions objects, success value, total number of questions, and categories.
   results are paginated in groups of 10. Include a request argument to select page number, starting from 1.
  +Sample:
   curl http://localhost:5000/questions?page=1
   {
     "categories": {
       "1": "Science", 
       "2": "Art", 
       "3": "Geography", 
       "4": "History", 
       "5": "Entertainment", 
       "6": "Sports"
     }, 
     "questions": [
       {
         "answer": "Maya Angelou", 
         "category": 4, 
         "difficulty": 2, 
         "id": 5, 
         "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
       }, 
       {
         "answer": "Muhammad Ali", 
         "category": 4, 
         "difficulty": 1, 
         "id": 9, 
         "question": "What boxer's original name is Cassius Clay?"
       }, 
       {
         "answer": "Apollo 13", 
         "category": 5, 
         "difficulty": 4, 
         "id": 2, 
         "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
       }, 
       {
         "answer": "Tom Cruise", 
         "category": 5, 
         "difficulty": 4, 
         "id": 4, 
         "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
       }, 
       {
         "answer": "Edward Scissorhands", 
         "category": 5, 
         "difficulty": 3, 
         "id": 6, 
         "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
       }, 
       {
         "answer": "Brazil", 
         "category": 6, 
         "difficulty": 3, 
         "id": 10, 
         "question": "Which is the only team to play in every soccer World Cup tournament?"
       }, 
       {
         "answer": "Uruguay", 
         "category": 6, 
         "difficulty": 4, 
         "id": 11, 
         "question": "Which country won the first ever soccer World Cup in 1930?"
       }, 
       {
         "answer": "George Washington Carver", 
         "category": 4, 
         "difficulty": 2, 
         "id": 12, 
         "question": "Who invented Peanut Butter?"
       }, 
       {
         "answer": "Lake Victoria", 
         "category": 3, 
         "difficulty": 2, 
         "id": 13, 
         "question": "What is the largest lake in Africa?"
       }, 
       {
         "answer": "The Palace of Versailles", 
         "category": 3, 
         "difficulty": 3, 
         "id": 14, 
         "question": "In which royal palace would you find the Hall of Mirrors?"
       }
     ], 
     "success": true, 
     "totalQuestions": 20
   }

 .DELETE /questions/{question_id}
  +General: 
   deletes a specific question with the given question_id if it exists. It returns success value.
  +Sample:
   curl -X DELETE http://localhost:5000/questions/58
   {
    "success": true
   }
   
 .POST /questions
  +General: 
   creates a new question using the submitted question, answer, category, and difficulty.
   It returns success value.
  +Sample:
   curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"testing question","answer":"answering test question","difficulty":"1","category":"1"}'
   {
    "success": true
   }
   
 .POST /questions/search
  +General: 
   return any questions for whom the search term is a substring of the question.
   It returns a list of questions objects, success value, total number of questions.
   results are paginated in groups of 10. Include a request argument to select page number, starting from 1.
  +Sample:
   curl http://localhost:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
   {
     "questions": [
       {
         "answer": "Maya Angelou",
         "category": 4,
         "difficulty": 2,
         "id": 5,
         "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
       },
       {
         "answer": "Edward Scissorhands",
         "category": 5,
         "difficulty": 3,
         "id": 6,
         "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
       }
     ],
     "success": true,
     "total_questions": 2
   }

 .GET /categories/{category_id}/questions
  +General: 
   get questions based on category_id if it exists. 
   It returns a list of questions objects, success value, total number of questions, and current category.
   results are paginated in groups of 10. Include a request argument to select page number, starting from 1.
  +Sample:
   curl http://localhost:5000/categories/1/questions
   {
     "currentCategory": 1,
     "questions": [
       {
         "answer": "The Liver",
         "category": 1,
         "difficulty": 4,
         "id": 20,
         "question": "What is the heaviest organ in the human body?"
       },
       {
         "answer": "Alexander Fleming",
         "category": 1,
         "difficulty": 3,
         "id": 21,
         "question": "Who discovered penicillin?"
       },
       {
         "answer": "Blood",
         "category": 1,
         "difficulty": 4,
         "id": 22,
         "question": "Hematology is a branch of medicine involving the study of what?"
       }
     ],
     "success": true,
     "totalQuestions": 3
   }

 .POST /quizzes
  +General: 
   get questions to play the quiz. 
   get questions based on category_id if it exists. 
   It takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
   It returns a questions object and success value.
  +Sample:
   curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[16,17],"quiz_category":{"type":"Art","id":2}}'
   {
     "question": {
       "answer": "One",
       "category": 2,
       "difficulty": 4,
       "id": 18,
       "question": "How many paintings did Van Gogh sell in his lifetime?"
     },
     "success": true
   }

## Testing
To run the tests, run
python test_flaskr.py

There are 14 tests covering:
  - get all categories successfully
  - get all questions successfully
  - invalid page number handling when getting questions, checking error 404 
  - delete question with id successfully
  - handling delete question with nonexisting id, checking error 422
  - create question successfully
  - handling create question with empty answer, checking error 400
  - search questions by searchTerm successfully
  - handling search questions with empty searchTerm, checking error 400
  - handling search questions with nonExisting searchTerm, checking error 422
  - get Questions By CategoryId successfully
  - handling get questions with nonExisting CategoryId, checking error 422
  - quizzes get question by CategoryId successfully
  - handling quizzes questions with empty inputs, checking error 400
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```