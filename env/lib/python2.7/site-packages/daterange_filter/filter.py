# -*- coding: utf-8 -*-


'''
Has the filter that allows to filter by a date range.

'''
import datetime
import django
from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_static import static
from django.conf import settings

use_suit = 'DATE_RANGE_FILTER_USE_WIDGET_SUIT'

if hasattr(settings, use_suit):
    DATE_RANGE_FILTER_USE_WIDGET_SUIT = getattr(settings, use_suit)
else:
    DATE_RANGE_FILTER_USE_WIDGET_SUIT = False

if DATE_RANGE_FILTER_USE_WIDGET_SUIT:
    try:
        from suit.widgets import SuitDateWidget as AdminDateWidget, SuitSplitDateTimeWidget as AdminSplitDateTime
    except ImportError:
        from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
else:
    from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

try:
    from django.utils.html import format_html
except ImportError:
    from django.utils.html import conditional_escape, mark_safe

    def format_html(format_string, *args, **kwargs):
        args_safe = map(conditional_escape, args)
        kwargs_safe = dict((k, conditional_escape(v)) for (k, v) in kwargs.items())
        return mark_safe(format_string.format(*args_safe, **kwargs_safe))


# Django doesn't deal well with filter params that look like queryset lookups.
FILTER_PREFIX = 'drf__'


def clean_input_prefix(input_):
    return dict((key.split(FILTER_PREFIX)[1] if key.startswith(FILTER_PREFIX) else key, val)
                for (key, val) in input_.items())


class DateRangeFilterAdminSplitDateTime(AdminSplitDateTime):
    def format_output(self, rendered_widgets):
        return format_html('<p>{0} {1}<br />{2} {3}</p>',
                           '', rendered_widgets[0],
                           '', rendered_widgets[1])


class DateRangeFilterBaseForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(DateRangeFilterBaseForm, self).__init__(*args, **kwargs)
        self.request = request

    @property
    def media(self):
        try:
            if getattr(self.request, 'daterange_filter_media_included'):
                return forms.Media()
        except AttributeError:
            setattr(self.request, 'daterange_filter_media_included', True)

            js = ["calendar.js", "admin/DateTimeShortcuts.js"]
            css = ['widgets.css']

            return forms.Media(
                js=[static("admin/js/%s" % path) for path in js],
                css={'all': [static("admin/css/%s" % path) for path in css]}
            )


class DateRangeForm(DateRangeFilterBaseForm):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s%s__gte' % (FILTER_PREFIX, field_name)] = forms.DateField(
            label='',
            widget=AdminDateWidget(
                attrs={'placeholder': _('From date')}
            ),
            localize=True,
            required=False
        )

        self.fields['%s%s__lte' % (FILTER_PREFIX, field_name)] = forms.DateField(
            label='',
            widget=AdminDateWidget(
                attrs={'placeholder': _('To date')}
            ),
            localize=True,
            required=False,
        )

    # Django 1.4 can't handle media inheritance well. We have to do it manually.
    if django.VERSION < (1, 5):
        @property
        def media(self):
            return super(DateRangeForm, self).media


class DateTimeRangeForm(DateRangeFilterBaseForm):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateTimeRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s%s__gte' % (FILTER_PREFIX, field_name)] = forms.DateTimeField(
            label='',
            widget=DateRangeFilterAdminSplitDateTime(
                attrs={'placeholder': _('From date')}
            ),
            localize=True,
            required=False
        )

        self.fields['%s%s__lte' % (FILTER_PREFIX, field_name)] = forms.DateTimeField(
            label='',
            widget=DateRangeFilterAdminSplitDateTime(
                attrs={'placeholder': _('To date')},
            ),
            localize=True,
            required=False
        )

    # Django 1.4 can't handle media inheritance well. We have to do it manually.
    if django.VERSION < (1, 5):
        @property
        def media(self):
            return super(DateTimeRangeForm, self).media


class DateRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s%s__gte' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_upto = '%s%s__lte' % (FILTER_PREFIX, field_path)
        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        """
        Pop the original parameters, and return the date filter & other filter
        parameters.
        """
        
        cl.params.pop(self.lookup_kwarg_since, None)
        cl.params.pop(self.lookup_kwarg_upto, None)
        return ({
            'get_query': cl.params,
        }, )

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return DateRangeForm(request, data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = clean_input_prefix(dict(filter(lambda x: bool(x[1]), self.form.cleaned_data.items())))

            # filter by upto included
            lookup_upto = self.lookup_kwarg_upto.lstrip(FILTER_PREFIX)
            if filter_params.get(lookup_upto) is not None:
                lookup_kwarg_upto_value = filter_params.pop(lookup_upto)
                filter_params['%s__lt' % self.field_path] = lookup_kwarg_upto_value + datetime.timedelta(days=1)

            return queryset.filter(**filter_params)
        else:
            return queryset


class DateTimeRangeFilter(admin.filters.FieldListFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since_0 = '%s%s__gte_0' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_since_1 = '%s%s__gte_1' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_upto_0 = '%s%s__lte_0' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_upto_1 = '%s%s__lte_1' % (FILTER_PREFIX, field_path)

        super(DateTimeRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since_0, self.lookup_kwarg_since_1, self.lookup_kwarg_upto_0, self.lookup_kwarg_upto_1]

    def get_form(self, request):
        return DateTimeRangeForm(request, data=self.used_parameters, field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = clean_input_prefix(dict(filter(lambda x: bool(x[1]), self.form.cleaned_data.items())))
            return queryset.filter(**filter_params)
        else:
            return queryset


# register the filters
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.DateField), DateRangeFilter)
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.DateTimeField), DateTimeRangeFilter)
