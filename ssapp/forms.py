from django import forms
from .models import Details, Course


class DateInput(forms.DateInput):
    input_type = 'date'


class DetailsForm(forms.ModelForm):
    genders = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    gender = forms.ChoiceField(choices=genders, widget=forms.RadioSelect)
    purposes = (('Enquiry', 'Enquiry'), ('Place Order', 'Place Order'), ('Return', 'Return'))
    purpose = forms.ChoiceField(choices=purposes, widget=forms.RadioSelect)
    material = (('Debit Note Book', 'Debit Note Book'), ('Pen', 'Pen'), ('Exam Papers', 'Exam Papers'))
    materials = forms.ChoiceField(choices=material, widget=forms.RadioSelect)
    date_of_birth = forms.DateField(widget=DateInput(attrs={'onchange': "calculateAge()"}))

    class Meta:
        model = Details
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department_id=department_id).order_by('course')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.department.course_set.order_by('course')
