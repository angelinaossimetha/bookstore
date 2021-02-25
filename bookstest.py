#new new submit 12/11
from testlight import *
from books import *

def test_setup():
    book_HT[1] = Book(title='Bobby: My Story in Pictures', author='Bobby Orr',
                      genre='Arts & Photography', img_url='https://images-na.ssl-images-amazon.com/'
                                                          'images/I/A18ahXUBrGL._SL500_SR200,200_.jpg',
                      rating=4.4, reviews=7, ident=0)
    book_HT[2] = Book(title='Bob Ross Bobblehead: With Sound!', author='Bob Ross',
                      genre='Arts & Photography', img_url='https://images-na.ssl-images-amazon.'
                                                          'com/images/I/615SY61-25L._SL500_SR200,200_.jpg',
                      rating=4.7, reviews=32, ident=1)
    book_HT[3] = Book(title="John Sloane's Country Seasons 2019 Deluxe Wall Calendar",
                      author='John Sloane', genre='Arts & Photography', img_url='https://images-na.'
                                                                                'ssl-images-amazon.com/'
                                                                                'images/I/91Mieh0NaCL._SL500_SR200,'
                                                                                '200_.jpg', rating=5.0,
                      reviews=1, ident=100)
    book_HT[4] = Book(title='O.M.G. Glamour Squad: Coloring Book (Volume 1)',
                      author='Books Plus', genre='Arts & Photography', img_url='https://images-na.ssl-'
                                                                               'images-amazon.com/images'
                                                                               '/I/51wLxHL5z7L._SL500_'
                                                                               'SR200,200_.jpg',
                      rating=None, reviews=None, ident=5)
    book_HT[5] = Book(title='The Heir: A Contemporary Royal Romance',
                      author='Georgia Le Carre', genre='Romance',
                      img_url='https://images-na.ssl-images-amazon.com/images/I/'
                              '91HPzwVQ%2BNL._SL500_UX300_PJku-sticker-v7,TopRight,0,-50_OU15__'
                              'BG0,0,0,0_FMpng_SR200,200_.jpg', rating=4.5, reviews=9, ident=15000)

def tests():
    #tests for functions in books.py go here"""
    # note: your setup function has not yet been run. this allows you to work
    #       with a smaller dataset for testing if you would like. or you
    #       can uncomment this line to have your setup() function run.
    test_setup()

    rec_output = [book_HT[3],book_HT[4]]
    list_bookscores = [Bookscore(book_HT[1],0), Bookscore(book_HT[2],0)]
    list_bookscores1 = [Bookscore(book_HT[1],1), Bookscore(book_HT[2],1)]
    list_bookscores2 = [Bookscore(book_HT[1],2), Bookscore(book_HT[2],3)]
    purchased_book = book_HT[3]

    #testing removing one item if the purchased Book is in list scores

    compute_score(list_bookscores, purchased_book)
    test("computing score", list_bookscores , list_bookscores1)
    compute_score(list_bookscores, book_HT[2])
    test("compute score2", list_bookscores, list_bookscores2)
    add_book_to_cart(1)
    add_book_to_cart(2)


    #testing function add to cart; see if cart updates

    test("testing for adding books in cart", cart, {1 : book_HT[1],
                                                    2 : book_HT[2]})
    remove_bookscore(list_bookscores, book_HT[1])
    test("removed bookscore",list_bookscores, [Bookscore(book_HT[2],3)])

    #test that removes Books out of dict cart

    buy_books_in_cart()
    test("testing cart after buy_books_in_cart() has been called", cart, {})

    #test transferring Books to purchase list

    test("book 1 and 2 should now be in purchases", get_purchases(),
         [book_HT[1], book_HT[2]])

    #test that outputs the correct recommendations given purchased books

    test("test for general case for recommendation",
         get_recommendations(), rec_output)

    add_book_to_cart(3)
    test("only book three should be in cart", cart, {3 : book_HT[3]})

    buy_books_in_cart()
    test("book three should be out of cart", cart, {})
    test(" test for 1 book left in recommendations", get_recommendations(),
         [book_HT[4]])

    add_book_to_cart(4)
    buy_books_in_cart()
    test("4 books should be in purchases", get_purchases(),
         [book_HT[1], book_HT[2], book_HT[3], book_HT[4]])
    test("test for no  to recommend",get_recommendations(), [])

    add_book_to_cart(5)
    buy_books_in_cart()
    test("all books should be in purchases", get_purchases(),
         [book_HT[1], book_HT[2], book_HT[3], book_HT[4], book_HT[5]])

    #given that all books are bought, no recommendations should be displayed

    test("test for one book  to recommend", get_recommendations(), [])



if __name__ == '__main__':
    tests()  # run tests if running file directly, as opposed to importing
