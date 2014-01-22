import json
import urllib

from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template.defaulttags import URLNode
from django import forms

from . import discover
from . import mock

class FixtureForm(forms.Form):
    template = forms.CharField()
    fixture = forms.CharField()

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
        return cleaned_data

def show_dashboard(request):
    """
    Shows the ui_devel dashboard with iframe that renders the selected template
    """

    # get the dictionary of template fixtures
    fixtures = discover.get_template_fixtures()

    form = FixtureForm(fixtures)

    return render_to_response("ui_devel/dashboard.html",
                              {'form': form,
                               'fixtures_json': json.dumps(fixtures,
                                                 cls=mock.UIMockEncoder)},
                              RequestContext(request))


def render_template(request):
    # get the dictionary of template fixtures
    fixtures = discover.get_template_fixtures()

    form = FixtureForm(fixtures, request.GET)
    if form.is_valid():
        # render the template
        context = form.context
        # overrride the url tag to return "" always
        old_render = URLNode.render
        def new_render(cls, context):
            """ Override existing url method to simply return ""
            """
            return ""
        URLNode.render = new_render
        rendered = render_to_string(form.cleaned_data['template'],
                                  context,
                                  RequestContext(request))
        # revert url tag functionality
        URLNode.render = old_render

        return HttpResponse(rendered)

    else:
        # render default template
        print form.errors
        pass