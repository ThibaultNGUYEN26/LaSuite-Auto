# RemoveSnapshots200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_ids** | **List[str]** | The snapshot IDs that were removed | [optional] 

## Example

```python
from grist_client.models.remove_snapshots200_response import RemoveSnapshots200Response

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveSnapshots200Response from a JSON string
remove_snapshots200_response_instance = RemoveSnapshots200Response.from_json(json)
# print the JSON string representation of the object
print(RemoveSnapshots200Response.to_json())

# convert the object into a dict
remove_snapshots200_response_dict = remove_snapshots200_response_instance.to_dict()
# create an instance of RemoveSnapshots200Response from a dict
remove_snapshots200_response_from_dict = RemoveSnapshots200Response.from_dict(remove_snapshots200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


