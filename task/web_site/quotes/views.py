from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuoteForm, AuthorForm
from .models import Quote, Author
from django.contrib.auth.decorators import login_required
from .scraping import authors, quotes
from datetime import datetime
from collections import Counter


# Create your views here.
def main(request):
    quotes=Quote.objects.all()
    tags_all=[]

    for obj in quotes:
        tags=obj.tags
        tags_all.extend(tags)
    counter = Counter(tags_all)
    ten_tags_number=counter.most_common(10)
    ten_tags=[]
    for i in ten_tags_number:
        ten_tags.append(i[0])

    return render(request, 'quotes/index.html', {'quotes': quotes,'ten_tags':ten_tags})

def tag(request, tag):
    quotes_tag=Quote.objects.filter(tags__contains=tag)
    return render (request, 'quotes/tag.html', {"tag":tag, "quotes_tag":quotes_tag})

@login_required
def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        
        if form.is_valid():
            quote=form.save(commit=False)
            quote.tags=form.cleaned_data["tags"].strip().split(",")
            quote.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {'form': form})

    return render(request, 'quotes/quote.html', {'form': QuoteForm()})



@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})
    return render(request, 'quotes/author.html', {'form': AuthorForm()})

def author_detail(request, fullname):
    author = Author.objects.get(fullname=fullname)
    return render(request, 'quotes/author_detail.html', {"author": author} )

@login_required
def scrap(request):
    url = "http://quotes.toscrape.com"
    authors_json=authors(url)
    quotes_json=quotes(url)

    for author in authors_json:
        Author.objects.get_or_create(
            fullname=author["fullname"],
    defaults={
        "born_date":datetime.strptime(author['born_date'], '%B %d, %Y').date(),
        "born_location": author["born_location"],
        "description": author["description"],})

    for quote in quotes_json:
        try:
            Quote.objects.get_or_create(
        quote=quote["quote"],
        author=Author.objects.get(fullname=quote["author"]),
        defaults={"tags": quote["tags"],})
        except Author.DoesNotExist:
            Quote.objects.get_or_create(
        quote=quote["quote"],
        author=Author.objects.get(fullname="Alexandre Dumas-fils"),
        defaults={"tags": quote["tags"],})

    return redirect(to='quotes:main')

