from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny

User = get_user_model()
# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number','')
        if not username or not password or not email:
            return Response({
               'detail': 'Usename, password or email are required.' 
            },status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({
                'detail': 'Username already exists.'
            },status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.phone_number = phone_number
            user.save()

            
            return Response({
                'status': 'success',
                'message': 'User registered successfully!',
                'user_id': user.id,
                'email': user.email,
                'phone_number': user.phone_number or "N/A",
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'detail': f'Error: {str(e)}'
            },status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        #email = request.data.get('email')
        #phone_number = request.data.get('phone_number','')
        #user = User.objects.filter(username=username).first()
        if not username or not password:
            return Response({
                'error': 'Invalid credent'
            },status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({
            'status': 'success',
            'message': 'Login successful!',
            'user_id': user.id,
            'email': user.email,
            #'phone_number': user.phone_number or "N/A",
        }, status=status.HTTP_200_OK)

