# from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField, PasswordField
# from wtforms.fields.html5 import EmailField


# class CreateUserForm(Form):
#     firstName = StringField('First Name', [validators.Length(min=1,
#                                                              max=150), validators.DataRequired()])
#     lastName = StringField('Last Name', [validators.Length(min=1,
#                                                            max=150), validators.DataRequired()])
#     email = EmailField('Email address', [validators.DataRequired(), validators.Email])

#     DateofBirth = DateField('Date of Birth', validators=[validators.DataRequired()], format="%d/%m/%Y",
#                             render_kw={"placeholder": "dd/mm/yyyy"})

#     gender = SelectField('Gender', [validators.DataRequired()],
#                          choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
#                          default='')
#     remarks = TextAreaField('Remarks', [validators.Optional()])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirmpassword', message='Passwords must match')])
#     confirmpassword = PasswordField('Confirm Password')
#     Username = StringField('Username', [validators.length(min=1, max=30), validators.data_required])

#     def validate(self):
#         pass

# class loginform(Form):
#     username=StringField('',[validators.length(min=1,max=30),validators.input_required()],render_kw={"placeholder": "Username"})
#     password = PasswordField('', [validators.DataRequired()],render_kw={"placeholder": "Password"})

#     def validate(self):
#         pass







