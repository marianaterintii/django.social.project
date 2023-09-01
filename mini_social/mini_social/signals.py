from .models import Post, Comment
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

def postPublishedCallback(sender, instance, **kwargs): # 2argumente obligatorii in signals
    if isinstance (instance, Post):
        print ("Post published")
        
        host = settings.SITE_URL
        print(f"you can read it <a href='{host}/post/get/{instance.id}'> here</a>")
        send_mail(
            "Mini Social: A new post was published",
            "",
            settings.SITE_MAIL,
            ["marianaterintii@gmail.com"],
            fail_silently=False, #show errors
            html_message = f"you can read it <a href='{host}/post/get/{instance.id}'> here</a>",
        )
#HW notify by email the post author when a new comment was added to its post
# hint: post_save(comment)--> post---> author---> email
@receiver(post_save, sender=Comment)
def commentPostCallback(sender, instance, **kwargs):
    host = settings.SITE_URL
    if instance.post.author != instance.author:
        send_mail(
            "Mini Social: New Comment on Your Post",
            f"You have a new comment on post:'{instance.post.title}' from {instance.author.username}. Read <a href='{host}/post/get/{instance.post.id}'> here</a>",
            settings.SITE_MAIL,
            [instance.post.author.email],
            fail_silently=False,
            html_message=f"You have a new comment on post '{instance.post.title}' from {instance.author.username}. Read <a href='{host}/post/get/{instance.post.id}'> here</a>",
        )
