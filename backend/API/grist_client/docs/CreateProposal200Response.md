# CreateProposal200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Proposal ID | [optional] 
**comparison** | [**DocComparison**](DocComparison.md) |  | [optional] 

## Example

```python
from grist_client.models.create_proposal200_response import CreateProposal200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateProposal200Response from a JSON string
create_proposal200_response_instance = CreateProposal200Response.from_json(json)
# print the JSON string representation of the object
print(CreateProposal200Response.to_json())

# convert the object into a dict
create_proposal200_response_dict = create_proposal200_response_instance.to_dict()
# create an instance of CreateProposal200Response from a dict
create_proposal200_response_from_dict = CreateProposal200Response.from_dict(create_proposal200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


