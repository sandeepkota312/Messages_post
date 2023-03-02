from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=20)
    message=models.TextField()
    likes=models.ManyToManyField(User,related_name='post_likes',default=None)
    posted_date=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(null=True,default=0,blank=True)
    class Meta:
        ordering=('-posted_date',)
    # @classmethod
    # def number_of_likes(self):
    #     return self.likes.count()
    def __str__(self):
        return f"{self.user} : {self.title}"