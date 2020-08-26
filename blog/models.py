from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import truncatechars

# in models.py we need to think about what we are going to save in the database

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
    	return self.likes.count()
    

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	created_date = models.DateTimeField(editable=False)
	edited = models.DateTimeField(editable=False, null=True)

	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return self.text[:20]

	@property
	def short_description(self):
		return truncatechars(self.text, 35)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_date = timezone.now()
		else:
			self.edited = timezone.now()
		return super(Comment, self).save(*args, **kwargs)