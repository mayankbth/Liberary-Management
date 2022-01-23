from book_app.models import Book, Genre, Transaction, TransactionRecord
from book_app.models import Review as ReviewModel
from book_app.api.serializers import (BookSerializer, GenreSerializer,
                                      TransactionSerializer, TransactionRecordSerializer,
                                      ReviewSerializer)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from book_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


# defining the genres (get and post request)
class Genre_listAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# defining the genres details (get, put, delete)
class Genre_detailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response({'error': 'Gener not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# defining the books
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def book_list(request):

    if request.method == 'GET':

        book_object = Book.objects.all()
        paginator = PageNumberPagination()

        object_size = request.GET.get('size', 1)
        current_page = request.GET.get('page', 1)
        paginator.page_size = object_size

        result_page = paginator.paginate_queryset(book_object, request)

        num_objects = len(result_page)

        total_num_object = len(book_object)
        objs = int(object_size)
        remainder = total_num_object % objs
        if remainder == 0:
            total_num_page = (total_num_object // objs)
        else:
            total_num_page = (total_num_object // objs) + 1

        serializer = BookSerializer(result_page, many=True)
        context = {
            'Current Page': current_page,
            'Objects Present': num_objects,
            'Defined Objects Size Per Page': object_size,
            'Total Objects': total_num_object,
            'Total Number Of Page': total_num_page,
            'Next Page': paginator.get_next_link(),
            'Previous Page': paginator.get_previous_link(),
            'Result': serializer.data
        }
        return Response(context)

    else:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# defining the books
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def book_details(request, pk):

    if request.method == 'GET':
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    if request.method == 'PUT':
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # Defining the book reviews (get, post)
# class Review_all(generics.ListCreateAPIView):
#     queryset = ReviewModel.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)


# Defining the book reviews (get, post)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def Review_all(request):

    if request.method == 'GET':

        review = ReviewModel.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    else:

        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            obj = ReviewModel.objects.filter(review_user=request.user, book=serializer.data['book'])
            if obj == None:
                serializer.save(review_user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response('Review already, exists', serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response('Review already, exists...!')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# defining the book reviews (get, put, delete request)
class Review(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


# This is current transaction (get, post request)
class Transaction_listAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        transctions = Transaction.objects.all()
        serializer = TransactionSerializer(transctions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer_record = TransactionRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer_record.is_valid():
                serializer_record.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# This is for change in current transactions state (get, put, delete request)
class Transaction_detailsAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            transction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transction)
        return Response(serializer.data)

    def put(self, request, pk):
        transction = Transaction.objects.get(pk=pk)
        transction_record = TransactionRecord.objects.get(pk=pk)
        serializer = TransactionSerializer(transction, data=request.data)
        serializer_record = TransactionRecordSerializer(transction_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer_record.is_valid():
                serializer_record.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transction = Transaction.objects.get(pk=pk)
        transction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# This is transaction history
class Transaction_Record_listGV(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = TransactionRecord.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)


# this is for search operation (searchable api)
class All_Records(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'genre__category', 'genre__description', 'pages', 'author', 'arrived']

