# ForkDoc200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fork_id** | **str** | The unique identifier for this fork | 
**doc_id** | **str** | The full document ID of the fork | 
**url_id** | **str** | The URL-friendly ID of the fork | 

## Example

```python
from grist_client.models.fork_doc200_response import ForkDoc200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ForkDoc200Response from a JSON string
fork_doc200_response_instance = ForkDoc200Response.from_json(json)
# print the JSON string representation of the object
print(ForkDoc200Response.to_json())

# convert the object into a dict
fork_doc200_response_dict = fork_doc200_response_instance.to_dict()
# create an instance of ForkDoc200Response from a dict
fork_doc200_response_from_dict = ForkDoc200Response.from_dict(fork_doc200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


