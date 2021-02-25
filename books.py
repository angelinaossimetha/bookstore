#new submit 12/11
import csv    # https://docs.python.org/3/library/csv.html
import random # https://docs.python.org/3/library/random.html
from dataclasses import dataclass

with open('books.csv', encoding='utf-8') as f:
    lines = list(csv.reader(f))  # loads lines of books.csv into list of lists

with open('genres.txt') as f:
    # loads list of genres to display on main page into list of strings
    # we have this list because otherwise there are too many books to display
    # and the website will get overloaded. Feel free to edit genres.txt!
    display_genres = list(map(str.strip, f.read().strip().split('\n')))



# frozen=True makes Books immutable (in other words, after you
# create them, you cannot change them). This allows you to use
# books as the keys in a hashtable if you want: {Book(...): 3, ...}
@dataclass(frozen=True)
class Book:
    # ** do not modify this dataclass **
    title   : str
    author  : str
    genre   : str
    img_url : str
    rating  : float # out of 5 stars
    reviews : int   # number of reviews on amazon
    ident   : int   # identifier

@dataclass
class Bookscore:
    book : Book
    score : int

######################
## Helper functions ##
######################

def create_bookHT(lst : list) -> dict:
    """Takes in a list<list<String>> of which
    there are fields within each list (referring
    to list within mega list that corresponds to
    the Book dataclass fields). For each element
    in the list it creates a Book, adding all the
    elements into a hashtable. Returns the
    hashtable/dict"""

    identifier = 0


    for elt in lst :
        if (elt[4] == '') and (elt[5] == ''):
            book_HT[identifier] = Book(elt[0],elt[1],elt[2],
                                       elt[3],None,None,identifier)
            identifier += 1
        elif (elt[4] == ''):
            book_HT[identifier] = Book(elt[0],elt[1],elt[2],
                                       elt[3],None,int(elt[5]),identifier)
            identifier += 1
        elif (elt[5] == ''):
            book_HT[identifier] = Book(elt[0],elt[1],elt[2],
                                       elt[3],float(elt[4]),None,identifier)
            identifier += 1
        else:
            book_HT[identifier] = Book(elt[0],elt[1],elt[2],elt[3],
                                       float(elt[4]),int(elt[5]),identifier)
            identifier += 1

def create_book_list(hash_table : dict) -> list:
    """Takes in a dict/hashtable(with key =
    identifier and value = Book) as input and
    returns a sorted list<Bookscores> based on
    the books rating"""

    bookss = []
    for id in hash_table:
        bookss.append(Bookscore(hash_table[id],0))
    return sorted(bookss,key=lambda b:
    -1 if b.book.rating == None else b.book.rating, reverse = True)

######################
## Global variables ##
######################

book_HT = {}#Book_HT transfer
# all the books in csv document into hashtable ht

recommendations : list =  [] #Book

purchase : list = [] #books

genre_HT : dict = create_bookHT(lines)

cart : dict = {} #books

book_list = create_book_list(book_HT) #for all books in Book_HT,
#  they are placed into a list of books

hold_recommendations = [] #list of Bookscore

######################
## Helper function ##
######################

def genreto_books(book_dict : dict) -> dict:
    """Takes in two dicts which represents a genre dic
     and a book dic respectively. Returns  """
    genre_dict = {}
    for subject in  display_genres:
        genre_dict[subject] = []

    for elt in book_dict:
        book_genre = book_dict[elt].genre
        if book_genre in genre_dict:
            genre_dict[book_genre].append(book_dict[elt])
    return genre_dict

######################
## Global variables ##
######################

genre_HT = genreto_books(book_HT)
book_HT = {}

def setup():
    """ procedure to setup any global variables (
    which must be defined
    above this function). """

    create_bookHT(lines)
    book_list = create_book_list(book_HT)
    genre_HT = genreto_books(book_HT)

def get_cart() -> list:
    """ return current representation of the cart. """
    global cart

    return cart.values()


def get_recommendations() -> list:
    """
    return current recommendations, in order of how r
    ecommended the book is
    """
    global recommendations

    rec_length = len(recommendations)

    if rec_length <= 0:
        return []
    return recommendations


def get_book(identifier: int) -> Book:
    """ given a book id (integer), return the Book
    corresponding to that id """
    global book_HT

    return book_HT[identifier]



def add_book_to_cart(ident: int):
    """ given the ident of a book, add the corresponding
     book to the cart. no return required. """
    global cart, book_HT

    cart[ident] = book_HT[ident]

def remove_book_from_cart(ident: int):
    """ given the ident of a book, remove the corresponding
    book from the cart. no return required """
    global cart

    del cart[ident]


def compute_score(rec_list : list ,purchased_book : Book):
    """Takes in a list of Bookscores and updates the
    Bookscore's score based on the purchased_book"""
    for b in rec_list:
        if purchased_book.genre == b.book.genre:
            b.score += 1
        if purchased_book.author == b.book.author:
            b.score += 1


def remove_bookscore(rec_list : list,purchased_book : Book):
    """Takes in a list<Bookscores> and a Book. Updates (removes
    a book from list) the inputted list if the inputed
    Book exist in the inputed list"""

    for bookscore in rec_list:
        if purchased_book == bookscore.book:
            rec_list.remove(bookscore)
            break


def buy_books_in_cart():
    """ purchase all books in cart. update cart, previous purchases,
    books, recommendations as required. no return required. """
    global cart, purchase, recommendations,hold_recommendations
    #for loop goes through cart add books to purchase and remove from cart
    #create helper function to compute recommedation scorces,update book_list
    #with new recommedations

    if len(purchase) == 0:
        hold_recommendations = create_book_list(book_HT)

    for id in cart:
        purchase.append(cart[id])
        remove_bookscore(hold_recommendations,cart[id])
        compute_score(hold_recommendations,cart[id])
    hold_recommendations.sort(key=lambda elt: elt.score, reverse=True)

    hold_rec_length = len(hold_recommendations)
    recommendations = []

    if hold_rec_length >= 50:
        for index in range(50):
            if hold_recommendations[index].score > 0:
                recommendations.append(hold_recommendations[index].book)
    else:
            for ind in range(hold_rec_length):
                if hold_recommendations[ind].score > 0:
                    recommendations.append(hold_recommendations[ind].book)
    cart.clear()

def search_books(query: str) -> list:
    """ given a query string, return list of matching Books """
    global book_list

    lower_query = query.lower()

    searched_books = []

    for elt in book_list:
        if (len(searched_books) < 50) and \
                ((lower_query in elt.book.author.lower()) or
            (lower_query in elt.book.genre.lower()) or
            (lower_query in elt.book.title.lower())):

           searched_books.append(elt.book)

    return searched_books

def get_book_dict() -> dict:
    """ return a dictionary of genre -> list of books.
    use random.sample to randomly choose some books to display
    for each genre. do not allow the number of books in any given
    genre to be greater than 25 (or the website will be overwhelmed)
    there should be one key for each genre in display_genres
    (loaded @ top) """
    global genre_HT


    temp = {}

    for elt in genre_HT:
        if len(genre_HT[elt]) >= 20:
            temp[elt] = random.sample(genre_HT[elt], 20)
        else:
            temp[elt] = genre_HT[elt]
    return temp

def get_purchases() -> list:
    global purchase
    return purchase

