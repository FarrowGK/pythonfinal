from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime, date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, fname, lname, email, password, conpassword, dob):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }
        if len(fname) < 1:
            response["errors"].append("First name is required")
        elif len(fname) < 3:
            response["errors"].append("First name is required to have atleast 3 characters")

        if len(lname) < 1:
            response["errors"].append("Last name is required")
        elif len(lname) < 3:
            response["errors"].append("Last name is required to have atleast 3 characters")

        if len(email) < 1:
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email):
            response["errors"].append("Invalid email address")

        if len(password) < 1:
            response["errors"].append("Password is required")
        elif len(password) < 8:
            response["errors"].append("Password must be longer than 8 characters")

        if len(conpassword) < 1:
            response["errors"].append("Confirm Password is required")
        elif password != conpassword < 1:
            response["errors"].append("Passwords must match")
        if len(dob) < 1:
            response["errors"].append("Enter a date")
        else:
            date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.now()
            if date > today:
                response["errors"].append("Enter a valid birtday.")

        if len(response["errors"]) > 0:
            response["valid"] = False
        else:
            response["user"] = User.objects.create(
                fname = fname,
                lname = lname,
                email = email,
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                dob = dob
            )
        return response
    def login(self, email, password):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }
        if len(email) < 1:
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email):
            response["errors"].append("Invalid email address")
            return redirect('/')
        else:
            email_list = User.objects.filter(email = email.lower())
            if len(email_list) == 0:
                response["errors"].append("Unknown Email")
        if len(password) < 1:
            response["errors"].append("Password is required")
        elif len(password) < 8:
            response["errors"].append("Password must be longer than 8 characters")
        if len(response["errors"]) == 0:
            hashed_pw = email_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response["user"] = email_list[0]
            else:
                response["errors"].append("Incorrect Password")
        if len(response["errors"]) > 0:
            response["valid"] = False
        return response
class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
class QuoteManager(models.Manager):
    def createquote(self, quotedby, message, creator):
        errors = []
        valid = True
        response = {
            "valid": True,
            "errors": [],
            "quoted": None
        }
        if len(quotedby) < 3:
            response['errors'].append("Enter a valid quote creator")
        if len(message) < 10:
            response['errors'].append("Message must be more than 10 characters")
        if len(response['errors']) > 0:
            response["valid"] = False
            return response
        else:
            response["quoted"] = Quote.objects.create(
                quotedby = quotedby,
                message = message,
                creator = creator
            )
            return response
    def join(self, quoter, itemid):
        response = {
            "valid": True,
            "errors": [],
            "quoter": None,
        }
        quote = Quote.objects.get(id=itemid)
        user = User.objects.get(id=quoter)
        quote.quoters.add(user)
        return response
    def remove(self, itemid):
        response = {
            "valid": True,
            "errors": [],
            "quoter": None,
        }
        quote = Quote.objects.get(id=itemid)
        Quote.objects.remove(quote)
        return response
    def unwant(self, itemid, id):
        print itemid
        quote = Quote.objects.get(id=itemid)
        user = User.objects.get(id=id)
        quote.quoters.remove(user)
        return (quote)
class Quote(models.Model):
    quotedby = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(User, related_name="adding")
    quoters = models.ManyToManyField(User, related_name="quoter")
    objects = QuoteManager()
