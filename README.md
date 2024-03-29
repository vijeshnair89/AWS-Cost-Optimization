This is a python project which identifies the stale resources like snapshots in this case and deletes the resource to avoid getting charged from AWS...

Scenario on which the resource will be removed:

Scenario 1:
If there is snapshot which has not volume attached to it will be deleted.

Scenario 2:
If there is a snapshot with a volume attached but the volume has no running instance attached, then the snapshot will be removed.
