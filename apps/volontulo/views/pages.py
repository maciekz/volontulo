# -*- coding: utf-8 -*-

"""
.. module:: pages
"""

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from apps.volontulo.models import Page
from apps.volontulo.utils import is_admin_test


class PageList(ListView):  # pylint: disable=too-many-ancestors
    """View listing static pages."""
    model = Page
    template_name = 'pages/page_list.html'

    @method_decorator(user_passes_test(is_admin_test))
    def dispatch(self, *args, **kwargs):
        """
        Method is overriden to check that current user instance
        is administrator.
        """
        # pylint: disable=no-member
        return super(PageList, self).dispatch(*args, **kwargs)


class PageDetails(DetailView):  # pylint: disable=too-many-ancestors
    """View with details of static page."""
    model = Page
    template_name = 'pages/page_detail.html'


class PageCreate(CreateView):  # pylint: disable=too-many-ancestors
    """View responsible for creation of new static page."""
    model = Page
    fields = (
        'title',
        'content',
        'published',
    )
    template_name = 'pages/page_edit_form.html'
    success_url = reverse_lazy('pages_list')

    def form_valid(self, form):
        # pylint: disable=attribute-defined-outside-init
        self.object = form.save(commit=False)
        self.object.author = self.request.user.userprofile
        self.object.save()
        return redirect(self.get_success_url())

    @method_decorator(user_passes_test(is_admin_test))
    def dispatch(self, *args, **kwargs):
        """
        Method is overriden to check that current user instance
        is administrator.
        """
        # pylint: disable=no-member
        return super(PageCreate, self).dispatch(*args, **kwargs)


class PageEdit(UpdateView):  # pylint: disable=too-many-ancestors
    """View responsible for editing static page."""
    model = Page
    fields = (
        'title',
        'content',
        'published',
    )
    template_name = 'pages/page_edit_form.html'
    success_url = reverse_lazy('pages_list')

    @method_decorator(user_passes_test(is_admin_test))
    def dispatch(self, *args, **kwargs):
        """
        Method is overriden to check that current user instance
        is administrator.
        """
        # pylint: disable=no-member
        return super(PageEdit, self).dispatch(*args, **kwargs)


class PageDelete(DeleteView):  # pylint: disable=too-many-ancestors
    """Page responsible for deletion of static page."""
    model = Page
    success_url = reverse_lazy('pages_list')

    def get(self, request, *args, **kwargs):
        """
        method overrides default get method to allow deletion
        without confirmation
        """
        return self.post(request, *args, **kwargs)

    @method_decorator(user_passes_test(is_admin_test))
    def dispatch(self, *args, **kwargs):
        """
        Method is overriden to check that current user instance
        is administrator.
        """
        # pylint: disable=no-member
        return super(PageDelete, self).dispatch(*args, **kwargs)
