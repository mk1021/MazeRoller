import boto3
import math


# TODO: design table and translate into code
def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

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

    return response


def update_table(where, data_things):
    print("hi")
    # TODO: write the up to data thing, idk


def data_to_distance(sth):  # TODO: add relevant conversion calculation
    return sth


def new_coord(prev_coord, data):
    cur_coord = [0, 0]
    # assuming movement data (preferably with heading/bearing) is sent as a list, assume [steps_moved, bearing]

    distance_moved = data_to_distance(data[0])

    cur_coord[0] = prev_coord[0] + round(distance_moved * math.sin(data[1]))
    cur_coord[1] = prev_coord[1] + round(distance_moved * math.cos(data[1]))

    # TODO: any other information we can pull from the coord and heading now?
    #       sth to help build the map, preferably

    return cur_coord


def main():
    coord = [0, 0]
    print("hi")

    db_obj = create_table()

    # to be looped inside server thing
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # when receive new coords
    mvmnt_data = [5, math.pi/2]
    coord = new_coord(coord, mvmnt_data)

    # TODO: add other things to update table with

    update_table(db_obj, coord)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # not sure if there even needs to be more code outside the loop, but here we are


if __name__ == '__main__':
    main()
