# Doc


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**is_pinned** | **bool** |  | 
**url_id** | **str** |  | 

## Example

```python
from grist_client.models.doc import Doc

# TODO update the JSON string below
json = "{}"
# create an instance of Doc from a JSON string
doc_instance = Doc.from_json(json)
# print the JSON string representation of the object
print(Doc.to_json())

# convert the object into a dict
doc_dict = doc_instance.to_dict()
# create an instance of Doc from a dict
doc_from_dict = Doc.from_dict(doc_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


