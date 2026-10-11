from datetime import date, timedelta

class Library:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.collection = []
        self.loans = []

    def add_volume(self, volume):
        if volume.library is not self:
            print('This volume belongs to another library')
        elif volume in self.collection:
            print('This volume is already in the library\'s collection.')
        elif volume.library.is_volume_borrowed(volume):
            print('It\'s not possible to add a borrowed volume to the library\'s collection')
        else:
            self.collection.append(volume)

    def remove_volume(self, volume):
        if volume.library is not self:
            print('This volume belongs to another library')
        elif volume not in self.collection:
            print('Volume not found in the library\'s collection')
        elif volume.library.is_volume_borrowed(volume):
            print('It\'s not possible to remove a borrowed volume')
        else:
            self.collection.remove(volume)

    def _display_volumes(self, volumes, empty_message='No volumes found.'):
        if not volumes:
            print(empty_message)
            return
        print(f'Volumes in {self.name}:')
        print(f'{"Number":<10}{"Title":<30}{"Author":<20}{"ISBN":<15}{"Status":<10}')
        for volume in volumes:
            status = 'Borrowed' if volume.library.is_volume_borrowed(volume) else 'Available'
            print(f'{volume.number:<10}{volume.book.title:<30}{volume.book.author:<20}{volume.book.isbn:<15}{status:<10}')
        
    def search_volume(self, title):
        volumes_found = [volume for volume in self.collection if title.lower() in volume.book.title.lower()]
        self._display_volumes(volumes_found, empty_message='No volumes found with the given title.')

    def search_author(self, author):
        volumes_found = [volume for volume in self.collection if author.lower() in volume.book.author.lower()]
        self._display_volumes(volumes_found, empty_message='No volumes found by the given author.')

    def list_volumes(self):
        self._display_volumes(self.collection, empty_message='No volumes in the library\'s collection.')

    def list_available_volumes(self):
        available_volumes = [volume for volume in self.collection if not volume.library.is_volume_borrowed(volume)]
        self._display_volumes(available_volumes, empty_message='No available volumes in the library\'s collection.')

    def is_volume_borrowed(self, volume):
        return any(loan.volume is volume and loan.return_date is None for loan in self.loans)

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

class Volume:
    def __init__(self, number, library, book):
        self.number = number
        self.library = library
        self.book = book

class User:
    def __init__(self, name, membership_number):
        self.name = name
        self.membership_number = membership_number
        self.loans = []

    def borrow_volume(self, volume):
        if volume not in volume.library.collection:
            print(f'Volume not available at {volume.library.name}')
        elif volume.library.is_volume_borrowed(volume):
            print('Volume is already borrowed.')
        else:
            loan = Loan(self, volume)
            self.loans.append(loan)
            volume.library.loans.append(loan)
            print(f'Volume borrowed successfully. Due date: {loan.due_date}')

    def return_volume(self, volume):
        for loan in self.loans:
            if loan.volume is volume and loan.return_date is None:
                loan.return_date = date.today()
                print(f'Volume returned successfully on {loan.return_date}.')
                return
        print('This volume was not borrowed by this user.')

    def list_borrowed_volumes(self):
        active_loans = [loan for loan in self.loans if loan.return_date is None]
        if not active_loans:
            print(f'{self.name} has no borrowed books.')
            return
        print(f'Borrowed volumes by {self.name}:')
        print(f'{"Number":<10}{"Title":<30}{"Author":<20}{"ISBN":<15}{"Library":<20}')
        for loan in active_loans:
            volume = loan.volume
            print(f'{volume.number:<10}{volume.book.title:<30}{volume.book.author:<20}{volume.book.isbn:<15}{volume.library.name:<20}') 

class Loan:
    def __init__(self, user, volume, loan_days = 14):
        self.user = user
        self.volume = volume
        self.loan_date = date.today()
        self.due_date = self.loan_date + timedelta(days=loan_days)
        self.return_date = None

    def is_overdue(self):
        if self.return_date is None:
            return date.today() > self.due_date
        return self.return_date > self.due_date
    