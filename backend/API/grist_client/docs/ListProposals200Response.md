# ListProposals200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**proposals** | [**List[ListProposals200ResponseProposalsInner]**](ListProposals200ResponseProposalsInner.md) |  | [optional] 

## Example

```python
from grist_client.models.list_proposals200_response import ListProposals200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListProposals200Response from a JSON string
list_proposals200_response_instance = ListProposals200Response.from_json(json)
# print the JSON string representation of the object
print(ListProposals200Response.to_json())

# convert the object into a dict
list_proposals200_response_dict = list_proposals200_response_instance.to_dict()
# create an instance of ListProposals200Response from a dict
list_proposals200_response_from_dict = ListProposals200Response.from_dict(list_proposals200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


