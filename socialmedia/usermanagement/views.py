from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView,status
from .serializers import UserSerializer,UserLoginSerializer,ChangePasswordSerializer
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
# Create your views here.

# Views using APIView :-

class UserSignUpAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({
                    "success": False,
                    "message": "Email already exists."
                },status=status.HTTP_400_BAD_REQUEST)
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return Response({
                    "success": False, 
                    "message": "Username already exists."
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginLogoutAPIView(APIView):

    # Login Functionality
    def post(self,request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email = serializer.validated_data['email'])
                if user.password == serializer.validated_data['password']:
                    token = Token.objects.get_or_create(user=user)
                    return Response({
                        "success":True,
                        "Token":token[0].key
                    })
                else:
                    return Response({
                        "success":False,
                        "message":"Incorrect Email or Password"
                    })               
            except User.DoesNotExist:
                return Response({
                    "success":False,
                    "message":"user does not exist" 
                })
    # Logout Functionality   
    def delete(self,request):
        Token.objects.filter(user=request.user).delete()
        return Response({
            "success":True,
            "message":"Logout Successful"
        })
class UserDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if old_password != user.password:
                return Response({
                    "success":False,
                    "message": "Incorrect old password"
                }, status=status.HTTP_400_BAD_REQUEST)

            user.password = new_password
            print(new_password)
            user.save()

            return Response({
                "success":True,
                "message": "Password changed successfully"
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
