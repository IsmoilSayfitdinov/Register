from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwner
from .serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from .models import BlogModel
from rest_framework import generics
from blog.paginations import CustomPagination

class BlogsCreate(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": 200, "message": "Blog created successfully"})
        else:
            return Response({"status": 400, "message": "Blog not created"})

class BlogeUpdate(APIView):
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = BlogSerializer
    
    def put(self, request, pk):
        blog = BlogModel.objects.filter(id=pk)
        
        if not blog.exists():
            return Response({"status": 400, "message": "Blog not found"})
        
        serializer = BlogSerializer(blog.first(), data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "Blog updated successfully"})
        else:
            return Response({"status": 400, "message": "Blog not updated"})
    
    
class BlogDelete(APIView):
    permission_classes = [IsOwner]
    serializer_class = BlogSerializer
    
    def delete(self, request, pk):
        blog = BlogModel.objects.filter(id=pk)
        
        if not blog.exists():
            return Response({"status": 400, "message": "Blog not found"})
        
        blog.delete()
        return Response({"status": 200, "message": "Blog deleted successfully"})
    
    
class BlogList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer 
    pagination_class = CustomPagination
    def get_queryset(self):
        return BlogModel.objects.all()
        
         
    
class BlogDeatail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    
    def get(self, request, pk):
        blog = BlogModel.objects.filter(id=pk)
        
        if not blog.exists():
            return Response({"status": 400, "message": "Blog not found"})
        
        serializer = BlogSerializer(blog.first())
        return Response({"status": 200, "data": serializer.data})


class MySelfBlog(APIView):
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = BlogSerializer
    
    def get(self, request):
        blog = BlogModel.objects.filter(user=request.user)
        serializes = BlogSerializer(blog, many=True)
        
        return Response({"status": 200, "data": serializes.data}) 

    