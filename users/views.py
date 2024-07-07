from rest_framework import generics
from .serializers import UserRegisterSreializer, LoginSerializer, UpdateUserSerializer
from .models import UserModel, VerifyCodeModel
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class UserRegistrationViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    model = UserModel.objects.all()
    serializer_class = UserRegisterSreializer
    
class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = self.request.user
        code = request.data.get('code')
        
        verify_code = VerifyCodeModel.objects.filter(code=code)
        print(verify_code)
        if verify_code.exists():
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            res = {
                "status": 200,
                "message": "Code verified successfully",
                "access": access_token,
                "refresh": str(refresh)
            }
            
            return Response(res)
        else:
            return Response({"status": 400, "message": "Wrong code"})
  
  
        
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        return Response(validated_data, status=status.HTTP_200_OK)
    
    
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(UpdateUserView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "User updated successfully ∞",
        }
        return Response(data, status=200)


class UserListForAdmin(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = UserModel.objects.all()
        serializer = UpdateUserSerializer(users, many=True)
        return Response(serializer.data)
    

class UdateUserForAdmin(APIView):
    permission_classes = [IsAdminUser]
    serializer = UpdateUserSerializer
    
    def put(self, request, pk):
        user = UserModel.objects.filter(id=pk)
        
        if user:
            user.update(**request.data)
            return Response({"status": 200, "message": "User updated successfully"})
        
        else:
            return Response({"status": 400, "message": "User not found"})
        
class DeleteUserForAdmin(APIView):
    permission_classes = [IsAdminUser]
    
    def delete(self, request, pk):
        user = UserModel.objects.filter(id=pk)
        
        if user:
            user.delete()
            return Response({"status": 200, "message": "User deleted successfully"})
        
        else:
            return Response({"status": 400, "message": "User not found"})