class Library:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.collection = []

    def add_volume(self, volume):
        if volume.library is not self:
            print('This volume belongs to another library')
        elif volume in self.collection:
            print('This volume is already in the library\'s collection.')
        elif volume.borrowed:
            print('It\'s not possible to add a borrowed volume to the library\'s collection')
        else:
            self.collection.append(volume)

    def remove_volume(self, volume):
        if volume.library is not self:
            print('This volume belongs to another library')
        elif volume not in self.collection:
            print('Volume not found in the library\'s collection')
        elif volume.borrowed:
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
            status = 'Borrowed' if volume.borrowed else 'Available'
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
        available_volumes = [volume for volume in self.collection if not volume.borrowed]
        self._display_volumes(available_volumes, empty_message='No available volumes in the library\'s collection.')

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

class Volume:
    def __init__(self, number, library, book, borrowed=False):
        self.number = number
        self.library = library
        self.book = book
        self.borrowed = borrowed

class User:
    def __init__(self, name, membership_number):
        self.name = name
        self.membership_number = membership_number
        self.borrowed_volumes = []

    def borrow_volume(self, volume):
        if volume not in volume.library.collection:
            print(f'Volume not available at {volume.library.name}')
        elif volume.borrowed:
            print('Volume is already borrowed.')
        else:
            self.borrowed_volumes.append(volume)
            volume.borrowed = True

    def return_volume(self, volume):
        if volume in self.borrowed_volumes:
            self.borrowed_volumes.remove(volume)
            volume.borrowed = False
        else:
            print('This volume is not borrowed by this user.')

    def list_borrowed_volumes(self):
        if self.borrowed_volumes:
            print(f'Borrowed volumes by {self.name}:')
            print(f'{"Number":<10}{"Title":<30}{"Author":<20}{"ISBN":<15}{"Library":<20}')
            for volume in self.borrowed_volumes:
                print(f'{volume.number:<10}{volume.book.title:<30}{volume.book.author:<20}{volume.book.isbn:<15}{volume.library.name:<20}')
        else:
            print(f'{self.name} has no borrowed books.')