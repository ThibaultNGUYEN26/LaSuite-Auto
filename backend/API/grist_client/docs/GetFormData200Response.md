# GetFormData200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**form_fields_by_id** | **object** | Form fields indexed by field ID | [optional] 
**form_layout_spec** | **str** | JSON layout specification for the form | [optional] 
**form_table_id** | **str** | ID of the table the form submits to | [optional] 
**form_title** | **str** | Title of the form | [optional] 

## Example

```python
from grist_client.models.get_form_data200_response import GetFormData200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetFormData200Response from a JSON string
get_form_data200_response_instance = GetFormData200Response.from_json(json)
# print the JSON string representation of the object
print(GetFormData200Response.to_json())

# convert the object into a dict
get_form_data200_response_dict = get_form_data200_response_instance.to_dict()
# create an instance of GetFormData200Response from a dict
get_form_data200_response_from_dict = GetFormData200Response.from_dict(get_form_data200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


