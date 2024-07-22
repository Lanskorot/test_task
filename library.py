import json
from typing import List, Dict, Optional


class Book:
    _id_counter = 0

    def __init__(self, title: str, author: str, year: int):
        """
        Инициализация книги.
        """
        Book._id_counter += 1
        self.id = Book._id_counter
        self.title = title
        self.author = author
        self.year = year
        self.status = 'в наличии'

    def json_book(self) -> Dict[str, str]:
        """
        Преобразует в json.
        """
        return {'id': self.id,
                'title': self.title,
                'author': self.author,
                'year': self.year,
                'status': self.status}

    @classmethod
    def from_json_to_dikt(cls, json_book: Dict[str, str]) -> 'Book':
        """
        Преобразует из json в словарь .
        """
        book = cls(json_book['title'], json_book['author'], int(json_book['year']))
        book.id = int(json_book['id'])
        book.status = json_book['status']
        if book.id > cls._id_counter:
            cls._id_counter = book.id
        return book


class Library:
    def __init__(self):
        """
        Инициализация библтотеки и загрузка в файл books.json.
        """
        self.list_books: List[Book] = []
        self.load()

    def add(self, title: str, author: str, year: int):
        """
        Добавляет книгу в библиотеку.
        """
        try:
            book = Book(title, author, year)
            self.books.append(book)
            self.save()
        except Exception as ex:
            print(f"Ошибка при добавлении книги: {ex}")

    def remove(self, book_id: int) -> bool:
        """  Удаляет книгу из библиотеки по id  """
        try:
            for book in self.books:
                if book.id == book_id:
                    self.books.remove(book)
                    self.save()
                    return True
        except Exception as ex:
            print(f"Ошибка при удалении книги: {ex}")
        return False

    def find(self, title: str) -> List[Book]:
        """ Поиск по названию книги """
        results = []
        try:
            for book in self.books:
                if title.lower() in book.title.lower():
                    results.append(book)
        except Exception as ex:
            print(f"Ошибка при поиске книги: {ex}")
        return results

    def show_all(self):
        """ Выводит все книги """
        try:
            if not self.books:
                print("Книг нет")
                return
            for book in self.books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
        except Exception as ex:
            print(f"Ошибка при отображении всех книг: {ex}")

    def change_status(self, book_id: int) -> bool:
        """ меняет статус в наличии/ выдана  """
        try:
            for book in self.books:
                if book.id == book_id:
                    book.status = "выдана" if book.status == "в наличии" else "в наличии"
                    self.save()
                    return True
        except Exception as ex:
            print(f"Ошибка при изменении статуса книги: {ex}")
        return False

    def save(self):
        """ сохраняет в файл """
        try:
            with open('books.json', 'w', encoding='utf-8') as file:
                json.dump([book.json_book() for book in self.books], file, ensure_ascii=False, indent=4)
        except Exception as ex:
            print(f"Ошибка при сохранении данных: {ex}")

    def load(self):
        """ загружает из файла """
        try:
            with open('books.json', 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                self.books = [Book.from_json_to_dikt(data) for data in books_data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError as ex:
            print(f"Ошибка при загрузке данных: {ex}")
            self.books = []


def main():
    """ главная функция реализующая комуникацию с библиотекой """
    print('Добро пожаловать в библиотеку.')
    while True:
        print('Выберите что вы хотите сделать:')
        print(' Если вы хотите добавить книгу, нажмите 1')
        print(' Если вы хотите удалить книгу нажмите 2')
        print(' Если вы хотите найти какую то книгу нажмите 3')
        print(' Если вы хотите увидеть список всех книг нажмите 4')
        print(' Если вы хотите изменить статус книги нажмите 5')
        print(' Если хотите выйти нажмите 6\n')
        choice = input(' Ваш выбор: ')
        if choice == '1':
            title = input('Введите название книги: ')
            author = input('Введите автора: ')
            year = input('Введите год создания ')
            try:
                library.add(title, author, int(year))
            except ValueError:
                print("Год должен быть числом.")
            except Exception as ex:
                print(f"Ошибка: {ex}")

        elif choice == '2':
            try:
                id = int(input('Введите id книги которую нужно удалить: '))
                if library.remove(id):
                    print('Книга удалена.')
                else:
                    print('Книга с таким ID не найдена.')
            except ValueError:
                print("ID должен быть числом.")
            except Exception as ex:
                print(f"Ошибка: {ex}")

        elif choice == '3':
            find_book = input('Введите название книги: ')
            results = library.find(find_book)
            if results:
                for book in results:
                    print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
            else:
                print('Книги не найдены.')

        elif choice == '4':
            library.show_all()

        elif choice == '5':
            try:
                book_id = int(input('Введите ID книги: '))
                if library.change_status(book_id):
                    print('Статус книги изменен.')
                else:
                    print('Книга с таким ID не найдена.')
            except ValueError:
                print("ID должен быть числом.")
            except Exception as ex:
                print(f"Ошибка: {ex}")

        elif choice == '6':
            print('Спасибо за то что воспользовались нашей библиотекой, До свидания!')
            break
        else:
            print('Неверный выбор, введите 1, 2, 3, 4, 5 или 6, попробуйте снова.')
        print('\n', '=' * 80)


if __name__ == "__main__":
    library = Library()
    main()
