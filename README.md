# Casting Agency Project
This is the final project of the Udacity Full Stack Developer Nano Degree Program. This aim to sum up all the knowledge in this course. In this project I use Flask for implement, PosgreSQL for database and deploy to Heroku. Moreover this also enable Auth for authentication and authorization. This project allow use to manage actor and movies within a Casting company.

So, for enhance what I've learned in this lession, I deceided to create it and I hope that it will be something benefit for life in the future

## Getting Started
**Installing Dependencies**

1. **Python 3.9**
Follow the instructions to install the latest version of python for your platform in the python docs

2. **Virtual Environment**
I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the python docs
   
4. **PIP Dependencies**
Once you have your virtual environment setup and running, install dependencies by running:

```bash
$ pip install -r requirements.txt
```
or 
```bash
$ pip3 install -r requirements.txt
```
if you using Python 3 or if you encounter any issues

**Running the server**

From within the ./src directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
$ source setup.sh
$ python app.py --reload
```
## Endpoints:

Endpoints : https://huelt22-e02c8fef4dc1.herokuapp.com/

Make sure that you have imported the **TOKEN** variable to environment

- GET /actors
```bash
curl -X GET 'https://huelt22-e02c8fef4dc1.herokuapp.com/actors'
```
This API return like below: 
```bash
{
  "actors": [],
  "success": true
}
```
- DELETE /actors/<int:actor_id>
Replace actor ID when using
```bash
curl -X DELETE 'https://huelt22-e02c8fef4dc1.herokuapp.com/actors/<int:actor>' -H "Authorization: Bearer ${TOKEN}"
```
This API return like below:
```bash
{
  "actor": "{
    'name': "George",
    'age': 28,
    'gender': 'MALE'
  }",
  "success": true
}
```
- POST /actors
```bash
curl -X POST 'https://huelt22-e02c8fef4dc1.herokuapp.com/actors' --data '{"name":"abc@example.com","gender":"nu","age":"123"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"
```
This API return like below:
```bash
{
  "created": 2,
  "success": true
}
```
- PATCH /actors/<int:actor_id>
Replace actor ID when using
```bash
curl -X PATCH 'https://huelt22-e02c8fef4dc1.herokuapp.com/actors/<int:actor>' --data '{"name":"abc@example.com","gender":"nu","age":"123"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"
```
This API return like below:
```bash
{
  "updated": "{
    'name': "Updated Actor",
    'age': 28,
    'gender': 'MALE'
  }",
  "success": true
}
```
Similarly, you can build these for /movies endpoints too.

## Auth0 Setup:

AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE are all available in the setup.sh file for reference. 
Json Web Tokens: You can find JWTs for each role in the setup.sh file to run the app locally or login by yourself by account below:

**Account**
- Casting Assistant assistant123@gmail.com
- Casting Director director123@gmail.com
- Executive Producer producer123@gmail.com
Password: 123456Aa@

**Roles** : All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- Casting Assistant * get:actors and get:movies
- Casting Director _ All permissions a Casting Assistant has and _ post:actors and delete:actors * patch:actors and patch:movies
- Executive Producer _ All permissions a Casting Director has and _ post:movies and delete:movies

## Deployment Details:

App is deployed to Heroku.
Heroku Postgres DATABASE details are available in setup.sh file for reference.

## Testing:
We can run our entire test case by running the following command at command line
```bash
$ python test_app.py
```
Thank You!
