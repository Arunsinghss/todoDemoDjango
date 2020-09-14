from django.contrib.auth.models import User
from bucket.serializers import TodoSerializer, BucketSerializer, UserSerializer
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from bucket.models import Bucket, Todo
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        params = request.data if request.data else request.POST
        bucket = params.get('task_bucket', None)
        kwargs = {
            'task':  params.get('task', ''),
            'is_completed':  params.get('is_completed', False),
            'created_by': request.user.id
        }

        if not kwargs.get('task'):
            return JsonResponse({"message": "Please Provide task ..."}, status=400)
        if bucket:
            kwargs['task_bucket'] = Bucket.objects.get(id=bucket)

        try:
            task = self.get_serializer(data=kwargs)
            task.is_valid(raise_exception=True)
            task_obj = task.save()
            return JsonResponse({"message": "Todo Task Added Successfully...", "data": task.data}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            params = request.data if request.data else request.POST
            if not params.get('task'):
                return JsonResponse({"message": "Please Provide task ..."}, status=400)
            todo = Todo.objects.get(pk=pk)
            todo.task = params.get('task', '')
            bucket = params.get('task_bucket', None)
            if bucket:
                todo.task_bucket = Bucket.objects.get(id=bucket)
            todo.is_completed = params.get('is_completed', False)
            todo.modified_by = request.user
            todo.save()
            tododata = self.serializer_class(todo).data
            return JsonResponse({"message": "Todo Task Updated Successfully...", "data": tododata}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            todo = Todo.objects.filter(id=pk).first()
            if todo:
                todo.delete()
                return JsonResponse({"message": "Todo Task deleted Successfully...", "data": {}}, status=200)
            else:
                return JsonResponse({"message": "No Such Task...", "data": {}}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class BucketViewset(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        params = request.data if request.data else request.POST
        kwargs = {
            'name':  params.get('name', ''),
            'created_by': request.user.id
        }
        if not kwargs.get('name'):
            return JsonResponse({"message": "Please Provide Bucket Name ..."}, status=400)

        try:
            bucket = self.get_serializer(data=kwargs)
            bucket.is_valid(raise_exception=True)
            bucket_obj = bucket.save()
            return JsonResponse({"message": "Bucket Added Successfully...", "data": bucket.data}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            params = request.data if request.data else request.POST
            if not params.get('name'):
                return JsonResponse({"message": "Please Provide Bucket Name ..."}, status=400)
            bucket = Bucket.objects.get(pk=pk)
            bucket.name = params.get('name', '')
            bucket.modified_by = request.user
            bucket.save()
            bucketdata = self.serializer_class(bucket).data
            return JsonResponse({"message": "Bucket Updated Successfully...", "data": bucketdata}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class LoginViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # default user will get or create while login so no need to handle in frontend for now
    def create(self, request, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="arun", first_name="arun", last_name="singh")
        if created:
            user.is_superuser = True
            user.is_staff = user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"message": "User Added Successfully...", "user": user.username, "token": token.key}, status=200)
