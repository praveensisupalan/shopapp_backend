from django.shortcuts import render
from rest_framework import views, authentication, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import Shop_Serializer, User_Serializer
from .models import shop
from rest_framework.response import Response
from core.models import CustomUser
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


class Shop_view(views.APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
       
    def get(self, request, *args, **kwargs):

        shops = shop.objects.all()
        serializer = Shop_Serializer(shops, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        
        serializer = Shop_Serializer(data=request.data)

        if serializer.is_valid():
            saved_shop = serializer.save()
            if saved_shop:
                return JsonResponse(data={"success": "Shop saved successfully"}, status=201)
            else:
                return JsonResponse({"error": "Shop couldn't be saved"})
        else:
            return JsonResponse(data=serializer.errors)

class Shop_Detail_View(views.APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        id = kwargs.get('id')
        shop_detail = shop.objects.get(id=id)

        serializer = Shop_Serializer(shop_detail)

        return JsonResponse(data=serializer.data)

class Shop_Delete_View(views.APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self,request,*args, **kwargs):
        id=kwargs.get('id')
        shop_detail = shop.objects.get(id=id)
        shop_detail.delete()
        return JsonResponse(data={'status':'deleted'})


class SignUpView(views.APIView):

    def post(self, request, *args, **kwargs):

        serializer = User_Serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone_no = serializer.validated_data['phone_no']

            CustomUser.objects.create_user(
                username=username, email=email, password=password, phone_no=phone_no)
            return JsonResponse(data={"status":"success"})
        else:
            return JsonResponse(data={'status':'failed'})


class LoginView(views.APIView):
    

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return JsonResponse(data={
                "errors": {
                     "__all__": "Please enter both username and password"
                     }
                }, status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            serializer = TokenObtainPairSerializer(data={'username':username,'password':password})
            serializer.is_valid(raise_exception=True)
            login(request, user)
            return JsonResponse(data ={'token':serializer.validated_data['access'],'refresh_token':serializer.validated_data['refresh']}, status=201)
        else:
            return JsonResponse({"errors": "Invalid credentials"},status=400 )


class LogoutView(views.APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request):
       
        logout(request)

        return JsonResponse(data={'status':'logged_out'})
