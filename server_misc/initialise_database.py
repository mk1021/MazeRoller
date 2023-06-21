import boto3


def create_mvmnt_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'string',
                'AttributeType': 'S' | 'N' | 'B'
            },
        ],
        TableName='string',
        KeySchema=[
            {
                'AttributeName': 'string',
                'KeyType': 'HASH' | 'RANGE'
            },
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                }
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            },
        ],
        StreamSpecification={
            'StreamEnabled': True | False,
            'StreamViewType': 'NEW_IMAGE' | 'OLD_IMAGE' | 'NEW_AND_OLD_IMAGES' | 'KEYS_ONLY'
        },
        SSESpecification={
            'Enabled': True | False,
            'SSEType': 'AES256' | 'KMS',
            'KMSMasterKeyId': 'string'
        },
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        TableClass='STANDARD' | 'STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=True | False
    )

    if not response:
        raise ConnectionRefusedError("could not create mvmnt table")


def create_corner_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'string',
                'AttributeType': 'S' | 'N' | 'B'
            },
        ],
        TableName='string',
        KeySchema=[
            {
                'AttributeName': 'string',
                'KeyType': 'HASH' | 'RANGE'
            },
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                }
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            },
        ],
        StreamSpecification={
            'StreamEnabled': True | False,
            'StreamViewType': 'NEW_IMAGE' | 'OLD_IMAGE' | 'NEW_AND_OLD_IMAGES' | 'KEYS_ONLY'
        },
        SSESpecification={
            'Enabled': True | False,
            'SSEType': 'AES256' | 'KMS',
            'KMSMasterKeyId': 'string'
        },
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        TableClass='STANDARD' | 'STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=True | False
    )

    if not response:
        raise ConnectionRefusedError("could not create corner table")


def create_path_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'string',
                'AttributeType': 'S' | 'N' | 'B'
            },
        ],
        TableName='string',
        KeySchema=[
            {
                'AttributeName': 'string',
                'KeyType': 'HASH' | 'RANGE'
            },
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                }
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            },
        ],
        StreamSpecification={
            'StreamEnabled': True | False,
            'StreamViewType': 'NEW_IMAGE' | 'OLD_IMAGE' | 'NEW_AND_OLD_IMAGES' | 'KEYS_ONLY'
        },
        SSESpecification={
            'Enabled': True | False,
            'SSEType': 'AES256' | 'KMS',
            'KMSMasterKeyId': 'string'
        },
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        TableClass='STANDARD' | 'STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=True | False
    )

    if not response:
        raise ConnectionRefusedError("could not create path table")


def create_backup_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'string',
                'AttributeType': 'S' | 'N' | 'B'
            },
        ],
        TableName='string',
        KeySchema=[
            {
                'AttributeName': 'string',
                'KeyType': 'HASH' | 'RANGE'
            },
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                }
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'string',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH' | 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL' | 'KEYS_ONLY' | 'INCLUDE',
                    'NonKeyAttributes': [
                        'string',
                    ]
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            },
        ],
        StreamSpecification={
            'StreamEnabled': True | False,
            'StreamViewType': 'NEW_IMAGE' | 'OLD_IMAGE' | 'NEW_AND_OLD_IMAGES' | 'KEYS_ONLY'
        },
        SSESpecification={
            'Enabled': True | False,
            'SSEType': 'AES256' | 'KMS',
            'KMSMasterKeyId': 'string'
        },
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        TableClass='STANDARD' | 'STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=True | False
    )

    if not response:
        raise ConnectionRefusedError("could not create backup table")


def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    create_mvmnt_table(dynamodb)
    create_corner_table(dynamodb)
    create_path_table(dynamodb)
    create_backup_table(dynamodb)

    print("tables successfully created")

    return dynamodb
