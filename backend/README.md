# Trivia API

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game


## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:
```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500 Internal Server Error

### Endpoints
#### GET /categories
- General:
    - Returns a dictionary of categories of quizzes , success value
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "success": true
  "categories": {
    "1": "Science"
    "2": "Art"
    "3": "Geography"
  }
}

```
#### GET /questions
- General:
    - Returns a list of questions, total questions, categories and success
    -  Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
         "success": True,
         "questions": [
           {
             "answer": "Tom Cruise",
             "category": "5",
             "difficulty": 4,
             "id": 4,
             "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
           },
           {
             "answer": "Maya Angelou",
             "category": "4",
             "difficulty": 2,
             "id": 5,
             "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
           },
           {
             "answer": "Edward Scissorhands",
             "category": "5",
             "difficulty": 3,
             "id": 6,
             "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
           }],
         "total_questions": 3,
         "categories": {
           "1": "Science"
           "2": "Art"
           "3": "Geography"
         }
       }

```
#### DELETE /questions/{id}
- General:
    - Deletes the question of the given ID if it exists. Returns success value
- `curl -X DELETE http://127.0.0.1:5000/questions/2`
```{
  "success": true
   }
```
#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns category, success value, total questions, and question list based on current page number to update the frontend.
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", "answer":"Edward Scissorhands", "category":"5", "difficulty": "3"}'`
```
{
  "success": True,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }],
  "total_questions": 3,
  "categories": {
    "1": "Science"
    "2": "Art"
    "3": "Geography"
  }
}
```
#### POST /search
- General:
    -search for a question using the submitted search term. Returns the results, success value, total questions.
- `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}'`
```
{
  "success": true,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },  
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }],
  "total_questions": 2
}
```
#### GET /categories/{id}/questions
- General:
    -Returns a list of questions in a given category, current category, total questions in category and success value
    -Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- `curl http://127.0.0.1:5000/categories/5/questions`
```
{
  "success": true,
  "questions": [  
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }],
  "current_category": "Entertainment",
  "total_questions": 1
}
```


#### POST /quizzes
- General:
    - receives the actual question and the category and returns next question in category, previous question and success value
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Entertainment","id":"6"}, "previous_questions":[1]}'`
```
{
  "success": true,
  "question": {
    "answer": "Edward Scissorhands",
    "category": "5",
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
}
```


## Deployment N/A

## Authors
Yours truly, Brandon Armand Nyamkimbi

## Acknowledgements
The awesome team at Udacity for their efforts and encouragement on my journey to full stack engineer!
