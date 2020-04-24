from django.db import models
import re
import bcrypt
from datetime import datetime, date


# Create your models here.
class UserManager(models.Manager):
    def userValidator(self,postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name of at least 2 characters required!"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name of at least 2 characters required!"

# email validation

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['reg_email']):
            errors['reg_email'] = "Invalid email address!"


        emailMatch = User.objects.filter(email = postData['reg_email'])

        if len(emailMatch)>0:
            errors['duplicated_email'] = "Email taken, please use another email!"

# birthdate validation

        currentDate = date.today()
        birthday = datetime.strptime(postData['bday'], "%Y-%m-%d").date()
        print(currentDate)

        if birthday > currentDate:
            errors['bday'] = "Invalid date of birth, Please provide your date of birth."

# password Validation
        if postData['reg_pw'] != postData['confirm_pw']:
            errors['reg_pw'] = "Password does not match!"

        elif len(postData['reg_pw'])<8:
            errors['reg_pw'] = "Password needs to be at least 8 characters"
        return errors

# Login validations

    def loginValidator(self, postData):
        errors = {}
        # log In errors
        emailMatch = User.objects.filter(email = postData['login_email'])
        
        if len(postData['login_email'])<1:
            errors['login_email'] = "Enter your registered email to Log In"
# email validation on login
        elif len(emailMatch) == 0:
            errors['email does not exist'] = "Invalid email, please use another email or register!"
        # if the email is valid, verify if password match
        else:
            user = emailMatch[0]
            if not bcrypt.checkpw(postData['login_pw'].encode(), user.password.encode()):
                errors['login_pw'] = "Password does not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    birthday = models.DateField(auto_now_add=False, null = True)
    password = models.CharField(max_length=75)
    confirm_password = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
