import boto3


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_object_url(date, candid):
    return create_presigned_url("alerce-challenges", "ztf_{}_programid1/{}.avro".format(date,candid))

def upload_file(f, date, candid):
    s3 = boto3.client('s3')
    BUCKET_NAME = "alerce-challenges"
    OBJECT_NAME = "ztf_{}_programid1/{}.avro".format(date,candid)
    s3.upload_fileobj(f, BUCKET_NAME, OBJECT_NAME)
    return get_object_url(date,candid)
