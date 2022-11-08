from django import forms
from .models import Assignment, Submissions


# ASSIGNMENT CREATE FORM
class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'file', 'marks', 'due_date', 'exclude_urls']

    def __init__(self, *args, **kwargs):
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Title"
        self.fields['content'].label = "Content"
        self.fields['marks'].label = "Marks"
        self.fields['file'].label = "Upload file"
        self.fields['due_date'].label = "Due Date"

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        if valid:
            return valid
        return valid

    def save(self, commit=True):
        assignment = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            assignment.save()
        return assignment


# ASSIGNMENT UPDATE FORM
class AssignmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['marks', 'due_date', 'exclude_urls']

    def __init__(self, *args, **kwargs):
        super(AssignmentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['marks'].label = "Marks"
        self.fields['due_date'].label = "Due Date"
        self.fields['exclude_urls'].label = "Exclude URL's"
        self.fields['exclude_urls'].description = "Add one URL on each line"

    def is_valid(self):
        valid = super(AssignmentUpdateForm, self).is_valid()

        if valid:
            return valid
        return valid

    def save(self, commit=True):
        assignment = super(AssignmentUpdateForm, self).save(commit=False)
        if commit:
            assignment.save()
        return assignment


# ASSIGNMENT SUBMISSION FORM
class AssignmentSubmitForm(forms.ModelForm):
    class Meta:
        model = Submissions
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmitForm, self).__init__(*args, **kwargs)
        
        self.fields['file'].label = "Upload File" 

    def is_valid(self):
        valid = super(AssignmentSubmitForm, self).is_valid()

        if valid:
            return valid
        return valid

    def save(self, commit=True):
        submission = super(AssignmentSubmitForm, self).save(commit=False)
        if commit:
            submission.assignment = Assignment.objects.get( id=1 )
            submission.save()
        return submission
