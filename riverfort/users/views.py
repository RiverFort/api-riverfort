from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from .serializers import RegisterUserSerializer
from .utils import Util
from .models import NewUser
import jwt
import re

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
      reg_serializer = RegisterUserSerializer(data=request.data)
      if reg_serializer.is_valid():

        domain_pattern = '(?<=@)[^.]+(?=\.)'
        email = reg_serializer.validated_data['email']
        domain = re.search(domain_pattern, email).group(0)
        if domain == 'riverfortcapital' or domain == 'terravista-partners':
          
          newuser = reg_serializer.save()

          # email verify for activating account
          user_data = reg_serializer.data
          theUser = NewUser.objects.get(email=user_data['email'])
          token = RefreshToken.for_user(theUser).access_token
          current_site = get_current_site(request).domain
          relativeLink = reverse('users:email-verify')
          absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
          email_body = 'Hi ' + newuser.first_name + '\n\n' + 'Please use the link below to verify your email \n' + absurl
          data = {
            'email_subject': 'Activate your RiverFort Portal account',
            'email_body': email_body,
            'to_email': newuser.email,
          }
          Util.send_email(data)

          if newuser:
              return Response(status=status.HTTP_201_CREATED)
        else:
          return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
  def get(self, request):
    token = request.GET.get('token')
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      user    = NewUser.objects.get(id=payload['user_id'])
      if not user.is_active:
        user.is_active = True
        user.save()
      return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
      return Response({'error': 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
      return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


