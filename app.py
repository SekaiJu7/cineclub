# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtWidgets
from movie import get_movies
from movie import Movie

# 2 lignes pour contourner le pb de non affichage sur MAC OS BIG SUR
import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cine Club")
        self.setup_ui()
        self.populate_movies()
        self.setup_connections()

    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.le_movieTitle = QtWidgets.QLineEdit()
        self.btn_addMovie = QtWidgets.QPushButton("Ajouter un film")
        self.lw_movies = QtWidgets.QListWidget()
        self.lw_movies.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.btn_removeMovies = QtWidgets.QPushButton("Supprimer le(s) film(s)")

        self.main_layout.addWidget(self.le_movieTitle)
        self.main_layout.addWidget(self.btn_addMovie)
        self.main_layout.addWidget(self.lw_movies)
        self.main_layout.addWidget(self.btn_removeMovies)

    def populate_movies(self):
        # import movie
        # for movie in movie.get_movies():
        #     self.lw_movies.addItem(movie.nom_film)
        # Ou bien ce qui suit, permettant de faire appel à des instances
        # au lieu d'ajouter une chaîne de caractères avec addItem(str) à lw_movies
        movies = get_movies()
        for movie in movies:
            lw_item = QtWidgets.QListWidgetItem(movie.nom_film)
            lw_item.setData(QtCore.Qt.UserRole, movie)
            self.lw_movies.addItem(lw_item)

    def setup_connections(self):
        self.btn_addMovie.clicked.connect(self.add_movie)
        self.btn_removeMovies.clicked.connect(self.remove_movie)
        self.le_movieTitle.returnPressed.connect(self.add_movie)

    def add_movie(self):
        ajout_film = self.le_movieTitle.text()
        if not ajout_film:
            return False
        new_film = Movie(nom_film=ajout_film)
        if new_film.add_movies():
            lw_item = QtWidgets.QListWidgetItem(ajout_film)
            lw_item.setData(QtCore.Qt.UserRole, new_film)  # Permet d'attacher un objet (notre instance de Movie)
            self.lw_movies.addItem(lw_item)  # à notre listWidgetItem afin de l'utiliser dans lw_movies
            self.le_movieTitle.setText("")
            print(f'Film {ajout_film} ajouté !')
        else:
            print("Le film existe déjà dans la base")

    def remove_movie(self):
        for selected_item in self.lw_movies.selectedItems():
            movie = selected_item.data(QtCore.Qt.UserRole)
            movie.withdraw()
            self.lw_movies.takeItem(self.lw_movies.row(selected_item))


app = QtWidgets.QApplication([])

win = Window()

win.show()

app.exec_()
