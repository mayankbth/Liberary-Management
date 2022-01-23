from django.urls import path
from book_app.api.views import (book_list, book_details, Genre_listAV, Genre_detailsAV,
                                Transaction_listAV, Transaction_detailsAV,
                                Transaction_Record_listGV,
                                All_Records, Review_all, Review)

urlpatterns = [
    path('list/', book_list, name='book-list'),
    path('list/<int:pk>/', book_details, name='book-details'),
    path('genre/list/', Genre_listAV.as_view(), name='Genre-list'),
    path('genre/<int:pk>/', Genre_detailsAV.as_view(), name='Genre-details'),
    path('transction/list/', Transaction_listAV.as_view(), name='Transaction-list'),
    path('transction/<int:pk>/', Transaction_detailsAV.as_view(), name='Transaction-details'),
    path('transction/record/', Transaction_Record_listGV.as_view(), name='transaction-record-list'),
    # path('review/', Review_all.as_view(), name="Review-all"),
    path('review/', Review_all, name="Review-all"),
    path('review/<int:pk>/', Review.as_view(), name="Review"),

    # this is for search operation (searchable api)
    path('find/', All_Records.as_view(), name='All-Records'),
]

