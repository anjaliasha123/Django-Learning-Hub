from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class TaggedItemManager(models.Manager):
    def get_tags_for(self, content_type, object_id):
        ct = ContentType.objects.get_for_model(content_type)
        return TaggedItem.objects\
            .select_related('tag')\
            .filter(object_id=object_id, content_type=ct)

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
