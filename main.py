from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox

import sys
import random
import string
import json


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("pass_ui.ui", self)
        self.generate_button = self.findChild(QtWidgets.QPushButton, 'generate_button')
        self.add_button = self.findChild(QtWidgets.QPushButton, 'add_button')
        self.search_button = self.findChild(QtWidgets.QPushButton, 'search_button')
        self.password_entry = self.findChild(QtWidgets.QLineEdit, 'password_entry')
        self.website_to_save = self.findChild(QtWidgets.QLineEdit, 'website_entry')
        self.username_to_save = self.findChild(QtWidgets.QLineEdit, 'username_entry')

        self.generate_button.clicked.connect(self.pass_generator)
        self.add_button.clicked.connect(self.save_data)
        self.search_button.clicked.connect(self.find_password)

        self.show()

    def show_message_box(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        retval = msg.exec()

    def pass_generator(self):
        size = 12
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation
        new_password = ''.join(random.choice(chars) for _ in range(size))
        self.password_entry.setText(f"{new_password}")

    def save_data(self):

        website_to_save = self.website_to_save.text()
        username_to_save = self.username_to_save.text()
        password_to_save = self.password_entry.text()

        if len(username_to_save) == 0:
            username_to_save = self.username_to_save.placeholderText()

        new_data = {
            website_to_save: {
                "email": username_to_save, "password": password_to_save,
            }
        }
        print(new_data)

        if len(website_to_save) != 0 and len(username_to_save) != 0 and len(password_to_save) != 0:
            print(website_to_save, username_to_save, password_to_save)

            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # saving the updated data
                    json.dump(data, data_file, indent=4)
            finally:
                self.website_to_save.clear()
                self.password_entry.clear()
                self.username_to_save.clear()
        else:
            self.show_message_box(text="Empty", title="Information")


    def find_password(self):
        website_to_search = self.website_to_save.text()
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            self.show_message_box(text="Data file not found", title="Error")
        else:
            if website_to_search in data:
                user_email = data[website_to_search]["email"]
                user_password = data[website_to_search]["password"]
                self.show_message_box(text=f"Email: {user_email}\nPassword: {user_password}", title="Found!")

            else:
                self.show_message_box(text="Data file not found", title="Error")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()  # MAKE WINDOW VISIBLE
    app.exec()  # EVENT LOOP


if __name__ == '__main__':
    main()
