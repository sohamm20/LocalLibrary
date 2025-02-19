from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from catalog.forms import RenewBookForm 
from django.views import generic

def index(request):
     # Generate counts of some of the main objects
     num_books = Book.objects.all().count()
     num_instances = BookInstance.objects.all().count()
     # Available books (status = 'a')
     num_instances_available = BookInstance.objects.filter(status__exact='a').count()
     # The 'all()' is implied by default.
     num_authors = Author.objects.count()
     num_genres = Genre.objects.count()
     num_languages = Language.objects.count()
     num_visits = request.session.get('num_visits', 0)
     request.session['num_visits'] = num_visits + 1 
     

     context = {
         'num_books': num_books,
         'num_instances': num_instances,
         'num_instances_available': num_instances_available,
         'num_authors': num_authors,
         'num_genres': num_genres,
         'num_languages': num_languages,
         'num_visits': num_visits,
     }

     # Render the HTML template index.html with the data in the context variable
     return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'book_list'     # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5]  
    #template_name = 'books/book_list.html'
    
    #def get_queryset(self):
        #return Book.objects.filter(title__icontains='war')[:5]

    #def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        #context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        ##return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
 
#only visible to users with can_mark_returned permission
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog/can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    form_class = RenewBookForm
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    form = form_class(request.POST)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
