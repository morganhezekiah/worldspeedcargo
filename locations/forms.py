from random import choices
from django import forms




status = [
        ('In Transit', 'In Transit'),
        ('On Hold', 'On Hold'),
        ('Out Of Delivery', 'Out Of Delivery'),
        ('Picked Up', 'Picked Up'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
      ]
class AddLocationForm(forms.Form):
    location = forms.CharField(
        label="Location",
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"eg. Dubai"}),
    )

    
    status = forms.ChoiceField(
        label='Status', 
        widget=forms.Select(attrs={"class":"form-select"}),
         choices=status
         )

    remark = forms.CharField(
        label="Remark",
        widget=forms.Textarea(attrs={"class":"form-control","placeholder":"(optional)"})
    )
