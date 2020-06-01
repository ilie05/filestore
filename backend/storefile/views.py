import os
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

        up_file = req.FILES['file_content']
        boto_client = Boto3Client(req.user)
        boto_client.upload_file(up_file)

        serializer = FileSerializer(data={})  # parse data to serializer
        if serializer.is_valid():
            serializer.save(name=up_file.name, size=up_file.size, user=req.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, req):
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        filename = req.query_params.get('name')
        boto_client = Boto3Client(req.user)
        file_content, mime_type = boto_client.get_file(filename)

        response = LogSuccessResponse(file_content, content_type=mime_type)
        response['filepath'] = 'temp/{}/{}'.format(boto_client.bucket_name, filename)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    def delete(self, req):
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        filename = req.data.get('filename')
        boto_client = Boto3Client(req.user)
        boto_client.delete_file(filename)

        return Response(status=status.HTTP_204_NO_CONTENT)


class LogSuccessResponse(HttpResponse):
    def close(self):
        super(LogSuccessResponse, self).close()
        # get the file to be deleted from header, then delete the header
        if self.status_code == 200:
            file_to_delete = self._headers['filepath'][1]
            del self._headers['filepath']
            os.remove(file_to_delete)


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


# class ProfilePictureView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = ProfilePictureSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser,)
#
#     @static
#     def perform_create(self, serializer):
#         print(self.request.FILES['profile_pic'])
#         serializer.save(user=User.objects.get(pk=2))
