import csv
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

MODELS_DICT = {
    'category': Category,
    'comments': Comment,
    'genre': Genre,
    'genre_title': GenreTitle,
    'review': Review,
    'titles': Title,
    'users': User,
}


def validate_kwargs(kwargs: dict):
    """Validate csv values"""
    if kwargs.get('author'):
        kwargs['author'] = User.objects.get(
            id=int(kwargs['author'])
        )
    if kwargs.get('category'):
        kwargs['category'] = Category.objects.get(
            id=int(kwargs['category'])
        )
    if kwargs.get('id'):
        kwargs['id'] = int(kwargs['id'])
    if kwargs.get('pub_date'):
        kwargs['pub_date'] = datetime.strptime(
            kwargs['pub_date'],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    if kwargs.get('review_id'):
        kwargs['review_id'] = int(kwargs['review_id'])
    if kwargs.get('score'):
        kwargs['score'] = int(kwargs['score'])
    if kwargs.get('title_id'):
        kwargs['title_id'] = int(kwargs['title_id'])
    if kwargs.get('year'):
        kwargs['year'] = int(kwargs['year'])


def populate_model(model_name, data_dir):
    """Populate model model_name with data from data_dir"""
    if model_name == 'genre_title':
        populate_genre_title(data_dir)
        return
    data_path: str = os.path.join(data_dir, model_name + '.csv')
    model = MODELS_DICT[model_name]
    model.objects.all().delete()
    with open(data_path) as csvfile:
        csv_reader = csv.reader(csvfile)
        keys = next(csv_reader)
        for row in csv_reader:
            kwargs = dict(zip(keys, row))
            validate_kwargs(kwargs)
            model.objects.create(**kwargs)


def populate_genre_title(data_dir: str):
    """Populate GenreTitle model from data_dir's genre_title.csv file """
    GenreTitle.objects.all().delete()
    data_path: str = os.path.join(data_dir, 'genre_title.csv')
    titles: Dict[int, List[int]] = defaultdict(list)
    with open(data_path) as csvfile:
        csv_reader = csv.reader(csvfile)
        keys = next(csv_reader)
        for row in csv_reader:
            kwargs = dict(zip(keys, row))
            titles[int(kwargs['title_id'])].append(int(kwargs['genre_id']))

    for title_id, genre_ids in titles.items():
        title = Title.objects.get(id=title_id)
        title.genre.add(*genre_ids)


class Command(BaseCommand):
    help = 'Populates database'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str)

    def handle(self, *args, **options):
        models = ('users', 'category', 'genre', 'titles',
                  'genre_title', 'review', 'comments')
        for model in models:
            try:
                populate_model(model, options['data_dir'])
            except FileNotFoundError as error:
                self.stdout.write(self.style.WARNING(
                    f'Could not find {model} model: {error}'
                ))
            except Exception as error:
                self.stdout.write(self.style.ERROR(
                    f'Can not populate {model} model: {error}'
                ))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Populated {model} model')
                )
        # # populate models
        # populate_model('users', data_dir)
        # populate_model('category', data_dir)
        # populate_model('genre', data_dir)
        # populate_model('titles', data_dir)
        # populate_genre_title(data_dir)
        # populate_model('review', data_dir)
        # populate_model('comments', data_dir)

        # for poll_id in options['datadir']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(
        # self.style.SUCCESS('Successfully closed poll "%s"' % poll_id
        # ))
