from rest_framework.viewsets import ModelViewSet
from .models import Movie,Actor,Comment
from .serializers import MovieSerializer,ActorSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import TrigramSimilarity

class MovieViewSet(ModelViewSet):
  queryset=Movie.objects.all()
  serializer_class=MovieSerializer
  filter_backends=(SearchFilter,OrderingFilter)
  ordering_fields=('-watch','watch')
  search_fields=('name',)

  @action(detail=True, methods=['POST'])
  def add_actor(self,request,*args,**kwargs):
    movie=self.get_object()
    actor=Actor.objects.get_or_create(name=request.data['name'],birthdate=request.data['birthdate'],gender=request.data['gender'])
    print(type(actor))
    movie.actors.add(actor[0])
    return Response(status=status.HTTP_202_ACCEPTED)
  
  @action(methods=['POST'],detail=True)
  def remove_actor(self,request,*args,**kwargs):
    movie=self.get_object()
    actor=movie.actors.last()
    movie.actors.remove(actor)
    return Response(status=status.HTTP_202_ACCEPTED)
  
  @action(methods=['POST'],detail=True)
  def watchs(self, request,*args,**kwargs):
    movie=self.get_object()

    with transaction.atomic():
      movie.watch+=1
      movie.save()
    
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  @action(methods=['GET'],detail=False)
  def top(self, request,*args,**kwargs):
    movie=self.get_queryset()
    movie=movie.order_by('-watch')[:10]
    serializer=MovieSerializer(movie,many=True)
    return Response(serializer.data)

class ActorViewSet(ModelViewSet):
  def get_queryset(self):
    queryset=Actor.objects.all()
    search = self.request.query_params.get('search')
    if search is not None:
      queryset=queryset.annotate(similarity=TrigramSimilarity('name',search)).filter(
        similarity__gt=0.4
      ).order_by('-similarity')
    
    return queryset

  serializer_class=ActorSerializer
  filter_backends=(OrderingFilter,)
  ordiring_fields=['gender']






class MovieAPIView(APIView):
  def get(self,request):
    movie=Movie.objects.all()
    serializer=MovieSerializer(data=movie).data
    return Response(data=serializer)
  
  def post(self,request):
    serializer=MovieSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
  
  def put(self,req,pk):
    movie=Movie.objects.filter(pk=pk)
    serializer=MovieSerializer(instance=movie,data=req.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data=serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self,req,pk):
    movie=Movie.objects.filter(pk=pk)
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ActorAPIView(APIView):

  def get_object(self,pk):
    try:
      return Actor.objects.get(pk=pk)
    except Exception as e:
      raise e
    
  def get(self, request):
    actor=Actor.objects.all()
    serializer=ActorSerializer(actor,many=True)
    return Response(data=serializer.data)
  
  def put(self,request,pk):
    actor=self.get_object(pk)
    serializer=ActorSerializer(actor,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data=serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self,request,pk):
    actor=self.get_object(pk)
    actor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class MovieActorAPIView(APIView):
  def get(self,request,pk):
    movie=Movie.objects.get(pk=pk)
    actor=movie.actors.all()
    serializer=ActorSerializer(actor,many=True)
    return Response(data=serializer.data)

class CommentAPIView(APIView):
  permission_classes=[IsAuthenticated]
  authentication_classes=[TokenAuthentication]

  def get(self,req):
    comment=Comment.objects.all()
    serializer=CommentSerializer(comment,many=True)
    return Response(serializer.data)

  def post(self,request):
    serializer=CommentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self,req,pk):
    pass

  def delete(self,req,pk):
    comment = Comment.objects.filter(order=pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)