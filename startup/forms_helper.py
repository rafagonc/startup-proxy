from django.shortcuts import render
from rest_framework.response import Response

from django.forms import (CharField, TextInput, Textarea, IntegerField,
                          FloatField, DecimalField, EmailField, URLField,
                          FileField, BooleanField, DateField, DateTimeField,
                          ModelChoiceField, ChoiceField, ImageField, TimeField,
                          ModelMultipleChoiceField)


def form_get_view(request, pk, model_class, form_class, title, submit="Save"):
    if pk:
        model = model_class.objects.get(pk=pk).to_dict()
    else:
        model = {}
    return render(
        request, "forms.html", {
            "title": title,
            'submit': submit,
            **split_form_fields_into_types(form_class(initial=model)),
        })


def form_post_success(success_message,
                      request,
                      form_class,
                      instance,
                      title,
                      submit="Save"):
    return render(
        request, "forms.html", {
            "response": {
                "success": True,
                "message": success_message
            },
            "title": title,
            'submit': submit,
            **split_form_fields_into_types(form_class(initial=instance)),
        })


def form_post_error(error, request, pk, model_class, form_class, title):
    if pk:
        model = model_class.objects.get(pk=pk).to_dict()
    else:
        model = {}
    return render(
        request, "forms.html", {
            **split_form_fields_into_types(form_class(initial=model)),
            'submit': "Save",
            "title": title,
            "response": {
                "success": False,
                "message": error
            },
        })


def merge_items_in_array(n=3, i=[]):
    l = len(i)
    for ndx in range(0, l, n):
        yield i[ndx:min(ndx + n, l)]


def join_form_field_by_types(form, merge_factor, classes, notin=False):
    if notin:
        return merge_items_in_array(merge_factor, [
            field for field in form if field.field.__class__.__name__ not in
            [cl.__name__ for cl in classes]
        ])
    else:
        return merge_items_in_array(merge_factor, [
            field for field in form if field.field.__class__.__name__ in
            [cl.__name__ for cl in classes]
        ])


def split_form_fields_into_types(form):
    text_input_fields = join_form_field_by_types(form, 3, (
        CharField,
        IntegerField,
        FloatField,
        DecimalField,
        EmailField,
        URLField,
    ))
    textarea_input_fields = join_form_field_by_types(form, 3,
                                                     (Textarea, TextInput))
    date_input_fields = join_form_field_by_types(form, 3,
                                                 [DateField, DateTimeField])
    model_choice_fields = join_form_field_by_types(
        form, 3, [ModelChoiceField, ModelMultipleChoiceField, ChoiceField])
    extra_input_fields = join_form_field_by_types(
        form,
        3, (CharField, TextInput, TimeField, Textarea, IntegerField,
            FloatField, DecimalField, EmailField, URLField, FileField,
            BooleanField, ModelChoiceField, ChoiceField, DateField,
            DateTimeField, ModelMultipleChoiceField),
        notin=True)

    file_input_fields = join_form_field_by_types(form, 5,
                                                 [FileField, ImageField])
    checkbox_input_fields = join_form_field_by_types(form, 5, [BooleanField])
    return {
        "text_input_fields": text_input_fields,
        "textarea_input_fields": textarea_input_fields,
        "extra_input_fields": extra_input_fields,
        "file_input_fields": file_input_fields,
        "checkbox_input_fields": checkbox_input_fields,
        "date_input_fields": date_input_fields,
        "model_choice_fields": model_choice_fields
    }
