from django.shortcuts import render
import requests
from requests.compat import quote_plus
# from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from .import models
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
BASE_CRAIGSLIST_URL = 'https://{}.craigslist.org/search/?query={}'
    



# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    location = request.POST.get('location')
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(location.lower(), quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    content = {
        "search": search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', content)