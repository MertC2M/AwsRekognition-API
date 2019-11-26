from chalice import Chalice
from botocore.exceptions import ClientError
import boto3

app = Chalice(app_name='AwsRekognition-API')
app.debug = False

client = boto3.client('rekognition')
s3 = boto3.resource('s3')


@app.route('/detect_labels_in_image')
def detect_labels_in_image():
    s3_image = app.current_request.query_params.get('s3_image')
    try:
        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'rekognitiontrialbucketnudephotos',
                    'Name': s3_image,
                }
            }
        )
        return response
    except ClientError as e:
        return {"status": "Error: %s" % e.response['Error']['Message']}


@app.route('/detect_texts_in_image')
def detect_texts_in_image():
    s3_image = app.current_request.query_params.get('s3_image')
    try:
        response = client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': 'rekognitiontrialbucketc2m',
                    'Name': s3_image,
                }
            }
        )
        return response
    except ClientError as e:
        return {"status": "Error: %s" % e.response['Error']['Message']}


@app.route('/')
def index():
    return {'hello': 'world'}
