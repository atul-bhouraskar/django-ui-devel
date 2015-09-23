import json
import urllib

from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.defaulttags import URLNode
from django import forms

from . import discover
from . import mock

class FixtureForm(forms.Form):
    template = forms.CharField()
    fixture = forms.CharField()
    logged_in = forms.BooleanField(required=False)

    def __init__(self, fixtures, *args, **kwargs):
        super(FixtureForm, self).__init__(*args, **kwargs)
        self.fixtures = fixtures

        self.context = None

    def clean(self):
        cleaned_data = super(FixtureForm, self).clean()
        template = cleaned_data.get("template")
        fixture = cleaned_data.get("fixture")

        # check that the template is in fixtures
        try:
            template_entry = self.fixtures[template]
        except KeyError:
            raise forms.ValidationError("Invalid template name")

        #check that the fixture is in this template_entry
        try:
            self.context = template_entry[fixture]
        except KeyError:
            raise forms.ValidationError("Invalid fixture name")

        self.is_logged_in = cleaned_data.get('logged_in', False)

        return cleaned_data

def show_dashboard(request):
    """
    Shows the ui_devel dashboard with iframe that renders the selected template
    """

    # get the dictionary of template fixtures
    fixtures = discover.get_template_fixtures()

    form = FixtureForm(fixtures)

    fixtures_json = json.dumps(fixtures, cls=mock.UIMockEncoder)

    return render(request, "ui_devel/dashboard.html",
                  {'form': form,
                  'fixtures_json':fixtures_json})

class DevelContext(object):
    def __init__(self, request, context, is_authenticated):
        self.request = request
        self.context  = context
        self.is_authenticated = is_authenticated

    def __enter__(self):
        # overrride the url tag to return "" always
        self.old_render = URLNode.render
        def new_render(cls, context):
            """ Override existing url method to simply return ""
            """
            return ""
        URLNode.render = new_render

        # replace the request user with a mock user
        self.old_user = getattr(self.request, 'user', None)

        self.request.user = self.context.get('user')
        if self.request.user is None:
            self.request.user = mock.UIMock('User',
                                get_full_name='Full Name')

        self.request.user.is_authenticated = self.is_authenticated

    def __exit__(self, exc_type, exc_val, exc_tb):
        # revert request.user
        self.request.user = self.old_user
        # revert url tag functionality
        URLNode.render = self.old_render

def render_template(request):
    # get the dictionary of template fixtures
    fixtures = discover.get_template_fixtures()

    form = FixtureForm(fixtures, request.GET)
    if form.is_valid():
        # render the template
        context = form.context

        with DevelContext(request, context, form.is_logged_in):
            rendered = render_to_string(form.cleaned_data['template'],
                                        context,
                                        RequestContext(request))

        return HttpResponse(rendered)

    else:
        # TODO render default template
        pass