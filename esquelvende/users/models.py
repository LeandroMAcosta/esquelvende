# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# import PIL
# from PIL import Image
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.utils.six import StringIO

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	phone = models.IntegerField(default=None, null=True)
	avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')


	# def save(self, *args, **kwargs):
	# 	# Do extra stuff before saving
 
	# 	# If new post, get the picture and resize it on the fly
	# 	if self.pk is None:
	# 		# 1200px width maximum
	# 		basewidth = 180
	# 		img = Image.open(self.avatar)
	# 		# Keep the exif data
	# 		exif = None
	# 		if 'exif' in img.info:
	# 			exif = img.info['exif']
	# 		width_percent = (basewidth/float(img.size[0]))
	# 		height_size = int((float(img.size[1])*float(width_percent)))
	# 		img = img.resize((basewidth, height_size), PIL.Image.ANTIALIAS)
	# 		output = StringIO()
	# 		# save the resized file to our IO ouput with the correct format and EXIF data ;-)
	# 		if exif:
	# 			img.save(output, format='JPEG', exif=exif, quality=90)
	# 		else:
	# 			img.save(output, format='JPEG', quality=90)
	# 		output.seek(0)
	# 		self.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.avatar.name, 'image/jpeg',
	# 											output.len, None)
 
		#super(CarPost, self).save(*args, **kwargs)

	
	# def save(self):

	# 	if not self.id and not self.avatar:
	# 		return            

	# 	super(UserProfile, self).save()

	# 	image = Image.open(self.avatar)
	# 	(width, height) = image.size

	# 	"Max width and height 800"        
	# 	if (800 / width < 800 / height):
	# 		factor = 800 / height
	# 	else:
	# 		factor = 800 / width

	# 	size = ( width / factor, height / factor)
	# 	image.resize(size, Image.ANTIALIAS)
	# 	image = image.save(self.avatar.path)
