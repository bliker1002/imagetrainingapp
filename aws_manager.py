import boto3
import json

class AWSManager:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.ec2 = boto3.client('ec2')
        self.lambda_client = boto3.client('lambda')
        self.sagemaker = boto3.client('sagemaker')

        self.AWS_ACCESS_KEY = 'your_access_key_here'
        self.AWS_SECRET_KEY = 'your_secret_key_here'
        self.BUCKET_NAME = 'ai-image-model-maker'
        self.EC2_INSTANCE_ID = 'your_ec2_instance_id_here'

    def upload_file(self, s3_key, local_path):
        self.s3.upload_file(local_path, self.BUCKET_NAME, s3_key)

    def upload_model(self, user_id, model_path):
        self.s3.upload_file(model_path, self.BUCKET_NAME, f'{user_id}/{user_id}.tar.gz')

    def start_training_job(self, user_id):
        self.start_ec2_instance()
        self.lambda_client.invoke(
            FunctionName='start-training-job',
            InvocationType='Event',
            Payload=json.dumps({'user_id': user_id})
        )

    def run_inference(self, user_id, prompt):
        response = self.sagemaker.invoke_endpoint(
            EndpointName=f'model-{user_id}',
            ContentType='application/json',
            Body=json.dumps({'prompt': prompt})
        )
        return json.loads(response['Body'].read().decode())['image_url']

    def start_ec2_instance(self):
        self.ec2.start_instances(InstanceIds=[self.EC2_INSTANCE_ID])

    def stop_ec2_instance(self):
        self.ec2.stop_instances(InstanceIds=[self.EC2_INSTANCE_ID])