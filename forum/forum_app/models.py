from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", blank=True)
    icon = models.ImageField(upload_to='category_icons/', verbose_name="Иконка", blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="posts", verbose_name="Категория")
    text = models.TextField(verbose_name="Текст поста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name="Автор")
    avatars = models.ImageField(upload_to='avatars/', blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0, verbose_name="Количество лайков")  # Поле для хранения количества лайков

    def __str__(self):
        return f"{self.author.get_full_name()} ({self.author.username}) - {self.text[:50]}"



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", verbose_name="Пост")

    def __str__(self):
        return f"{self.user.username} liked {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор комментария"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.text[:50]
    