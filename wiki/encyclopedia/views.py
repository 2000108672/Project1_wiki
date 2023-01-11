from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from random import randint



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title.strip())
    isNotFound = False
    if not content:
        isNotFound = True
        content = None
    else:
        content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title, 'isNotFound': isNotFound})



def search_entry(request):
    search_term = request.GET.get('q').strip()
    if search_term in util.list_entries():
        return redirect("entry", title=search_term)
    return render(request, "encyclopedia/search.html", {"entries": util.search_entries(search_term), "q": search_term})


def random_entry(request):
    entry_titles = util.list_entries()
    allRandom = entry_titles[randint(0, len(entry_titles)-1)]
    return redirect("entry", title=allRandom)



def create_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {"message": "It is not possible to save an entry with an empty title or content. Please provide both and try again.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "A page with this title already exists. Please try a different title.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/add.html")



def edit_entry(request, title):
    content = util.get_entry(title.strip())

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Cannot save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})
