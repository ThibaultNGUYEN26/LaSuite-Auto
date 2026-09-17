# CreateProposalRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**retracted** | **bool** | Set to true to retract an existing proposal | [optional] [default to False]

## Example

```python
from grist_client.models.create_proposal_request import CreateProposalRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateProposalRequest from a JSON string
create_proposal_request_instance = CreateProposalRequest.from_json(json)
# print the JSON string representation of the object
print(CreateProposalRequest.to_json())

# convert the object into a dict
create_proposal_request_dict = create_proposal_request_instance.to_dict()
# create an instance of CreateProposalRequest from a dict
create_proposal_request_from_dict = CreateProposalRequest.from_dict(create_proposal_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


