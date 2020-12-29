from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

MEMBERSHIP_CHOICES =(
	('Enterprise','ent'),
	('Professional','pro'),
	('Free','free')
	)



class Membership(models.Model):
	slug=models.SlugField()
	membership_type=models.CharField(
		choices=MEMBERSHIP_CHOICES,
		default='Free',
		max_length=30)
	price= models.IntegerField(default=15)

	def __str__(self):
		return self.membership_type


class UserMembership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	membership=models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)

	def __str__(self):
		return self.user.username

def post_save_usermembership_create(sender,instance,created,*args,**kwargs):
	if created:
		UserMembership.objects.get_or_create(user=instance)

	user_membership, created = UserMembership.objects.get_or_create(user=instance)


post_save.connect(post_save_usermembership_create,sender=settings.AUTH_USER_MODEL)

class Subscription(models.Model):
	user_membership=models.ForeignKey(UserMembership, on_delete=models.CASCADE)
	active =models.BooleanField(default=True)

	def __str__(self):
		return self.user.username

