import csv

from django.core.management.base import BaseCommand

from reviews.models import Review
from static.data import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = {
            'category.csv': Category,
            'comments.csv': Comment,
            'genre_title.csv': Genre_title,
            'review.csv': Review,
            'titles.csv': Title,
            'users.csv': User,
        }

        for csv_file, model in data.items():
            with open(csv_file, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                for i in range(1, len(file_reader)):
                    model.objects.create(*file_reader[i])
