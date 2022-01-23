from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# from book_app.api.views import user_id_value

import datetime


class Genre(models.Model):
    category = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.category


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='book')
    pages = models.IntegerField()
    author = models.CharField(max_length=100)
    arrived = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title


class Transaction(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phoneNumber = PhoneNumberField(unique=False, null=False, blank=False)
    email = models.EmailField(unique=False)
    book_title = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transction')
    borrowed = models.DateField()
    allowed = models.DateField(null=True, blank=True)
    submitted = models.DateField(null=True, blank=True)
    late_fee = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.user_id + " | " + self.name

    def save(self, *args, **kwargs):
        duration = self.borrowed + datetime.timedelta(days=15)
        self.allowed = duration

        self.book_title = str(self.book)

        if self.submitted != None:
            late = self.submitted - self.allowed
            fee = late.days * 10
            self.late_fee = fee

        super().save(*args, **kwargs)


class TransactionRecord(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phoneNumber = PhoneNumberField(unique=False, null=False, blank=False)
    email = models.EmailField(unique=False)
    book_title = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed = models.DateField()
    allowed = models.DateField(null=True, blank=True)
    submitted = models.DateField(null=True, blank=True)
    late_fee = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        duration = self.borrowed + datetime.timedelta(days=15)
        self.allowed = duration

        self.book_title = str(self.book)

        if self.submitted != None:
            late = self.submitted - self.allowed
            fee = late.days * 10
            self.late_fee = fee

        super().save(*args, **kwargs)

class Review(models.Model):
    # review_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # review_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    # def save(self, request, obj):
    #     obj.added_by = request.user
    #     super().save(request, obj)

    # def save(self, request, *args, **kwargs):
    #     self.review_user = request.user
    #     print(request.user)
    #     super().save(*args, **kwargs)

