from django.db.models import Count
from django.shortcuts import render
from blog.models import Comment, Post, Tag


def get_related_posts_count(tag):
    """Calculate posts number for <tag>"""
    return tag.num_posts


def get_likes_count(post):
    """Calculate likes number for <post>"""
    return post.num_likes


def serialize_post(post):
    """<post> object serializer"""
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': len(Comment.objects.filter(post=post)),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_post_optimized(post):
    """New serialized_post function"""
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    """<tag> object serializer"""
    return {
        'title': tag.title,
        'posts_with_tag': len(Post.objects.filter(tags=tag)),
    }


def index(request):
    """Main page handler"""
    most_popular_posts = Post.objects.popular() \
                                     .prefetch_authors_and_tags_with_posts_count()[:5] \
                                     .fetch_with_comments_count()
        
    most_popular_tags = Tag.objects.popular()[:5] \
                                   .annotate(posts_count=Count('posts'))

    most_fresh_posts = Post.objects.annotate(comments_count=Count('comments', distinct=True)) \
                                   .order_by('-published_at')[:5] \
                                   .prefetch_authors_and_tags_with_posts_count()
    

    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post_optimized(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    """Get particular <post> object information"""
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    likes = post.likes.all()

    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': len(likes),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    tag_posts = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
    most_popular_tags = list(tag_posts)[:5]

    post_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('num_likes')
    most_popular_posts = list(post_likes)[-5:]

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    """Get particular <tag> object information"""
    tag = Tag.objects.get(title=tag_title)

    tag_posts = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')
    most_popular_tags = list(tag_posts)[:5]

    post_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('num_likes')
    most_popular_posts = list(post_likes)[-5:]

    related_posts = tag.posts.all()[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    """Contact page rendering"""
    return render(request, 'contacts.html', {})
