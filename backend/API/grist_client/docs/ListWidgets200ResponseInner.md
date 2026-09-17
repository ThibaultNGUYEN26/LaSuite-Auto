# ListWidgets200ResponseInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Widget display name | [optional] 
**url** | **str** | URL to load the widget | [optional] 
**widget_id** | **str** | Unique widget identifier | [optional] 

## Example

```python
from grist_client.models.list_widgets200_response_inner import ListWidgets200ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListWidgets200ResponseInner from a JSON string
list_widgets200_response_inner_instance = ListWidgets200ResponseInner.from_json(json)
# print the JSON string representation of the object
print(ListWidgets200ResponseInner.to_json())

# convert the object into a dict
list_widgets200_response_inner_dict = list_widgets200_response_inner_instance.to_dict()
# create an instance of ListWidgets200ResponseInner from a dict
list_widgets200_response_inner_from_dict = ListWidgets200ResponseInner.from_dict(list_widgets200_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


