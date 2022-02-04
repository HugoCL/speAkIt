from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import environ
import boto3

env = environ.Env()
environ.Env.read_env()

s3_client = boto3.client('s3', aws_access_key_id=env(
    'AWS_ACCESS_KEY_ID'), aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'))


class UploadViewSet(APIView):
    """
    This put method should receive a file in form-data with the name "audio_file".
    The API will put the file in the S3 bucket and return the URL of the file together with the response from AWS.
    """

    def put(self, request):
        print(request.data)
        audio_file = request.FILES['audio_file']
        if audio_file.content_type not in ['audio/mpeg', 'audio/mp3']:
            return Response({"message": "The file is not a valid audio file."})
        response = s3_client.put_object(
            Body=audio_file, Bucket=env('AWS_BUCKET_NAME'), Key=audio_file.name, ACL='public-read')
        if response:
            URL = "https://{}.s3.amazonaws.com/{}".format(
                env('AWS_BUCKET_NAME'), audio_file.name)
            return Response({"message": "Successfully uploaded file", "s3_url": URL, "aws_response": response})
        else:
            return Response({"message": "Failed to upload file", "aws_response": response})
