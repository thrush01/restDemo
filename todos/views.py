from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Todo
from rest_framework import filters
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from todos.pagination import CustomPageNumberPagination


class TodoAPIView(ListCreateAPIView):
    serializer_class=TodoSerializer
    pagination_class=CustomPageNumberPagination
    permission_classes=(IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_fields=['id','title','is_completed']
    search_fields=['id','title','is_completed']
    ordering_fields=['id','title','is_completed']

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=TodoSerializer
    permission_classes=(IsAuthenticated,)
    lookup_field='id'


    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)





# @method_decorator(csrf_exempt, name='dispatch')
# class CreateTodoAPIView(CreateAPIView):
#    # queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes=(IsAuthenticated,)

#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)
# class TodoListAPIView(ListAPIView):
    
#     serializer_class = TodoSerializer
#     permission_classes=(IsAuthenticated,)

#     def get_queryset(self):
#         return Todo.objects.filter(owner=self.request.user)