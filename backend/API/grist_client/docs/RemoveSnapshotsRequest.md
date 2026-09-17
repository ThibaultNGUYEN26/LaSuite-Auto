# RemoveSnapshotsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_ids** | **List[str]** | List of snapshot IDs to remove | [optional] 

## Example

```python
from grist_client.models.remove_snapshots_request import RemoveSnapshotsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveSnapshotsRequest from a JSON string
remove_snapshots_request_instance = RemoveSnapshotsRequest.from_json(json)
# print the JSON string representation of the object
print(RemoveSnapshotsRequest.to_json())

# convert the object into a dict
remove_snapshots_request_dict = remove_snapshots_request_instance.to_dict()
# create an instance of RemoveSnapshotsRequest from a dict
remove_snapshots_request_from_dict = RemoveSnapshotsRequest.from_dict(remove_snapshots_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


