from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.order.models import Order


@api_view(['POST'])
def change_status(request, *args, **kwargs):
    status = request.data.get('status')
    id = request.data.get('id')
    order = get_object_or_404(Order, id=id)
    order.status = status
    order.save()
    return Response({
        "msg": "Success",
        "status": 200
    }, status=200)
