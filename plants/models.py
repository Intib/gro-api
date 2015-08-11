import time
from django.db import models
from cityfarm_api.models import Model


class PlantModel(Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='plant_models')
    read_only = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.name


class PlantType(Model):
    common_name = models.CharField(max_length=100)
    latin_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, related_name='children')
    model = models.ForeignKey(PlantModel, related_name='plant_types')
    plant_count = models.PositiveIntegerField(editable=False, default=0)
    read_only = models.BooleanField(editable=False, default=False)

    def is_above(self, target):
        """
        Check if this type or any of it's children are above `target` in the
        plant type graph. Used in form validation to prevent cycles in the
        graph.
        """
        for child in self.children:
            if child is target or child.is_above(target):
                return True
        return False

    def __str__(self):
        return self.common_name


class Plant(Model):
    index = models.PositiveIntegerField(editable=False)
    plant_type = models.ForeignKey(PlantType, related_name='plants')
    site = models.OneToOneField(
        'layout.PlantSite', null=True, related_name='plant'
    )

    def __str__(self):
        return "{} {}".format(self.plant_type.common_name, self.index)


class SowEvent(Model):
    plant = models.OneToOneField(Plant, related_name='sow_event')
    site = models.ForeignKey('layout.PlantSite', related_name='sow_events+')
    timestamp = models.IntegerField(default=time.time)

    def __str__(self):
        return 'Sowed plant {} in site {}'.format(self.plant, self.site)


class TransferEvent(Model):
    plant = models.ForeignKey(Plant, related_name='transfer_events')
    from_site = models.ForeignKey('layout.PlantSite', related_name='+')
    to_site = models.ForeignKey('layout.PlantSite', related_name='+')
    timestamp = models.IntegerField(default=time.time)

    def __str__(self):
        return 'Transfered plant {} from site {} to site {}'.format(
            self.plant, self.from_site, self.to_site
        )


class HarvestEvent(Model):
    plant = models.OneToOneField(Plant, related_name='harvest_event')
    timestamp = models.IntegerField(default=time.time)

    def __str__(self):
        return 'Harvested plant {}'.format(self.plant)


class PlantComment(Model):
    plant = models.ForeignKey(Plant, related_name='comments')
    content = models.TextField()
    timestamp = models.IntegerField(editable=False, default=time.time)
