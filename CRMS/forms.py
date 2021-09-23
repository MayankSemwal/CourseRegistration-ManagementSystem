# from django import forms
# from CRMS.models import Order
#
#
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('student', 'course', 'levels', 'order_date')
#         widgets = {'student': forms.RadioSelect(attrs={'class': 'radio'}),
#                    'order_date': forms.SelectDateWidget(attrs={'class': 'years=date.today()'})}
#         labels = {'student': "Student Name", 'order_date': "Order Date"}
#
#     # student = forms.RadioSelect()
#     # course = forms.MultipleChoiceField(label='course', max_length=100)  # Supports ManyToManyField
#     # levels = forms.IntegerField(label='levels', max_length=10)  # Supports upto level 10
#     # order_date = forms.SelectDateWidget()
#
#
# class InterestForm(forms.Form):
#     interestedChoices = (('1', 'Yes'), ('0', 'No'))
#     interested = forms.CharField(widget=forms.RadioSelect(choices=interestedChoices))
#     levels = forms.IntegerField(initial=1)
#     comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')

from django import forms
from CRMS.models import Order, Review, Student


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Student Name",
    )
    length = forms.TypedChoiceField(
        widget=forms.RadioSelect,
        choices=LENGTH_CHOICES,
        coerce=int,
        label="Preferred course duration:",
        required=False
    )
    max_price = forms.IntegerField(
        required=True,
        label="Maximum Price",
        min_value=0,
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']  # changed from book to course
        widgets = {'book': forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating': u'Rating: An integer between 1 (worst) and 5 (best)', }


# Project : 4
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name', 'address', 'email', 'interested_in']
        widgets = {'interested_in': forms.CheckboxSelectMultiple, 'password': forms.PasswordInput,
                   'email': forms.EmailInput}
        labels = {'interested_in': u'Select the interested topics', 'email': u'E-mail'}
        help_texts = {
            'username': None,
        }
