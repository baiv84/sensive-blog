from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class PostQuerySet(models.QuerySet):
    """<Post> model custom manager"""
    def year(self, year):
        """Get <post> queryset for some year"""
        posts_at_year = self.filter(published_at__year=year) \
                            .order_by('published_at')
        return posts_at_year

    def popular(self):
        """Get <post> queryset sorted by likes count3 (desc mode)"""
        popular_posts = self.annotate(likes_count=models.Count('likes')) \
                            .order_by('-likes_count')
        return popular_posts

    def fetch_with_comments_count(self):
        """Optimize comments counting process"""
        queryset_posts_ids = [post.id for post in self]
        posts_with_comments = Post.objects.filter(id__in=queryset_posts_ids) \
                                          .annotate(comments_count=models.Count('comments'))
        ids_and_comments_count = posts_with_comments.values_list('id', 'comments_count')
        count_for_id = dict(ids_and_comments_count)

        for post in self:
            post.comments_count = count_for_id[post.id]
        return self

    def prefetch_authors_and_tags_with_posts_count(self):
        """Preload authors with tag posts count"""
        posts_query_set = self.prefetch_related('author',
                                                models.Prefetch('tags', queryset=Tag.objects.annotate(posts_count=models.Count('posts'))))
        return posts_query_set


class TagQuerySet(models.QuerySet):
    """<Tag> model custom manager"""
    def popular(self):
        most_popular_tags = self.annotate(posts_per_tag_count=models.Count('posts')) \
                                .order_by('-posts_per_tag_count')
        return most_popular_tags


class Post(models.Model):
    """<Post> model impementation"""
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст')
    slug = models.SlugField('Название в виде url', max_length=200)
    image = models.ImageField('Картинка')
    published_at = models.DateTimeField('Дата и время публикации')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        limit_choices_to={'is_staff': True})

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        verbose_name='Кто лайкнул',
        blank=True)

    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        verbose_name='Теги')

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args={'slug': self.slug})


class Tag(models.Model):
    """<Tag> model impementation"""
    title = models.CharField('Тег', max_length=20, unique=True)

    objects = TagQuerySet.as_manager()

    class Meta:
        ordering = ['title']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_filter', args={'tag_title': self.slug})

    def clean(self):
        self.title = self.title.lower()


class Comment(models.Model):
    """<Comment> model impementation"""
    text = models.TextField('Текст комментария')
    published_at = models.DateTimeField('Дата и время публикации')

    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пост, к которому написан')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор')

    class Meta:
        ordering = ['published_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.author.username} under {self.post.title}'
