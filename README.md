# encryptid-intech-21
The platform for Encryptid inTech '21, built with Flask.

## Setup
1. Clone the repository

```$ git clone https://github.com/techsyndicate/encryptid-intech-2021```

2. Create a virtualenv and install all the dependencies.
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
3. Populate the variables in the `.env.example` and rename it to `.env`.

4. Set the `FLASK_ENV` and `FLASK_APP` setup environment variables.
```
$ export FLASK_ENV=development
$ export FLASK_APP=encryptid
```
5. Run the server on port 5000 with `flask run`.

