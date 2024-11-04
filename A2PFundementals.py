from enum import Enum

# Enum for currency to use variation for customer
class Currency(Enum):
    USD = "USD"
    AED = "AED"

# EBook class
class EBook:
    def __init__(self, title, author, publicationDate, genre, price):
        self.__title = title
        self.__author = author
        self.__publicationDate = publicationDate
        self.__genre = genre
        self.__price = price

    def getPrice(self):
        return self.__price

    def __str__(self):
        return "Title: " + self.__title + ", Author: " + self.__author + ", Published: " + self.__publicationDate + ", Genre: " + self.__genre

# Customer class
class Customer:
    def __init__(self, customerID, name, contactInfo):
        self.__customerID = customerID
        self.__name = name
        self.__contactInfo = contactInfo

    def getDiscount(self):
        return 0  # Normal customers have no discount

    def createAccount(self):
        return self.__customerID

    def __str__(self):
        return "Customer ID: " + self.__customerID + ", Name: " + self.__name + ", Contact: " + self.__contactInfo

# LoyaltyCardCustomer inherits from Customer
class LoyaltyCardCustomer(Customer):
    def __init__(self, customerID, name, contactInfo, loyaltyCardNumber, discountRate=10):
        super().__init__(customerID, name, contactInfo)
        self.__loyaltyCardNumber = loyaltyCardNumber
        self.__discountRate = discountRate

    def getDiscount(self):
        return self.__discountRate

    def __str__(self):
        return super().__str__() + ", Loyalty Card Number: " + self.__loyaltyCardNumber

# ShoppingCart class (Composition with Customer)
class ShoppingCart:
    def __init__(self, customerID):
        self.__customerID = customerID
        self.__books = []

    def addBook(self, ebook):
        self.__books.append(ebook)
        print("Book added:", ebook)

    def removeBook(self, ebook):
        if ebook in self.__books:
            self.__books.remove(ebook)
            print("Book removed:", ebook)
        else:
            print("Book not in cart")

    def calculateTotal(self):
        total = sum(book.getPrice() for book in self.__books)
        return total

    def __str__(self):
        return "ShoppingCart for Customer ID: " + self.__customerID + ", Books: " + str([str(book) for book in self.__books])

# Order class (Composition with Customer, Aggregation with EBook)
class Order:
    def __init__(self, customer):
        self.__customer = customer
        self.__books = []
        self.__totalPrice = 0
        self.__discountAmount = 0

    def addBook(self, ebook):
        self.__books.append(ebook)

    def removeBook(self, ebook):
        if ebook in self.__books:
            self.__books.remove(ebook)
            print("Book removed:", ebook)
        else:
            print("Book not in order")

    def calculateTotal(self):
        self.__totalPrice = sum(book.getPrice() for book in self.__books)
        return self.__totalPrice

    def applyDiscountIfEligible(self):
        # Apply discount only for LoyaltyCardCustomer
        discountRate = self.__customer.getDiscount()
        if discountRate > 0:
            self.__discountAmount = self.__totalPrice * (discountRate / 100)
            self.__totalPrice -= self.__discountAmount
        return self.__totalPrice

    def generateInvoice(self):
        self.calculateTotal()  # Initial total calculation
        print("Invoice for Customer:", self.__customer)
        for book in self.__books:
            print(book)
        print("Total Price before discount:", self.__totalPrice)

        # Apply discount if applicable
        final_price = self.applyDiscountIfEligible()

        print("Discount Applied:", self.__discountAmount)
        print("Final Price after discount:", final_price)
        return final_price

    def __str__(self):
        return "Order for Customer: " + str(self.__customer) + ", Books: " + str(
            [str(book) for book in self.__books]) + ", Total Price: " + str(self.__totalPrice) + ", Discount: " + str(self.__discountAmount)

# Payment class (Composition with Order)
class Payment:
    def __init__(self, amount, paymentMethod, currency=Currency.AED):
        # Corrected conversion: If currency is USD, convert from AED to USD
        self.__amount = amount / (3.67 if currency == Currency.USD else 1)
        self.__paymentMethod = paymentMethod
        self.__currency = currency.value

    def processPayment(self):
        print("Payment processed:", self.__amount, self.__currency)
        print("Payment Method:", self.__paymentMethod)

    def __str__(self):
        return "Payment of: " + str(self.__amount) + " " + self.__currency + " via " + self.__paymentMethod

# Example Usage
ebook1 = EBook("Climate of Shani", "Shani Almuharrami", "2004", "Historical Fiction", 80)
ebook2 = EBook("Life is weird", "Ali Mohamed", "2018", "Fiction", 70)

# Regular Customer (no discount)
regular_customer = Customer("C202215016", "Abdulaziz Omar", "202215016@zu.ac.ae")
order = Order(regular_customer)
order.addBook(ebook1)
order.addBook(ebook2)

# Removing one book from the order
order.removeBook(ebook2)  # Remove the second book

# continue with generating the invoice and payment
final_price_regular = order.generateInvoice()
payment = Payment(final_price_regular, "Credit Card", Currency.AED)
payment.processPayment()

# Loyalty Card Customer (eligible for discount)
loyalty_customer = LoyaltyCardCustomer("C202215017", "Khalid Alkaabi", "202215017@zu.ac.ae", "L202215017", 10)
order2 = Order(loyalty_customer)
order2.addBook(ebook1)
order2.addBook(ebook2)

final_price_loyalty = order2.generateInvoice()
payment2 = Payment(final_price_loyalty, "Credit Card", Currency.USD)
payment2.processPayment()
