from cityfarm_api.viewsets import SingletonViewSet
from farms.models import Farm
from farms.serializers import FarmSerializer


class FarmViewSet(SingletonViewSet):
    model = Farm
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
