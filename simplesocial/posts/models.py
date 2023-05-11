from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from django.contrib.auth import get_user_model
from groups.models import Group
from ckeditor.fields import RichTextField

User = get_user_model()
# Create your models here.
current_user_name = User.username


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    # message = models.TextField()
    message = RichTextField(blank=True, null=True)
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static/images", null=True, blank=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']


class UploadFileModel(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="posts/images")
    post = models.ForeignKey(Post,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

