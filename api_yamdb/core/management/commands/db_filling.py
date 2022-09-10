import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):
    """"Добавляет данные в базу из csv файлов."""

    help = 'Загрузка данных из csv файлов в базу'

    def handle(self, *args, **kwargs):

        def db_fill(csv_file, model, fk_index=None, linked_model=None):
            with open(csv_file, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                first_line = True
                for row in file_reader:
                    if first_line:
                        fields = row
                    else:
                        if fk_index:
                            row[fk_index] = linked_model.objects.get(
                                id=row[fk_index]
                            )

                        obj = model(
                            **{fields[i]: row[i] for i in range(len(fields))}
                        )
                        obj.save()
                    first_line = False

        db_fill('static/data/category.csv', Category)
        db_fill('static/data/genre.csv', Genre)
        db_fill('static/data/titles.csv', Title, 3, Category)
        db_fill('static/data/genre_title.csv', GenreTitle)
        db_fill('static/data/users.csv', User)
        db_fill('static/data/review.csv', Review, 3, User)
        db_fill('static/data/comments.csv', Comments, 3, User)
