# ApplyProposal200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**proposal_id** | **int** |  | [optional] 
**changes** | **object** | Summary of changes applied | [optional] 

## Example

```python
from grist_client.models.apply_proposal200_response import ApplyProposal200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyProposal200Response from a JSON string
apply_proposal200_response_instance = ApplyProposal200Response.from_json(json)
# print the JSON string representation of the object
print(ApplyProposal200Response.to_json())

# convert the object into a dict
apply_proposal200_response_dict = apply_proposal200_response_instance.to_dict()
# create an instance of ApplyProposal200Response from a dict
apply_proposal200_response_from_dict = ApplyProposal200Response.from_dict(apply_proposal200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


