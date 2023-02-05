import csv
import os

from reviews.models import (Category, Comment, Genre, GenreTitle, Review, Title, User)

# обязательно укажите правильный путь к папке data
path = "d:/Dev/api_yamdb/api_yamdb/static/data"
os.chdir(path) 


# Импортируем все попорядку, иначе могут вылетать исключения или ошибки
# User
with open('users.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = User(id=row['id'],username=row['username'],email=row['email'],role=row['role'],bio=row['bio'],first_name=row['first_name'],)
        p.save()
        
# Category
with open('category.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Category(id=row['id'],name=row['name'],slug=row['slug'])
        p.save()
        
# Genre
with open('genre.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Genre(id=row['id'],name=row['name'],slug=row['slug'])
        p.save()

# Title
with open('titles.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Title(id=row['id'],name=row['name'],year=row['year'],category=Category.objects.get(id=row['category']))
        p.save()

# GenreTitle
with open('genre_title.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = GenreTitle(id=row['id'],title=Title.objects.get(id=row['title_id']),genre=Genre.objects.get(id=row['genre_id']))
        p.save()

# Review
with open('review.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Review(id=row['id'],title=Title.objects.get(id=row['title_id']),text=row['text'], author=User.objects.get(id=row['author']),score=row['score'], pub_date=row['pub_date'])
        p.save()

# Comment
with open('comments.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Comment(id=row['id'],review=Review.objects.get(id=row['review_id']),text=row['text'],author=User.objects.get(id=row['author']),pub_date=row['pub_date'])
        p.save()
