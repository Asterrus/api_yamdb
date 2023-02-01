from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField('Слаг жанра', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=50)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


def year_validator(value):
    if value > timezone.localtime(timezone.now()).year:
        raise ValidationError("Год не должен быть больше текущего") 
    
    
class Title(models.Model):
    name = models.CharField('Наименование произведения', max_length=200)

    year = models.IntegerField(
        'Год создания произведения',
        validators=[year_validator]
    )
    description = models.CharField(
        'Описание произведения',
        max_length=250,
        default='нет описания',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='название категории',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        help_text='наименование жанра',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
