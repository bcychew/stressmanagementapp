from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #user is default
from django.db.models.signals import post_save
from django.dispatch import receiver

#post model for posts on feed
class Post(models.Model):
    body = models.TextField() #text
    created_on = models.DateTimeField(default = timezone.now) #time post
    author = models.ForeignKey(User, on_delete = models.CASCADE) #author, foreign key of default auth model User, if user deleted, author is deleted with models.CASCADE
    image = models.ImageField(upload_to ='uploads/post_images', blank = True, null = True) #image, can be blank or null, because it's optional
    likes = models.ManyToManyField(User, blank=True, related_name='likes')


class Comment(models.Model):
	comment = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
 
	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False
		
	@property
	def children(self):
 		return Comment.objects.filter(parent=self).order_by('-created_on').all()



#userprofile model for profile
class UserProfile(models.Model):
    #one user has 1 profile and vice versa, can be accessed by related name, 'profile', primary key = user
    user = models.OneToOneField(User, primary_key = True, verbose_name = 'user', related_name = 'profile', on_delete = models.CASCADE)
	#profile name, charfield because shorter length, optional
    name = models.CharField(max_length = 50, blank = True, null = True)
	#bio, textfield, optional
    bio = models.TextField(max_length = 500, blank = True, null = True)
	#birth_date, datefield, optional, require specific format designated by django
    birth_date = models.DateField(null = True, blank = True)
	#location is optional charfield, users can enter anything other than countries, less than 100 length
    location = models.CharField(max_length = 100, blank = True, null = True)
	#image will upload to uploads/profile_images, and the default is user.png, optional field
    image = models.ImageField(upload_to='uploads/profile_images', default = 'uploads/profile_images/user.png', blank = True)
	#many to many field friends because many users can have many friends, and many friends can have many users
    friends = models.ManyToManyField(User, blank = True, related_name = 'friends')
        
@receiver(post_save, sender=User)
#defines a receiver to take in sender and post
#create user profile with sender = User and if created, create UserProfile object
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

#defines receiver
@receiver(post_save, sender=User)
#save user profile object as instance
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
    #center usual model, instance is the actual user saved

class Thread(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
#thread model that takes in user and receiver from User auth models as foreign keys, and ensure they use no related_names with '+'

#usermessage model that involves thread as foreign key
class UserMessage(models.Model):
	#message_sender and message_receiver are foreign keys of users that cascade upon user delete
	#same for thread to thread
	thread = models.ForeignKey('Thread', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	message_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_images', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)
	#check is_read boolean field with yes/false