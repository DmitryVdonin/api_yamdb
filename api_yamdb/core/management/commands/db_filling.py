import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Category, Comments, Title, User, GenreTitle, Genre


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

            #'static/data/comments.csv': Comments,
            #'static/data/review.csv': Review,

        def db_fill(csv_file, model, fk_1=None, linked_model_1=None, fk_2=None, linked_model_2=None):
            with open(csv_file, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                count = 0
                for row in file_reader:
                    if count == 0:
                        fields = row
                    else:
                        if fk_1:
                            row[fk_1] = linked_model_1.objects.get(id=row[fk_1])
                        if fk_2:
                            row[fk_2] = linked_model_2.objects.get(id=row[fk_2])
                        obj = model(**{fields[i]: row[i] for i in range(len(fields))})
                        obj.save()
                    count += 1

        db_fill('static/data/category.csv', Category)
        db_fill('static/data/genre.csv', Genre)
        db_fill('static/data/titles.csv', Title, 3, Category)
        db_fill('static/data/genre_title.csv', GenreTitle)
        db_fill('static/data/users.csv', User)
