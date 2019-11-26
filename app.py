from chalice import Chalice
from botocore.exceptions import ClientError
import boto3

app = Chalice(app_name='AwsRekognition-API')
app.debug = False

client = boto3.client('rekognition')
s3 = boto3.resource('s3')


@app.route('/detect_labels_in_image')
def detect_labels_in_image():
    all_labels = []
    s3_image = app.current_request.query_params.get('s3_image')
    try:
        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'rekognitiontrialbucketnudephotos',
                    'Name': s3_image,
                }
            },
            MaxLabels=10
        )
        for label in response['Labels']:
            all_labels.append('Label: ' + '%s' % label['Name'] + ' Confidence: ' + '%s' % label['Confidence'])
        return all_labels
    except ClientError as e:
        return {"status": "Error: %s" % e.response['Error']['Message']}


@app.route('/detect_texts_in_image')
def detect_texts_in_image():
    s3_image = app.current_request.query_params.get('s3_image')
    all_texts = []
    try:
        response = client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': 'rekognitiontrialbucketc2m',
                    'Name': s3_image,
                }
            }
        )
        for text in response['TextDetections']:
            all_texts.append(
                'DetectedText: ' + '%s' % text['DetectedText'] + ' Confidence: %' + '{:.2f}'.format(text['Confidence']))
        return all_texts
    except ClientError as e:
        return {"status": "Error: %s" % e.response['Error']['Message']}


@app.route('/detect_moderation_label_in_image')
def detect_moderation_label_in_image():
    s3_image = app.current_request.query_params.get('s3_image')
    all_moderation_labels = []
    try:
        response = client.detect_moderation_labels(
            Image={
                'S3Object': {
                    'Bucket': 'rekognitiontrialbucketnudephotos',
                    'Name': s3_image,
                }
            },
            MinConfidence=70,
        )
        for label in response['ModerationLabels']:
            all_moderation_labels.append(
                'Name: ' + '%s' % label['Name'] + ' ParentName: ' + '%s' % label['ParentName']
                + ' Confidence: %' + '{:.2f}'.format(label['Confidence']))
        return all_moderation_labels
    except ClientError as e:
        return {"status": "Error: %s" % e.response['Error']['Message']}


@app.route('/')
def index():
    return {'hello': 'world'}
