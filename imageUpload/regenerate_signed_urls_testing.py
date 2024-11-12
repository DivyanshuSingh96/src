import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config

from decouple import config as env_config

def regenerate_signed_url(file_path):
    # Initialize boto3 client with Cloudflare R2 credentials
    session = boto3.session.Session()
    account_id = env_config("CLOUDFLARE_ACCOUNT_ID")
    access_key = env_config("CLOUDFLARE_R2_ACCESS_KEY")
    secret_key = env_config("CLOUDFLARE_R2_SECRET_KEY")
    bucket_name = env_config("CLOUDFLARE_R2_BUCKET")

    s3_client = boto3.client(
        's3',
        # endpoint_url=F'https://{account_id}.r2.cloudflarestorage.com',  # Replace with your Cloudflare R2 endpoint
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

    expiration_time = 3600  # URL expiration in seconds (1 hour)

    try:
        new_file_path = file_path.split('cloudflarestorage.com')[1].split("?")[0]
        # Generate presigned URL for the image in Cloudflare R2
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name, 'Key': new_file_path},
                                               ExpiresIn=expiration_time)

        final_url = f"https://64646f9b5ea8571f2ced7edbd8036eb4.r2.cloudflarestorage.com/{url.split('.com')[1][2:]}"
        
        return final_url
    except NoCredentialsError:
        return None

# Example usage
bucket_name = env_config("CLOUDFLARE_R2_BUCKET")
object_key = 'https://64646f9b5ea8571f2ced7edbd8036eb4.r2.cloudflarestorage.com/csp/media/images/0/a580f57d-a027-11ef-a2eb-d843aeb854c8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ec9cfb9b2a842510c277484e30881b81%2F20241111%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241111T122242Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b18079fd8ae08c5a08648d8c52427deedadf87a47511b549920437decffc183d'  # Replace with the actual object path in your R2 bucket
presigned_url = regenerate_signed_url(object_key)
print(f"Generated signed URL: {presigned_url}")
