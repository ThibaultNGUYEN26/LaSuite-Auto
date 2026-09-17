# DocParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**is_pinned** | **bool** |  | [optional] 

## Example

```python
from grist_client.models.doc_parameters import DocParameters

# TODO update the JSON string below
json = "{}"
# create an instance of DocParameters from a JSON string
doc_parameters_instance = DocParameters.from_json(json)
# print the JSON string representation of the object
print(DocParameters.to_json())

# convert the object into a dict
doc_parameters_dict = doc_parameters_instance.to_dict()
# create an instance of DocParameters from a dict
doc_parameters_from_dict = DocParameters.from_dict(doc_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


