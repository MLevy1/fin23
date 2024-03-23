from django.contrib import admin

from .models import (
    Tax_Return,
    Tax_Return_Form,
    Tax_Return_Form_Line,
    Tax_Return_Form_Line_Input,
    InputValue,
    DataSource,
)

# Register your models here.
admin.site.register(Tax_Return)
admin.site.register(Tax_Return_Form)
admin.site.register(Tax_Return_Form_Line)
admin.site.register(Tax_Return_Form_Line_Input)
admin.site.register(InputValue)
admin.site.register(DataSource)