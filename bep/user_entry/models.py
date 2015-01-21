from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.core.urlresolvers import reverse
import hashlib
import urllib
import urllib2
from xml.dom import minidom

# Create your models here.
class user_entry(models.Model):
	title = models.CharField(max_length=200)
	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    
    

    first_name = models.CharField(max_length=30, null=True, blank=True)        
    last_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    books_available = models.IntegerField(default=0)
    books_borrowed = models.IntegerField(default=0)
    points = models.IntegerField(default=1)

    about_me = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
    	return reverse('userprofile_edit', kwargs={'pk': self.pk})
    

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def profile_image_url(self):
        """
        Return the URL for the user's Facebook icon if the user is logged in via Facebook,
        otherwise return the user's Gravatar URL
        """
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        tw_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='twitter')
        gg_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
        elif len(tw_uid):
            extra_data = tw_uid[0].extra_data
            pic = extra_data['profile_image_url_https']
            return pic
        elif len(gg_uid):
            extra_data = gg_uid[0].extra_data
            pic = extra_data['picture']
            return pic
        return "http://www.gravatar.com/avatar/{}?s=40".format(
            hashlib.md5(self.user.email).hexdigest())

    def account_verified(self):
        """
        If the user is logged in and has verified hisser email address, return True,
        otherwise return False
        """
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False



User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
