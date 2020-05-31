import os
import mimetypes
import configparser
import boto3


class Boto3Client:
    def __init__(self, user):
        # Read configuration file
        config_parser = configparser.RawConfigParser()
        config_file_path = r'.aws/credentials'
        config_parser.read(config_file_path)

        session = boto3.Session(aws_access_key_id=config_parser.get('default', 'aws_access_key_id'),
                                aws_secret_access_key=config_parser.get('default', 'aws_secret_access_key'),
                                aws_session_token=config_parser.get('default', 'aws_session_token'))
        s3 = session.resource('s3')
        self.client = s3.meta.client

        self.bucket_name = 'bucket-yok-{}'.format(user.username)
        # Create one temp directory for each user

        dir_name = 'temp/{}'.format(self.bucket_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def upload_file(self, up_file):
        self.create_bucket()

        temp_file_path = 'temp/{}/{}'.format(self.bucket_name, up_file.name)
        with open(temp_file_path, 'wb+') as file:
            for chunk in up_file.chunks():
                file.write(chunk)

        self.client.upload_file(Filename=temp_file_path, Bucket=self.bucket_name, Key=up_file.name)
        os.remove(temp_file_path)

    def create_bucket(self):
        """
        If the user does not have a bucket, then create it.
        Bucket name 'bucket-yok-{username}'
        """

        buckets = self.client.list_buckets()
        buckets_names = [buck['Name'] for buck in buckets['Buckets']]

        if self.bucket_name not in buckets_names:
            self.client.create_bucket(Bucket=self.bucket_name)

    def list_files(self):
        res = self.client.list_objects(Bucket=self.bucket_name)
        files = res['Contents']
        return files

    def get_file(self, filename):
        temp_save_path = 'temp/{}/{}'.format(self.bucket_name, filename)
        self.client.download_file(Filename=temp_save_path, Bucket=self.bucket_name, Key=filename)

        file_content = open(temp_save_path, 'rb')
        mime_type, _ = mimetypes.guess_type(temp_save_path)
        # os.remove(temp_save_path)

        return file_content, mime_type
