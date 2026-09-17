# ListSnapshots200ResponseSnapshotsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_id** | **str** | Unique identifier for the snapshot | 
**last_modified** | **datetime** | When the snapshot was created | 
**doc_id** | **str** | Document ID that can be used to open this snapshot | 

## Example

```python
from grist_client.models.list_snapshots200_response_snapshots_inner import ListSnapshots200ResponseSnapshotsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListSnapshots200ResponseSnapshotsInner from a JSON string
list_snapshots200_response_snapshots_inner_instance = ListSnapshots200ResponseSnapshotsInner.from_json(json)
# print the JSON string representation of the object
print(ListSnapshots200ResponseSnapshotsInner.to_json())

# convert the object into a dict
list_snapshots200_response_snapshots_inner_dict = list_snapshots200_response_snapshots_inner_instance.to_dict()
# create an instance of ListSnapshots200ResponseSnapshotsInner from a dict
list_snapshots200_response_snapshots_inner_from_dict = ListSnapshots200ResponseSnapshotsInner.from_dict(list_snapshots200_response_snapshots_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


