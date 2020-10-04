from django.db import models
from django.urls import reverse

# Create your models here.


class Paragraph(models.Model):
    """
    хранит:
        название параграфа
        фото к параграфу
        текст параграфа
        (жирный ли текст)
        номер параграфа
    """
    paragraph_title = models.CharField("заголовок параграфа", max_length=200, blank=True)
    paragraph_img = models.ImageField("фото к параграфу", upload_to="seven_op/static/uploads/files/%Y/%m/%d",
                                      blank=True)
    paragraph_text = models.TextField("текст параграфа", blank=True)
    is_strong = models.BooleanField("жирный текст")
    paragraph_nb = models.IntegerField("номер параграфа", default=0, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        возвращает заголовок и время
        """
        return str(self.paragraph_title) + " ||| " + str(self.date)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Параграфы"


class Category(models.Model):
    """
    Хранит название категории
    """
    name_sing = models.CharField("имя в единственном числе", max_length=200)
    name_plur = models.CharField("имя во множественном числе", max_length=200)
    name_url = models.CharField("имя для ссылки", max_length=200)

    def __str__(self):
        """
        возвращает название
        :return: name_sing
        """
        return str(self.name_sing)

    def get_url_for_show_page(self):
        return reverse('show_category', args=[str(self.name_url)])

    class Meta:
        ordering = ["-name_sing"]
        verbose_name_plural = "Категории"


class UploadedFile(models.Model):
    """
    хранит загруженный файл
    """
    file = models.FileField("файл", upload_to="seven_op/static/uploads/files/%Y/%m/%d")
    name = models.CharField("имя файла", max_length=200)

    def __str__(self):
        """
        возвращает название файла
        :return: name
        """
        return str(self.name)

    class Meta:
        verbose_name_plural = "Загруженные файлы"


class UploadedPhoto(models.Model):
    """
    хранит загруженное фото
    """
    photo = models.ImageField("фото", upload_to="seven_op/static/uploads/img/%Y/%m/%d")
    index = models.IntegerField("номер фото в карусели", null=True, default=1,
                                help_text="если загружаете фото для карусели, то пронумеруйте их с 0")
    name = models.CharField("название фото", max_length=200)

    def __str__(self):
        """
        возвращает название фото
        :return: name
        """
        return str(self.name)

    class Meta:
        verbose_name_plural = "Загруженные фото"


class Comment(models.Model):
    """
    хранит коментарии к публикациям и блогам
    """
    author = models.CharField("имя автора", max_length=200)
    data = models.TextField("текст комментария")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        возвращает имя автора и дату
        :return: author + date
        """
        return str(self.author) + " ||| " + str(self.date)

    class Meta:
        ordering = ["-data"]
        verbose_name_plural = "Комментарии"


class BlogAuthor(models.Model):
    """
    хранит автора блогов
    """
    name = models.CharField("имя автора блогов", max_length=200)
    photo = models.ForeignKey('UploadedPhoto', on_delete=models.SET_NULL, null=True, blank=True,
                              help_text="выберете фото из загруженных")
    info = models.TextField("информация об авторе", help_text="необязательное поле", null=True, blank=True)

    def __str__(self):
        """
        возвращает имя автора
        :return: name
        """
        return str(self.name)

    def get_url_for_author_blogs(self):
        """
        возвращает ссылку на страницу с блогами автора
        :return:
        """
        return reverse('show_blogs_for_author', args=[str(self.id)])

    class Meta:
        ordering = ["-name"]
        verbose_name_plural = "Авторы блогов"


class Post(models.Model):
    """
    Хранит информацию о публикации
    """
    title = models.CharField("заголовок", max_length=200)
    description = models.CharField("описание", max_length=1000, blank=True, null=True, help_text="необязательное поле")
    author = models.CharField("имя автора", max_length=200)
    category = models.ForeignKey('Category', verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    paragraphs = models.ManyToManyField('Paragraph', verbose_name="Параграфы")
    preview = models.ImageField("фото на заголовок", upload_to="seven_op/static/uploads/previews/%Y/%m/%d", null=True,
                                default=None,
                                blank=True)
    photos_for_spin = models.ManyToManyField('UploadedPhoto', verbose_name='фото на "карусель"',
                                             default=None, blank=True)
    attached_files = models.ManyToManyField('UploadedFile', verbose_name="прикрепленные файлы",
                                            default=None, blank=True)
    comments = models.ManyToManyField('Comment', verbose_name="комментарии к публикации", default=None,
                                      blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        возвращает заголовок и дату
        :return: title + date
        """
        return str(self.title) + "  |||  " + str(self.date)

    def get_url_for_show(self):
        """
        возвращает ссылку для просмотра поста
        :return:
        """
        return reverse('show_post', args=[str(self.id)])

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Публикации"


class Blog(models.Model):
    """
    хранит информацию о блоге
    """
    title = models.CharField("заголовок", max_length=200)
    description = models.CharField("описание", max_length=1000, null=True, blank=True)
    author = models.ForeignKey('BlogAuthor', on_delete=models.SET_NULL, null=True)
    paragraphs = models.ManyToManyField('Paragraph', verbose_name="Параграфы")
    preview = models.ImageField("фото на заголовок", upload_to="seven_op/static/uploads/previews/%Y/%m/%d", null=True,
                                default=None)
    photos_for_spin = models.ManyToManyField('UploadedPhoto', verbose_name='Фото на "карусель"',
                                             default=None, blank=True)
    attached_files = models.ManyToManyField('UploadedFile', verbose_name="прикрепленные файлы",
                                            default=None, blank=True)
    comments = models.ManyToManyField('Comment', verbose_name="Комментарии к блогу", default=None, blank=True)

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        возвращает заголовок и дату
        :return: title + date
        """
        return str(self.title) + "  |||  " + str(self.date)

    def get_url_for_show(self):
        """
        возвращает ссылку для просмотра блога
        :return:
        """
        return reverse('show_blog', args=[str(self.id)])

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Блоги"
