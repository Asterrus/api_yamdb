from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

LENGTH_STR: int = 15


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    role_choices = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    )
    email = models.EmailField(blank=True, unique=True)
    role = models.CharField(max_length=10, choices=role_choices, default=USER)
    bio = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=128, null=True)
    confirmation_code = models.CharField(max_length=200, null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


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
    # Потом вынесем отдельно
    if value > timezone.localtime(timezone.now()).year:
        raise ValidationError('Год не должен быть больше текущего')


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

    rating = models.IntegerField(
        'Рейтинг', null=True, blank=True,)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseModelReviw(models.Model):
    """Абстрактная модель для добавления текста и даты публикации."""

    text = models.TextField(
        'Текст записи', max_length=500, help_text='Поле для новой записи'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class Review(BaseModelReviw):
    """Модель для управления отзывами произведений."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Ваша оценка данному произведению от 1 до 10 (целое число)',
        validators=(MinValueValidator(1), MaxValueValidator(10),))

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='reviews_unique',
            ),
        )

    def __str__(self):
        """Метод для возврата названия объекта."""
        return self.text[:LENGTH_STR]


@receiver([post_delete, post_save], sender=Review)
def title_rating_change(sender, instance, using, **kwargs):
    """Каждый раз при создании, изменении или удалении отзыва
       будет пересчитан рейтинг Title."""
    instance.title.rating = instance.title.reviews.aggregate(
        models.Avg('score'))['score__avg']
    instance.title.save()


class Comment(BaseModelReviw):
    """Модель для управления комментариями к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Метод для возврата названия объекта."""
        return self.text[:LENGTH_STR]
