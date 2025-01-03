from universities.models import University
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def bookmark(request, id):

    university = get_object_or_404(University, id=id)
    if university.bookmarks.filter(id=request.user.id).exists():
        university.bookmarks.remove(request.user)
        messages.add_message(
            request, messages.INFO, f'{university.name} removed from your bookmark.')
    else:
        university.bookmarks.add(request.user)
        messages.add_message(
            request, messages.SUCCESS, f'{university.name} added to your bookmark.')

    return redirect(request.META['HTTP_REFERER'])


def bookmarks_page(request):

    title = 'Bookmarks'

    search_query = request.GET.get('search', '')
    user = request.user

    if search_query:
        data = user.bookmarks.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)).distinct()
        title = f'Search results for {search_query}'
        temp_data = list(reversed(data))
    else:
        data = user.bookmarks.all()
        temp_data = list(reversed(data))

    paginator = Paginator(temp_data, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    bookmarked_unis = user.bookmarks.all()

    context = {
        'title': title,
        'universities': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'bookmarked_unis': bookmarked_unis,
        'data': data,
    }
    return render(request, 'bookmarks/bookmarks.html', context)
