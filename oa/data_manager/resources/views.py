from rest_framework.viewsets import ModelViewSet
from ..data_manager.permissions import EnforceReadOnly
from .models import (
    ResourceType, ResourceProperty, ResourceEffect, Resource
)
from .serializers import (
    ResourceTypeSerializer, ResourcePropertySerializer,
    ResourceEffectSerializer, ResourceSerializer
)


class ResourceTypeViewSet(ModelViewSet):
    """ A type of resource, such as "air" or "water" """
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [EnforceReadOnly, ]


class ResourcePropertyViewSet(ModelViewSet):
    """
    An measurable attribute of a resource type, such as "temperature" or "pH"
    """
    queryset = ResourceProperty.objects.all()
    serializer_class = ResourcePropertySerializer
    permission_classes = [EnforceReadOnly, ]


class ResourceEffectViewSet(ModelViewSet):
    """
    An action that can be performed on a resource to affect it's state, such as
    "circulation" or "venting"
    """
    queryset = ResourceEffect.objects.all()
    serializer_class = ResourceEffectSerializer
    permission_classes = [EnforceReadOnly, ]


class ResourceViewSet(ModelViewSet):
    """
    An input to the growing process of a plant, such as a reservoir of water or
    the light shining on a tray
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
