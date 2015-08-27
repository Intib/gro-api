from django.conf import settings
from ..farms.models import Farm
from ..farms.serializers import FarmSerializer
if settings.SERVER_TYPE == settings.LEAF:
    from ..data_manager.viewsets import SingletonModelViewSet as FarmViewSetBase
else:
    from rest_framework.viewsets import ModelViewSet as FarmViewSetBase


class FarmViewSet(FarmViewSetBase):
    """ Represents a single Personal Food Computer """
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    allow_on_unconfigured_farm = True
