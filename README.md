# Phonebook API

This is a simple web application with a single HTTP endpoint, `/search/`. 

`/search/` takes at least one of three optional query arguments: `firstName`, `lastName`, `state`.

`/search/?firstName=Jack` will return all the people that have a first name of Jack 

`/search/?firstName=Jack&lastName=Dovel&state=NC` will return all people with the first name of Jack and last name of Dovel in the state of North Carolina.

The response body looks like this:

```
[
  {
    "first_name": "Jack", 
    "last_name": "Dovel", 
    "phonenumber": "4141604385", 
    "state": "NC",
    "email": "jack.dovel@example.com" 
  }
]

```

# Install

1. Make sure that you have Python 3.8 and Pip3 installed on your machine.
2. Install the dependencies with `pip3 install -r requirements.txt`
3. Start the server with `python3 app.py`

# Instructions 

1. Clone this repository
2. Create a new repository under your own account with this code (do not fork this repo directly)
3. For each task below either open a new Github Issue describing a problem and recommending a fix, or create a pull request with a code change.

It is not required that you complete all of the tasks. Play to your strengths and complete the tasks that do the best to demonstrate your skill set.

# Tasks

## Coding Tasks

- The API is case-sensitive right now. Make it case-insensitive.
- Paginate the results instead of having them all show at once 
- Implement an endpoint that does a reverse lookup (search by phone number) 
- The current search implementation makes the API vulnerable to an SQL Injection attack. Fix this bug.

## Questions

- There are multiple duplicates throughout the database. Within the context of this Phonebook API, how might we find and address duplicate entries? 
- We'd like to improve the system to allow us to store multiple phone numbers and email addresses. We want the ability to label the type of email or phone as "work", or "home", and we want the ability to store no more than one "primary" email and phone for each contact. How should we design the schema for this system?
- If you were to build this same system from scratch, how would you do it? 
  - What are some problems with the current design?
  - How could we grow the dataset without impacting search performance? 
- How could the code quality be improved? 
- How might we add tests?
