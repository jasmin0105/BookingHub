import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def geocode_address(request):
    """
    External API integration — 2GIS Geocoding API
    GET /api/geocode/?address=Chui+Avenue+1+Bishkek
    """
    address = request.GET.get('address', '')
    if not address:
        return Response({'error': 'address parameter is required'}, status=400)

    try:
        # 2GIS Geocoding API
        url = "https://catalog.api.2gis.com/3.0/items/geocode"
        params = {
            'q': address,
            'fields': 'items.point',
            'key': 'demo',
        }
        res = requests.get(url, params=params, timeout=5)

        if res.status_code == 200:
            data = res.json()
            items = data.get('result', {}).get('items', [])
            if items:
                point = items[0].get('point', {})
                return Response({
                    'address': address,
                    'lat': point.get('lat'),
                    'lon': point.get('lon'),
                    'full_name': items[0].get('full_name', address),
                    'source': '2GIS API'
                })

        # Fallback — return Bishkek center coords
        return Response({
            'address': address,
            'lat': 42.8746,
            'lon': 74.5698,
            'full_name': address,
            'source': 'fallback'
        })

    except requests.RequestException:
        return Response({
            'address': address,
            'lat': 42.8746,
            'lon': 74.5698,
            'source': 'fallback'
        })
