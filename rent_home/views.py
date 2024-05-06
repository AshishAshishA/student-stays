from django.shortcuts import render, redirect, get_object_or_404
from rent_home.models import Room, RoomType, House, Property_Type, Budget_Range, Area
from .filters import RoomFilter
from .forms import HouseForm, RoomForm

from django.urls import reverse,reverse_lazy

from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from allauth.account import views as auth_views

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib import messages


class RoomIndexView(ListView):
    models = Room
    template_name = 'rent_home/room_index.html'
    queryset=Room.objects.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Room.objects.all()
        # print('filter',self.request.GET)

        context['filter_done']=None
        if self.request.GET:
            context['filter_done']=True

        context['rooms'] = RoomFilter(self.request.GET, queryset=queryset)


        return context

room_index = RoomIndexView.as_view()


class HouseDetailView(DetailView):
    model = House
    template_name='rent_home/house_detail.html'
    context_object_name = 'house'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        rooms=context['rooms'] = Room.objects.filter(house=self.kwargs.get('pk'))

        return context

house_detail = HouseDetailView.as_view()


class HouseListView(LoginRequiredMixin, ListView):
    raise_exception=False
    login_url='login'
    redirect_field_name='next'

    model = House
    template_name = 'rent_home/house_list.html'
    context_object_name = 'houses'

    def get_context_data(self):
        context = super().get_context_data()

        context['houses'] = context['houses'].filter(user=self.request.user)

        return context

house_list = HouseListView.as_view()

class RoomDetailView(DetailView):
    model = Room
    template_name='rent_home/room_details.html'
    context_object_name = 'room'

room_details = RoomDetailView.as_view()

class AddHouseView(LoginRequiredMixin, CreateView):
    raise_exception = False
    login_url = 'login'
    redirect_field_name = 'next'

    model = House
    form_class = HouseForm
    template_name = 'rent_home/add_house.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated: # and self.request.user.has_perm('Post.add_post'):
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            # If user is not authenticated or does not have required permissions
            return self.handle_no_permission()

    def get_success_url(self):
        return reverse_lazy('house-detail', kwargs={'pk':self.object.pk})

add_house = AddHouseView.as_view()

class AddRoomView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rent_home/add_room.html'

    def form_valid(self,form):
        house = get_object_or_404(House, pk=self.kwargs.get('pk'))
        form.instance.house = house
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('house-detail', kwargs={'pk':self.object.house.pk})

add_room = AddRoomView.as_view()

class HouseUpdateView(UpdateView):
    model = House
    template_name = 'rent_home/add_house.html'
    form_class = HouseForm

    def get_success_url(self):
        return reverse_lazy('house-detail', kwargs={'pk':self.kwargs.get('pk')})

house_update = HouseUpdateView.as_view()

class RoomUpdateView(LoginRequiredMixin,UpdateView):
    raise_exception = False
    login_url = 'login'
    redirect_field_name = 'next'

    model = Room
    template_name = 'rent_home/add_room.html'
    form_class = RoomForm

    def get_success_url(self):
        return reverse_lazy('room-details', kwargs={'pk':self.kwargs.get('pk')})

room_update = RoomUpdateView.as_view()

#allauth authentication

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        print(self.request.POST)

        if next_url:
            return next_url
        else:
            return reverse_lazy('room-index')

allauth_login = CustomLoginView.as_view()

class CustomSignUpView(auth_views.SignupView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')

        if next_url == None:
            next_url = self.request.POST.get('next')

        if next_url:
            return next_url
        else:
            return reverse_lazy('room-index')

allauth_signup = CustomSignUpView.as_view()

class PrivacyPolicyView(TemplateView):
    template_name = 'rent_home/privacy_policy.html'

privacy_policy_view = PrivacyPolicyView.as_view()
