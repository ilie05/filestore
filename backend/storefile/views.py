from django.http import HttpResponse
from rest_framework import generics, permissions, parsers
from .models import Snippet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SnippetSerializer, FileSerializer
from .s3_utils import Boto3Client


class FileView(APIView):
    def post(self, req):
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        up_file = req.FILES['profile_pic']

        boto_client = Boto3Client(req.user)
        boto_client.upload_file(up_file)

        serializer = FileSerializer(data={})  # parse data to serializer
        if serializer.is_valid():
            serializer.save(name=up_file.name, size=up_file.size, user=req.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, req):
        filename = req.query_params.get('name')

        boto_client = Boto3Client(req.user)
        file_content, mime_type = boto_client.get_file(filename)

        response = HttpResponse(file_content, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response


class FilesView(APIView):
    def get(self, req):
        boto_client = Boto3Client(req.user)
        files = boto_client.list_files()
        return Response(files, status=status.HTTP_200_OK)


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
