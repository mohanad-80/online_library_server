from django.db import models
# from django.contrib.auth import get_user_model
from authentication.models import CustomUser


class Book(models.Model):
    ISBN = models.CharField(max_length=255, unique=True)
    availability = models.BooleanField(default=True)
    bookCover = models.TextField()
    bookGenres = models.TextField()
    bookPlot = models.TextField()
    bookTitle = models.CharField(max_length=255)
    bookAuthor = models.CharField(max_length=255)
    language = models.CharField(max_length=30)
    numOfPages = models.PositiveIntegerField()  # check if there is an error when validating
    publishDate = models.CharField(max_length=15)


class BorrowedBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowDate = models.DateField()  # auto_now_add=True
    returnDate = models.DateField()
