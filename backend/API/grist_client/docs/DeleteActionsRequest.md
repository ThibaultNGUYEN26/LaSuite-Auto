# DeleteActionsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**keep** | **int** | The number of the latest history actions to keep | 

## Example

```python
from grist_client.models.delete_actions_request import DeleteActionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteActionsRequest from a JSON string
delete_actions_request_instance = DeleteActionsRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteActionsRequest.to_json())

# convert the object into a dict
delete_actions_request_dict = delete_actions_request_instance.to_dict()
# create an instance of DeleteActionsRequest from a dict
delete_actions_request_from_dict = DeleteActionsRequest.from_dict(delete_actions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


