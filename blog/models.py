from django.db import models
from django.utils.timezone import now
from django_resized import ResizedImageField
from account.utils.blog_utils import count_words, read_time
from django.utils.text import slugify
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    name = models.CharField(max_length=100)
    short_bio = models.TextField()
    image = models.ImageField(upload_to="author image", blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class blogs(models.Model):
    status_choice = (
        ('Drafted', 'Drafted'), ('Published', 'Published')
    )
    title = models.CharField(max_length=500)
    date_published = models.DateField(default=now, blank=True)
    date_created = models.DateField(default=now, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(
        Author, blank=True, null=True, on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[750, 375], upload_to='article_pics', force_format='PNG', blank=True)
    content = RichTextUploadingField(blank=True)
    summary = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(
        max_length=20, choices=status_choice, default='DRAFT')
    views = GenericRelation(HitCount, object_id_field='object_p',
                            related_query_name='hit_count_generic_relation')
    count_words = models.CharField(max_length=50, default=0, blank=True)
    read_time = models.CharField(max_length=50, default=0, blank=True)
    deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('-date_published',)
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.content)
        self.read_time = read_time(self.content)
        super(blogs, self).save(*args, **kwargs)
