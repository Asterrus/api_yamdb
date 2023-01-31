from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    bio = models.TextField(null=True)
    password = models.CharField(max_length=128, null=True)
    confirmation_code = models.CharField(max_length=200, null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class BaseModelReviw(models.Model):
    """Абстрактная модель для добавления текста и даты публикации."""

    text = models.TextField(
        "Текст записи", max_length=500, help_text="Поле для новой записи"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

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
        related_name='reviews',
        verbose_name='Оценка',
        help_text='Ваша оценка данному произведению от 1 до 10 (целое число)',
        validators=(
            MinValueValidator(
                1, message='Укажите число большее или равное 1.'
            ),
            MaxValueValidator(
                5, message='Укажите число меньшее или равное 10'
            ),
        )
    )

    class Meta:
        ordering = ('-pub_date',)
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
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        """Метод для возврата названия объекта."""
        return self.text[:LENGTH_STR]
