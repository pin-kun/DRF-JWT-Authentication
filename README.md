# DRF-JWT-Authentication
Used JWT Authentication in DRF

This is a fairly simple Django Rest Framework API project using JWT Authentication.

### To run this project in your local system, follow below steps:
1. Clone the repo into local system: `git clone https://github.com/pin-kun/DRF-JWT-Authentication.git`
2. Create your own virtual env and actvate it. Linux command: `source your_venv/bin/activate`
3. Now in that virutal env, install the libraries and packages that I have used in this project
    - Run this command to install all the libraries in vnenv: `pip install -r requirements.txt`
4. Go to the project base directory and run this project
    - Command to run this project locally: `python manage.py runserver`
    
    
There is not Front-End for this project.
So, To test the API use `postman` or `Thunder Client` in VS Code


**JWT Authentication:**
-  While registering JWT Token will be assigned to user
-  While Logging in, It will use the Token assigned to it
-  While reseting the password, it will send the link to the mail and from there you can change the password.
    - Even if you don't get reset link in mail, don't worry. `uid` and `token` will be available in cmd. you can copy-paste into url and test the api

**APIs you can test in `postman`:**
- POST: http://127.0.0.1:8000/api/register/
- POST: http://127.0.0.1:8000/api/login/
- GET: http://127.0.0.1:8000/api/profile/
- POST: http://127.0.0.1:8000/api/changepassword/
- POST: http://127.0.0.1:8000/api/send-email-rest-password-link/
- POST: http://127.0.0.1:8000/api/reset-password/uid/token/ 
