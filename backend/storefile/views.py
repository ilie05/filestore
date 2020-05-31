from rest_framework import generics, permissions, parsers
from .models import Snippet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SnippetSerializer, FileSerializer
from .s3_utils import Boto3Client


class FileUploadView(APIView):
    # http_method_names = ['GET', 'PUT', 'DELETE', 'POST']
    # permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        up_file = request.FILES['profile_pic']

        boto_client = Boto3Client(request.user)
        boto_client.upload_file(up_file)

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
