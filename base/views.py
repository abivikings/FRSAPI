from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from psycopg2._psycopg import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from APIComponents.connect_db import *
from APIComponents.process_sp import ExecuteStoredProcedure as Exp
from .models import Campaign, CampaignDetails
from .serializers import CampaignSerializer, CampaignDetailsSerializer
from .utils import generate_access_token, generate_refresh_token
from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_authenticator = JWTAuthentication()


@api_view(['POST'])
def set_password():
    pass


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            user = User.objects.create(email=request.data['camp_admin_email'], password=make_password(request.data['password']), username=request.data['camp_admin_email'], is_active=False)
            campaign = Campaign()
            campaign.user = user
            campaign.name = request.data['name']
            campaign.save()
            campaign_details = CampaignDetails()
            campaign_details.user = user
            campaign_details.campaign = campaign
            campaign_details.title = request.data['name']
            campaign_details.save()
            group = Group.objects.get(pk=2)
            group.user_set.add(user)
            return Response({'status': 'Campaign Created'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Campaign Not Created'},
                            status=status.HTTP_400_BAD_REQUEST)


class CampaignDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CampaignDetails.objects.all()
    serializer_class = CampaignDetailsSerializer


@api_view(['GET'])
def auth_me(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        # unpacking
        user, token = response
        user = User.objects.get(username=user)
        userData = {
            'userData': {
                'userId': user.email,
                'username': user.username,
                'Id': user.id,
                'email': user.email,
                'role': user.groups.values_list('name', flat=True)[0],
                'IsActive': user.is_active,
                'EntryDt': user.date_joined
            }
        }
        return Response(userData, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_auth_group(request):
    queryset = Group.objects.all()
    result_list = list(queryset.values())
    return Response(result_list)


@api_view(['POST', 'GET'])
def CallStoredProcedure(request):
    conn = DbConnector()
    procedure_name = request.data['procedure_name']
    params = request.data['params']
    data = Exp.ExecuteProcedure(procedure_name, tuple(params), conn)
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def create_user(request):
    if request.method == 'POST':
        try:
            group_id = request.data['group_id']
            password = request.data['password']
            hash_pass = make_password(password)
            user = User.objects.create(first_name=request.data['first_name'],
                                       last_name=request.data['last_name'],
                                       email=request.data['email'],
                                       username=request.data['username'],
                                       password=hash_pass)

            group = Group.objects.get(pk=group_id)
            group.user_set.add(user)
            return Response(request.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            if e.args[0]:
                return JsonResponse({"error": "username already exist!!"})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
    if not request.data:
        return Response({'error': "Please provide username/password"}, status="400")

    email = request.data['email']
    response = Response()
    try:
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        if user.check_password(request.data['password']):
            if user:
                access_token, expire_date = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                response.set_cookie(key='Authorization', value=refresh_token)
                response.data = {
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'expiration': expire_date,
                    'userData': {
                        'userId': user.email,
                        'username': user.username,
                        'Id': user.id,
                        'email': user.email,
                        'role': user.groups.values_list('name', flat=True)[0],
                        'IsActive': user.is_active,
                        'EntryDt': user.date_joined
                    }
                }

                return response
            else:
                return Response(
                    {'Error': "Invalid credentials"},
                    status=400,
                    content_type="application/json"
                )
    except Exception as e:
        return Response(e)
    return Response("Somthing went wrong")
