from rest_framework import generics, permissions, parsers
from .models import Snippet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SnippetSerializer, FileSerializer
import boto3

AWS_ACCESS_KEY_ID = 'ASIASSOBTA4SEPJHRFHD'
AWS_SECRET_ACCESS_KEY = 'nuAq6Urw+01Cnzt41A2O6inuKiId42Tca6/QWJEi'
AWS_TOKEN = 'FwoGZXIvYXdzEMH//////////wEaDJ0NhREQNbvCx0w0+SLOAR7gkBUTXk5UkSKc3asZrZxn8WxtUBvqvDpT/qvEpEf6aT3X5vO116/9+LnO5EdDL5wUhmioiJY1te124zRQq3o468YMWcaDRtnvwqhznBj97Gqtzejp2CmDzdcKPownLc6fz+7h0TaUWnpfu6+N1Tb1Tun6um38sYIdSirjoJ5QInDx0TJ0bhx971q+RZHsrkIpZIMjqJEZ6tXsMTIKY7oW/zNQnBaLSszrq1WnB+QnQo+jpkRUbyUiQJj/lv/AYIrWGfJPqhEY51/RO1Z/KPfwyfYFMi2kov8bPgPjoZVl3We6Gfrp0SwRGkQlqX9aXT+OYoNbmRQ2MslurEFYCq6Ve7Y='


class BotoClient:
    def __init__(self):
        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_TOKEN)
        s3 = session.resource('s3')
        self.client = s3.meta.client

    def upload_file(self, up_file):
        self.client.upload_file(Filename='filex.txt', Bucket='bucket1-yok', Key="filex.txt")


class FileUploadView(APIView):
    # http_method_names = ['GET', 'PUT', 'DELETE', 'POST']
    # permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        up_file = request.FILES['profile_pic']
        with open('temp/' + up_file.name, 'wb+') as file:
            for chunk in up_file.chunks():
                file.write(chunk)

        serializer = FileSerializer(data={})    # parse data to serializer
        if serializer.is_valid():
            serializer.save(name=up_file.name, size=up_file.size, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# @api_view(['GET', 'POST'])
# def simple_upload(request):
#     print("asd")
#     if request.method == 'POST' and request.FILES['my_file']:
#         my_file = request.FILES['my_file']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, my_file)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })

# class ProfilePictureView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = ProfilePictureSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser,)
#
#     @static
#     def perform_create(self, serializer):
#         print(self.request.FILES['profile_pic'])
#         serializer.save(user=User.objects.get(pk=2))
