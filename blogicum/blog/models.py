from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import SELFTITLELEN

User = get_user_model()


class CommonFieldsModel(models.Model):
    """База для  модели"""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class BaseTitle(models.Model):
    """База для заголовка"""

    title = models.CharField(max_length=256, verbose_name='Заголовок')

    class Meta:
        abstract = True


class Location(CommonFieldsModel):
    """Местоположение"""

    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name[:SELFTITLELEN]


class Category(CommonFieldsModel, BaseTitle):
    """Категория"""

    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title[:SELFTITLELEN]


class Post(CommonFieldsModel, BaseTitle):
    """Публикация."""

    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=("Если установить дату и время в будущем — "
                   "можно делать отложенные публикации."),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title[:SELFTITLELEN]
