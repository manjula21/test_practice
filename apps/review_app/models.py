from __future__ import unicode_literals
from django.db import models
from django.contrib import messages

import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


# Create your models here.
class UserManager(models.Manager):
    def validate_registration_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['name']) < 2:
            errors.append("Name must be at least 2 characters long")

        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Name may only contain characters')

        if len(post_data['alias']) < 2:
            errors.append("Alias must be at least 2 characters long")

        if not re.match(NAME_REGEX, post_data['alias']):
            errors.append('Alias may only contain characters')

        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("Email already in use")

        if post_data['password'] != post_data['pw_confirm']:
            errors.append("Passwords do not match!")

        print " before error check" + str(errors)
        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            user = User.objects.create(
                        name       = post_data['name'],
                        alias      = post_data['alias'],
                        email      = post_data['email'],
                        password   = hashedpwd)

            response['user'] = user
            print " after user " + str(user)
            
        return response

    def validate_login_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

        user = User.objects.filter(email = post_data['email'])

        if len(user) > 0:
            # check this user's password
            user = user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response

    def validate_book_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        print "+++++++++" + str(post_data['book_review'])

        if len(post_data['book_name']) < 2:
            errors.append("Book name must be at least 2 characters long")
        if len(post_data['book_review']) < 2:
            errors.append("Review must be at least 2 characters long")
        else:
            if post_data['Author'] == "Empty":          
            	this_author = Author.objects.create(
            		author_name       = post_data['author_name'])
            else:
            	this_authors = Author.objects.filter(author_name = post_data['Author'])
            	this_author = this_authors[0]
            	print "this_author =" + str(this_author)
            
            #print "before this book " + str(this_author[0])
            this_book = Book.objects.create(
            	book_name       = post_data['book_name'],
            	author = this_author)

            user = User.objects.get(id=post_data['user_id'])
            print "user=" + str(user) + " userid=" + str(post_data['user_id'])
            review = Review.objects.create(
            	review = post_data['book_review'],
    			review_rating = post_data['rating'],
    			book = this_book,
    			user = user
            	)
                       

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['book'] = this_book
            response['author'] = this_author
            response['review'] = review

        return response


# database models
class User(models.Model):
    name        = models.CharField(max_length=255)
    alias       = models.CharField(max_length=255)
    email       = models.EmailField(unique=True)
    password    = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.email
    
class Author(models.Model):
    author_name = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.book_name

class Review(models.Model):
    review = models.CharField(max_length=255)
    review_rating = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name="reviews")
    user =models.ForeignKey(User, related_name="reviews")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()
    def __str__(self):
        return self.review

