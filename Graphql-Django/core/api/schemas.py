import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book

class Query(graphene.ObjectType):
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())
    bookAuthor = graphene.List(BookType, author=graphene.String())

    def resolve_books(self, info):
        requests=info.context
        return Book.objects.all()

    def resolve_book(self, info, id):
        try:
            requests=info.context
            print(requests)
            print(id)
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return None
    
    def resolve_bookAuthor(self, info, author):
        try:
            requests=info.context
            print(requests)
            print(author)
            return Book.objects.filter(author=author)
        except Book.DoesNotExist:
            return None
    

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_year = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, published_year):
        book = Book(title=title, author=author, published_year=published_year)
        book.save()
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        author = graphene.String()
        published_year = graphene.Int()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title=None, author=None, published_year=None):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return UpdateBook(book=None)

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if published_year is not None:
            book.published_year = published_year

        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    book_id = graphene.Int()

    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)
            book_id = book.id
            book.delete()
            return DeleteBook(book_id=book_id)
        except Book.DoesNotExist:
            return DeleteBook(book_id=None)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
