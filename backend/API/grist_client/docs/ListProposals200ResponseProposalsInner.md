# ListProposals200ResponseProposalsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Proposal ID | [optional] 
**src_doc_id** | **str** | Source document (fork) ID | [optional] 
**dest_doc_id** | **str** | Destination document (trunk) ID | [optional] 
**retracted** | **bool** | Whether the proposal has been retracted | [optional] 
**comparison** | [**DocComparison**](DocComparison.md) |  | [optional] 

## Example

```python
from grist_client.models.list_proposals200_response_proposals_inner import ListProposals200ResponseProposalsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListProposals200ResponseProposalsInner from a JSON string
list_proposals200_response_proposals_inner_instance = ListProposals200ResponseProposalsInner.from_json(json)
# print the JSON string representation of the object
print(ListProposals200ResponseProposalsInner.to_json())

# convert the object into a dict
list_proposals200_response_proposals_inner_dict = list_proposals200_response_proposals_inner_instance.to_dict()
# create an instance of ListProposals200ResponseProposalsInner from a dict
list_proposals200_response_proposals_inner_from_dict = ListProposals200ResponseProposalsInner.from_dict(list_proposals200_response_proposals_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


