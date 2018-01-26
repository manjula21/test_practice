from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from time import gmtime, strftime
from .models import User
from .models import Book
from .models import Author
from .models import Review

def index(request):
	print "I am in index of dashboard app ***"
  
	response = "Hello, I am your first request!"
	return render(request,'review_app/index.html')

def user_create(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    print "I am in index of user create ***"
    response = User.objects.validate_registration_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].name
        request.session['user_id'] = response['user'].id
        user_id = request.session['user_id'] 
        print "in if statement***"
        return redirect('/user/{}'.format(user_id))
    else:
        print "in else statement***"
        request.session['errors'] = response['errors']
        return redirect('review_app/index.html')

def user_review(request, user_id):
    print "I am in add_book_get***"

    return render(request, "review_app/user.html")

def user_login(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    response = User.objects.validate_login_data(request.POST)

    if (response['status']):
        request.session['name']    = response['user'].name
        request.session['user_id'] = response['user'].id
        request.session['errors']  = []
        user_id = request.session['user_id'] 
        #return redirect('/user/{}'.format(user_id))
        return render(request, "review_app/books.html")
    else:
        request.session['errors'] = response['errors']
        return redirect('/')

def add_book_get(request):
    print "I am in add_book_get***"
    authors = Author.objects.all()
    context = {
            'authorList' : authors,
            'user_id': request.session['user_id']
            }
  
    return render(request, "review_app/addbook.html", context)
    

def add_book_post(request):
    print "I am in add_book_post***"
    print str(request)

    response = Book.objects.validate_book_data(request.POST)
    print "response=***" + str(response)

    if (response['status']):
        request.session['errors']  = []
        request.session['book_name']    = response['book'].book_name
        
    else:
        request.session['errors'] = response['errors']
  
    return redirect('/book_review/' + str(response['book'].id) )

def book_review(request, book_id):
    print "I am in book review***"
    
    this_book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book= this_book)
    context = {
        "book" : this_book,
        "reviews" : reviews
    }

    return render(request, "review_app/book_review.html", context)
