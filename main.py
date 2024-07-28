import sqlite3


class Library:
    def __init__(self):
        self.con = sqlite3.connect("library.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS book(title, status)")

    def modify_book(self, action, title, status):
        if action == "add":
            self.cur.execute("INSERT INTO book VALUES (?, ?)", (title, status))
            self.con.commit()
        elif action == "delete":
            self.cur.execute("DELETE FROM book WHERE title = ?", (title,))
            self.con.commit()
        elif action == "update":
            self.cur.execute(
                "UPDATE book SET status = ? WHERE title = ?", (status, title)
            )
            self.con.commit()

    def show_book(self, status=None):
        print("Read book:\n=========")
        if status:
            self.cur.execute(
                "SELECT title, status FROM book WHERE status = ?", (status,)
            )
        else:
            self.cur.execute("SELECT title, status FROM book")
        books = self.cur.fetchall()
        for book in books:
            print(f"Title: {book[0]}\nStatus: {book[1]}")
            print("---------")

    def close(self):
        self.con.close()


def main():
    library = Library()

    while True:
        option_general = input("What you want to do: modify/display: ")
        if option_general == "modify":
            option_modify = input("What you want to modify: add/delete/update: ")
            if option_modify == "add":
                title = input("Title: ")
                status = input("Status: ")
                library.modify_book("add", title, status)

            elif option_modify == "delete":
                book_to_delete = input("Delete book: ")
                library.modify_book("delete", book_to_delete, status=None)

            elif option_modify == "update":
                title = input("Update book: ")
                status = input("Status: ")
                library.modify_book("update", title, status)

            elif option_modify == "exit":
                library.close()
                break
            else:
                print("Option not supported")
        elif option_general == "display":
            option_display = input("What you want to display: all/read/unread: ")
            if option_display == "all":
                library.show_book()
            elif option_display == "read":
                status = "read"
                library.show_book(status)
            elif option_display == "unread":
                status = "unread"
                library.show_book(status)
            else:
                print("Option not supported")
        elif option_general == "exit":
            library.close()
            break
        else:
            print("Option not supported")
    library.close()


if __name__ == "__main__":
    main()