from django.db import models
from django.contrib.auth.models import User

class messagesAbstract(models.Model):
    # post_id = models.BigAutoField(primary_key=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=50)
    message=models.TextField()
    likes=models.ManyToManyField(User,related_name='post_likes',default=None)
    posted_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=('-posted_date',)
    def __str__(self):
        return f"{self.user} : {self.title}"

class commentsAbstract(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class comments(commentsAbstract):
    post=models.ForeignKey(Messages,on_delete=models.CASCADE,default=1)
    curr_user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    comment=models.TextField()

    def fetch_comments(post_id):
        all_comments=comments.objects.filter(post=Messages.objects.get(id=post_id))
        all_comments=list(all_comments)
        return all_comments
    
    def add_comment(post_id,curr_user_id,comment):
        curr_user=User.objects.get(id=curr_user_id)
        post=Messages.objects.get(id=post_id)
        comments.objects.create(curr_user=curr_user,post=post,comment=comment)
        print('Done')

    def __str__(self) -> str:
        return f"{self.curr_user.username} commented on {self.post.user.username}'s {self.post.title14}"
