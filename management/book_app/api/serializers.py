from rest_framework import serializers
from book_app.models import Book, Genre, Transaction, TransactionRecord, Review


""" serializers.ModelSerializer """


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class TransactionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionRecord
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    # # Custom Serializer Field
    # len_title = serializers.SerializerMethodField()

    # # Nested Serializer
    # transction = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        # fields = ['id', 'title', 'author']
        # exclude = ['description']

    # # Custom Serializer Field
    # def get_len_title(self, object):
    #     length = len(object.title)
    #     return length
    #
    #
    # """Validation"""
    #
    # # Object Level Validation
    # def validate(self, data):
    #     if data['title'] == data['description']:
    #         raise serializers.ValidationError("Title and Description should be different!")
    #     else:
    #         return data
    #
    # # Field Level Validation
    # def validate_title(self, value):
    #
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value


class GenreSerializer(serializers.ModelSerializer):
    # Nested Serializer
    book = BookSerializer(many=True, read_only=True)

    # # String Related Field
    # book = serializers.StringRelatedField(many=True)

    # # HyperlinkedRelatedField
    # book = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='book-details'
    # )


    class Meta:
        model = Genre
        fields = "__all__"


""" serializers.Serializer """
#
#
# """ Validation """
#
# # Validator
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
#
#
# class BookSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     pages = serializers.IntegerField()
#     author = serializers.CharField()
#
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.pages = validated_data.get('pages', instance.pages)
#         instance.author = validated_data.get('author', instance.author)
#         instance.save()
#         return instance
#
#
#     """Validation"""
#
#     # Object Level Validation
#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different!")
#         else:
#             return data
#
#     # # Field Level Validation
#     # def validate_title(self, value):
#     #
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value

