import boto3

client = boto3.client('ec2')

response = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
                'pending',
            ],
        },
    ],
)

instanceset = set()
volumeset=set()
snapshotset=set()
for reservation in response["Reservations"]:
    for instances in reservation["Instances"]:
        instanceset.add(instances["InstanceId"])

print("Available instances: ",instanceset)
volumes = client.describe_volumes(
    Filters = [
        {
            'Name': 'status',
            'Values': [
                'available',
                'in-use',
            ],
        },   
    ],
)

for volume in volumes['Volumes']:
        volumeset.add(volume['VolumeId'])

print("Avalable Volumes : " ,volumeset)

snapshots = client.describe_snapshots(
    OwnerIds = [
        'self'
    ]
)

for snapshot in snapshots['Snapshots']:
    snapshotid = snapshot['SnapshotId']
    volumeid = snapshot['VolumeId']
   

    if volumeid not in volumeset:
        print(f"Snapshot {snapshotid} does not belong to any volume...Deleting snapshot")
        client.delete_snapshot(SnapshotId=snapshotid)
    else:
        volumedesc = client.describe_volumes(VolumeIds=[volumeid])
        if not volumedesc['Volumes'][0]['Attachments']:
            print(f"Snapshot {snapshotid} attached to a volume which has no attached instances.. Deleting snapshot")
            client.delete_snapshot(SnapshotId=snapshotid)
        else:
            print(f"Snapshot {snapshotid} is Valid")
            snapshotset.add(snapshotid)

print(f"Available Snapshots: {snapshotset}")
