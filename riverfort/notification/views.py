from rest_framework.decorators import api_view
from rest_framework.response   import Response

from notification.serializers import CompanySerializer
from notification.models import Company

from .utils import Util

@api_view(['POST'])
def add_company(request):
  serializer = CompanySerializer(data=request.data)
  if serializer.is_valid():
    validatedData = serializer.validated_data
    company = validatedData.get('company')
    time    = validatedData.get('time')
    email_body = 'Hi there:-)\n\n' + "Please don't forget to add the symbol/company: " + company + '\n\nRequested at ' + time + '.' + '\n\nThank you, RiverFort iOS app' 
    data = {
      'email_subject': 'New Symbol/Company Request',
      'email_body': email_body,
      'to_email': "donall.oleary@riverfortcapital.com",
    }
    Util.send_email(data)
  return Response(serializer.data)
