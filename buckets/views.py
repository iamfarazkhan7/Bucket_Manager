# File: buckets/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from .models import Bucket
from .forms import BucketForm


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require staff status"""
    def test_func(self):
        return self.request.user.is_staff


class BucketListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Bucket
    template_name = 'buckets/list.html'
    context_object_name = 'buckets'
    paginate_by = 10

    def get_queryset(self):
        return Bucket.objects.filter(owner=self.request.user)


class BucketCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Bucket
    form_class = BucketForm
    template_name = 'buckets/form.html'
    success_url = reverse_lazy('buckets:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Bucket "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Bucket'
        context['submit_text'] = 'Create Bucket'
        return context


class BucketUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Bucket
    form_class = BucketForm
    template_name = 'buckets/form.html'
    success_url = reverse_lazy('buckets:list')

    def get_queryset(self):
        return Bucket.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f'Bucket "{form.instance.name}" updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Bucket'
        context['submit_text'] = 'Update Bucket'
        return context


class BucketDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Bucket
    template_name = 'buckets/confirm_delete.html'
    success_url = reverse_lazy('buckets:list')

    def get_queryset(self):
        return Bucket.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        bucket = self.get_object()
        messages.success(request, f'Bucket "{bucket.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)