import boto3


def create_mvmnt_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'itemNum',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'xCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'yCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'heading',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'followingLeftWall',
                'AttributeType': 'B'
            },
            {
                'AttributeName': 'localisationNum',
                'AttributeType': 'N'
            }
        ],
        TableName='Movement',
        KeySchema=[
            {
                'AttributeName': 'itemNum',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'localisationNum',
                'KeyType': 'RANGE'
            },
        ],
        StreamSpecification={
            'StreamEnabled': False
        },
        SSESpecification={
            'Enabled': False
        },
        TableClass='STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=False
    )

    if not response:
        raise ConnectionRefusedError("could not create mvmnt table")


def create_corner_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'itemNum',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'xCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'yCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'distanceToGoal',
                'AttributeType': 'N'
            },
        ],
        TableName='Corners',
        KeySchema=[
            {
                'AttributeName': 'itemNum',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'xCoord',
                'KeyType': 'RANGE'
            },
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'ySweep',
                'KeySchema': [
                    {
                        'AttributeName': 'yCoord',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            },
        ],
        StreamSpecification={
            'StreamEnabled': False
        },
        SSESpecification={
            'Enabled': False
        },
        TableClass= 'STANDARD',
        DeletionProtectionEnabled=True
    )

    if not response:
        raise ConnectionRefusedError("could not create corner table")


def create_path_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'xCoord',
                'AttributeType': 'N'
            },
                        {
                'AttributeName': 'yCoord',
                'AttributeType': 'N'
            },
                        {
                'AttributeName': 'localisationNum',
                'AttributeType': 'N'
            }
        ],
        TableName='PathSquares',
        KeySchema=[
            {
                'AttributeName': 'xCoord',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'yCoord',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'localisationNum',
                'KeyType': 'RANGE'
            },
        ],
        StreamSpecification={
            'StreamEnabled': False
        },
        SSESpecification={
            'Enabled': False
        },
        TableClass= 'STANDARD',
        DeletionProtectionEnabled=True
    )

    if not response:
        raise ConnectionRefusedError("could not create path table")


def create_backup_table(dynamodb):
    if not dynamodb:
        raise ResourceWarning("dynamodb object does not exist")

    response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'itemNum',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'xCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'yCoord',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'heading',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'localisationNum',
                'AttributeType': 'N'
            }
        ],
        TableName='Movement',
        KeySchema=[
            {
                'AttributeName': 'itemNum',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'localisationNum',
                'KeyType': 'RANGE'
            },
        ],
        StreamSpecification={
            'StreamEnabled': False
        },
        SSESpecification={
            'Enabled': False
        },
        TableClass='STANDARD_INFREQUENT_ACCESS',
        DeletionProtectionEnabled=True
    )

    if not response:
        raise ConnectionRefusedError("could not create backup table")


def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    create_mvmnt_table(dynamodb)
    create_corner_table(dynamodb)
    create_path_table(dynamodb)
#    create_backup_table(dynamodb)

    print("tables successfully created")

    return dynamodb
