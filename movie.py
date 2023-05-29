import json
from pathlib import Path
import logging

data_json = Path(__file__).parent.resolve() / "data" / "movies.json"
print(data_json)


def get_movies():  # récupère les films sous forme d'instance de Movie

    with open(data_json, "r") as f:
        movie_titles = json.load(f)

    movies = [Movie(movie_title) for movie_title in movie_titles]
    return movies


class Movie:
    def __init__(self, nom_film: str):
        self.nom_film = nom_film.title()

    def __str__(self):  # peut être utilisé pour les attributs définis par le init
        return f"{self.nom_film}"

    def _get_movies(self):
        with open(data_json, "r") as f:
            return json.load(f)

    def _write_movies(self, movies):
        with open(data_json, "w") as f:
            json.dump(movies, f, indent=4)

    def add_movies(self):
        movies = self._get_movies()
        if self.nom_film not in movies:
            movies.append(self.nom_film)
            self._write_movies(movies)
            return True

        else:
            logging.warning(f"Le film {self.nom_film} est déjà dans la liste.")
            return False

    def withdraw(self):
        movies = self._get_movies()
        if self.nom_film in movies:
            del movies[movies.index(self.nom_film)]  # ou bien movies.remove(self.nom_film)
            self._write_movies(movies)
            return True
        else:
            logging.warning(f"Le film {self.nom_film} n'est pas dans la liste.")
            return False


if __name__ == "__main__":
    movies = get_movies()
    print(movies)
