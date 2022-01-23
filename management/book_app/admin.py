from django.contrib import admin
from book_app.models import Book, Genre, Transaction, TransactionRecord, Review

# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Transaction)
admin.site.register(TransactionRecord)
admin.site.register(Review)

