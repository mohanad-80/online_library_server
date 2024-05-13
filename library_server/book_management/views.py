import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book


@csrf_exempt
def getAll(request):
    if request.method == "GET":
        books = Book.objects.all()
        serialized_books = [
            {
                "id": book.id,
                "ISBN": book.ISBN,
                "availability": book.availability,
                "bookCover": book.bookCover,
                "bookGenres": book.bookGenres.split(","),
                "bookPlot": book.bookPlot,
                "bookTitle": book.bookTitle,
                "bookAuthor": book.bookAuthor,
                "language": book.language,
                "numOfPages": book.numOfPages,
                "publishDate": book.publishDate,
            }
            for book in books
        ]
        return JsonResponse(serialized_books, safe=False)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Assuming genres are passed as an array in the request body
        genres = data.get("bookGenres", [])
        # print(genres)
        # Convert the list of genres to a comma-separated string
        genres_str = ",".join(genres)

        # Create a new book instance with other fields
        book = Book.objects.create(
            ISBN=data.get("ISBN"),
            availability=data.get("availability", True),
            bookCover=data.get("bookCover"),
            bookGenres=genres_str,
            bookPlot=data.get("bookPlot"),
            bookTitle=data.get("bookTitle"),
            bookAuthor=data.get("bookAuthor"),
            language=data.get("language"),
            numOfPages=data.get("numOfPages"),
            publishDate=data.get("publishDate"),
        )

        # Return a success response
        return JsonResponse({"message": "Book added successfully"}, status=201)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def getOne(request, book_id):
    if request.method == "GET":
        try:
            # Retrieve the book object based on the provided book_id
            book = Book.objects.get(pk=book_id)

            # Convert the book object into a dictionary format
            book_data = {
                "id": book.id,
                "ISBN": book.ISBN,
                "availability": book.availability,
                "bookCover": book.bookCover,
                "bookGenres": book.bookGenres.split(","),
                "bookPlot": book.bookPlot,
                "bookTitle": book.bookTitle,
                "bookAuthor": book.bookAuthor,
                "language": book.language,
                "numOfPages": book.numOfPages,
                "publishDate": book.publishDate,
            }

            # Return the book data as a JSON response
            return JsonResponse(book_data)

        except Book.DoesNotExist:
            # Handle the case where the book with the provided ID does not exist
            return JsonResponse({"error": "Book not found"}, status=404)
    else:
        # Handle the case where the request method is not GET
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def edit(request, book_id):
    if request.method == "POST":
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        genres = data.get("bookGenres", [])
        genres_str = ",".join(genres)

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return HttpResponse("Book not found", status=404)

        # Update the book object with the new data
        book.ISBN = data.get("ISBN", book.ISBN)
        book.availability = data.get("availability", book.availability)
        book.bookCover = data.get("bookCover", book.bookCover)
        book.bookGenres = genres_str
        book.bookPlot = data.get("bookPlot", book.bookPlot)
        book.bookTitle = data.get("bookTitle", book.bookTitle)
        book.bookAuthor = data.get("bookAuthor", book.bookAuthor)
        book.language = data.get("language", book.language)
        book.numOfPages = data.get("numOfPages", book.numOfPages)
        book.publishDate = data.get("publishDate", book.publishDate)

        # Save the updated book object
        book.save()

        return HttpResponse("Book updated successfully", status=200)

    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def delete(request, book_id):
    if request.method == "POST":
        # Try to get the book object with the provided book_id
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return HttpResponse("Book not found", status=404)

        # Delete the book object from the database
        book.delete()

        return HttpResponse("Book deleted successfully", status=200)

    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def search(request):
    if request.method == "POST":
        data = json.loads(request.body)
        search_string = data.get("searchString", "")
        genres = data.get("genres", [])

        # If both search string and genres are empty, return an empty result
        if not search_string and not genres:
            return JsonResponse([], safe=False)

        # Filter books based on search string and genres
        if search_string:
            books = Book.objects.filter(
                bookTitle__icontains=search_string
            ) | Book.objects.filter(bookAuthor__icontains=search_string)
        else:
            books = Book.objects.all()

        if genres:
            # Filter books by genres if genres are provided
            for genre in genres:
                books = books.filter(bookGenres__icontains=genre)

        # Prepare data for JSON response
        books_data = [
            {
                "id": book.id,
                "ISBN": book.ISBN,
                "availability": book.availability,
                "bookCover": book.bookCover,
                "bookGenres": book.bookGenres.split(","),
                "bookPlot": book.bookPlot,
                "bookTitle": book.bookTitle,
                "bookAuthor": book.bookAuthor,
                "language": book.language,
                "numOfPages": book.numOfPages,
                "publishDate": book.publishDate,
            }
            for book in books
        ]

        return JsonResponse(books_data, safe=False)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def getAvailable(request):
    if request.method == "GET":
        available_books = Book.objects.filter(availability=True)
        books_data = [
            {
                "id": book.id,
                "ISBN": book.ISBN,
                "availability": book.availability,
                "bookCover": book.bookCover,
                "bookGenres": book.bookGenres.split(","),
                "bookPlot": book.bookPlot,
                "bookTitle": book.bookTitle,
                "bookAuthor": book.bookAuthor,
                "language": book.language,
                "numOfPages": book.numOfPages,
                "publishDate": book.publishDate,
            }
            for book in available_books
        ]

        return JsonResponse(books_data, safe=False)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def borrow(request, book_id):
    if request.method == "POST":
        try:
            # Get the book object based on the provided book_id
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        # Extract user_id, borrow date, and return date from the request body
        data = json.loads(request.body)
        user_id = data.get("user_id")
        borrow_date = data.get("borrow_date")
        return_date = data.get("return_date")

        try:
            # Get the user object based on the provided user_id
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Perform the borrowing operation by updating book's availability
        book.availability = False  # Book is now borrowed
        book.save()

        # Add a record to the BorrowedBook model
        borrowed_book = BorrowedBook.objects.create(
            user=user, book=book, borrowDate=borrow_date, returnDate=return_date
        )

        # Return a success response
        return JsonResponse({"message": "Book borrowed successfully"}, status=200)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def getBorrowed(request, user_id):
    if request.method == "GET":
        try:
            # Get the user object based on the provided user_id
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Get all borrowed books for the user
        borrowed_books = BorrowedBook.objects.filter(user=user)

        # Serialize the borrowed books data
        borrowed_books_data = [
            {
                "id": borrowed_book.id,
                "book": {
                    "id": borrowed_book.book.id,
                    "ISBN": borrowed_book.book.ISBN,
                    "availability": borrowed_book.book.availability,
                    "bookCover": borrowed_book.book.bookCover,
                    "bookGenres": borrowed_book.book.bookGenres.split(","),
                    "bookPlot": borrowed_book.book.bookPlot,
                    "bookTitle": borrowed_book.book.bookTitle,
                    "bookAuthor": borrowed_book.book.bookAuthor,
                    "language": borrowed_book.book.language,
                    "numOfPages": borrowed_book.book.numOfPages,
                    "publishDate": borrowed_book.book.publishDate,
                },
                "borrowDate": borrowed_book.borrowDate,
                "returnDate": borrowed_book.returnDate,
            }
            for borrowed_book in borrowed_books
        ]

        # Return the borrowed books data as JSON response
        return JsonResponse(borrowed_books_data, safe=False)
    else:
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


# from django.middleware.csrf import get_token
# from django.http import JsonResponse

# def signup(request):
#     # Process signup request and save user data
#     # Generate CSRF token for the user's session
#     csrf_token = get_token(request)
#     # Return JSON response with CSRF token
#     return JsonResponse({'csrf_token': csrf_token})

# # Return response with CSRF token set as a header
#     response = HttpResponse()
#     response['X-CSRFToken'] = csrf_token
#     return response


# else:
#         # Handle GET requests
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
