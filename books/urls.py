from django.urls import path

from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BooksListView.as_view(), name='bookslist'),
    # path('<int:pk>/', views.BookDetailView.as_view(), name='bookdetail'),
    path('create/', views.BookCreateView.as_view(), name='bookcreate'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='bookupdate'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='bookdelete'),
]