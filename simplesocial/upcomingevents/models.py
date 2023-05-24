from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
from ckeditor.fields import RichTextField
import misaka

User = get_user_model()
# Create your models here.

class UpcomingEvent(models.Model):
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    event_start_at = models.DateTimeField(blank=False, null=False)
    # message = models.TextField()
    message = RichTextField(blank=True, null=True)
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='events', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


    def save(self, *args, **kwargs):
        local = misaka.html(self.message)
        print("¥¥¥¥  def save(self, *args, **kwargs): ¥¥¥¥¥")
        print(local)
        self.message_html = misaka.html(self.message)
        super(UpcomingEvent, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-event_start_at']

