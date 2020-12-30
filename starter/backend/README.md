# Full Stack Trivia API Backend

## Getting Started

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


## API Reference 

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted on a base URL. The backend app is hosted at the defualt, http://127.0.0.1:5000/, which is set as a proxy in the front end configuration. 
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{      "success": False, 
        "error": 404,
        "message": "Not found"
        }
```

The API will return the following types when requests fail:
-	400: Bad Request
-	404: Not Found
-	422: Unprocessable Entity
- 500: Internal Server Error
### Endpoints

To avoid redundacny in the API documentation, this is a refernece of the main object types.

##### question
An object of answer: answer_string, category: category_id, difficulty: difficulty_level, id: question_id, and question: question_string key:value pairs.

##### categories

An object of id: category_string key:value pairs.

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request arguments: none
- Returns: an object with a success:value key:value pair and categories that contains categories object.
- Sample: `curl http://127.0.0.1:5000/categories`
```
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
 ```

#### GET '/questions'

- Fetches a dictionary of questions, success value, total number of questions, and categories.
- Results are paginated in groups of 10. 
- Include a request argument to choose page number starting from 1. One is default so it need not to be included.
- Returns: An object with a success:value key:value pair, total_questions: total_questions_number key:value pair, questions key that contains a list of questions objects.
- Sample: `curl http://127.0.0.1:5000/questions`
```{
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
},
{
"answer": "Agra",
"category": 3,
"difficulty": 2,
"id": 15,
"question": "The Taj Mahal is located in which Indian city?"
},
{
"answer": "Escher",
"category": 2,
"difficulty": 1,
"id": 16,
"question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
}
],
"success": true,
"total_questions": 33
}
```
#### POST '/questions'

- Fetches a dictionary of questions based on a serach term, for whom the search term  is a substring of the question. 
- Request arguments: search term.
- Returns: an object with a success:value key:value pair, total_questions: total_questions_number key:value pair, questions key that contains a list of questions objects.
- Sample: `curl --request POST http://127.0.0.1:5000/questions --header "Content-Type: application/json" -d "{\"searchTerm\":\"title\"}"`

```
{
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### DELETE '/questions/<int:question_id>'

- If provided, deletes the specified question.
- Request argument: question ID.
- Returns: an object of success: value key:value pairs and id: deleted_question_id key:value pairs.
- Sample: `curl curl http://127.0.0.1:5000/questions/9 -X DELETE`
```
{
  "id": "9",     
  "success": true
}
```

#### GET '/categories/<int:category_id>/questions'

- Fetches a dictionary of questions based on the submitted category ID.
- Request argument: category ID.
- Returns: an object with a success:value key:value pair, total_questions: total_questions_number key:value pair, questions key that contains a list of questions objects, and current_category: category_id key:value pair.
- Sample: `curl http://127.0.0.1:5000/categories/3/question'`
```
{
  "current_category": 3,
  "questions": [
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
#### POST '/add'
- Creates a new question using the submitted question, answer, category, difficulty.
- Request arguments: question object.
- Returns: an object with a success:value key:value pair and added question data.
- Sample: `curl --request POST http://127.0.0.1:5000/add --header "Content-Type: application/json" -d "{\"question\":\"What is the best movie ever?\",\"answer\":\"The God Father\",\"difficulty\":2,\"category\":5}"`
```
{
  "answer": "The God Father",
  "category": 5,
  "difficulty": 2,
  "id": 57,
  "question": "What is the best movie ever?",
  "success": true
}
```

### POST '/quizzes'

- Feteches a random question within a given category.
- Request arguments: an object of 'quiz_category' key that includes an object of id: category_id  and type: category_string key:value pairs, and previous_questions key that contains a list of the previously played questions IDs.
- Returns: an object with a success:value key:value pair and question key that includes the random question object or False if there is no question.
- Sample: `curl --request POST http://127.0.0.1:5000/quizzes --header "Content-Type: application/json" -d "{\"previous_questions\":[17], \"quiz_category\": {\"id\": 2, \"type\": \"Art\"}}"`

```
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
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
