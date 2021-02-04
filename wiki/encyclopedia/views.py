from django.shortcuts import render, redirect

from . import util
import random
import markdown2 as md


def index(request):
    if request.method == "POST":
        # get search query value
        query = request.POST['q']
        # see if there is an entry based on the query(title)
        entry = util.get_entry(query)
        # empty list initialised
        search_list = []
        if not entry:
            # get list of all existing entries
            entry_list = util.list_entries()
            # iterate that list
            for item in entry_list:
                # if query is found as a substring in an item - append that item to search_list
                # this does NOT check for each character if lower or upper case so User needs to try both upper
                # and/or lower case if the phrase is not found
                if query in item:
                    # append that item to search list
                    search_list.append(item)
            # if search list is returned empty, return view with error message
            if len(search_list) == 0:
                return render(request, "encyclopedia/title_error.html", {
                    "title": query
                })
            # else return template with search list
            return render(request, "encyclopedia/subquery_search_result.html", {
                "search_list": search_list
            })
        else:
            # if query matches, redirect user to that entry page
            return redirect("wiki", title=query)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def wiki_entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/title_error.html", {
            "title": title
        })
    # convert Markdown into HTML before loading
    html = md.markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": html,
        "title": title
    })


def create_new_page(request):
    if request.method == "POST":
        title = request.POST['page_title']
        content = request.POST['page_text']

        # check if entry exist
        result = util.get_entry(title)
        if result:
            return render(request, "encyclopedia/page_exist_error.html", {
                "title": title
            })
        # otherwise save entry
        util.save_entry(title, content)

        # redirect user to newly created page
        return redirect('wiki', title=title)
    else:
        return render(request, "encyclopedia/new_page.html")


def random_page(request):
    # get entry list
    entries_list = util.list_entries()
    title = random.choice(entries_list)

    # redirect user to random the entry page
    return redirect('wiki', title=title)


def edit_entry(request, title):
    if request.method == "POST":
        content = request.POST['page_text']

        # save the edited entry
        util.save_entry(title, content)

        # redirect user back to the entry page
        return redirect('wiki', title=title)

        # populate page on load with current entry data
    else:
        # find entry data based on the title
        entry = util.get_entry(title)
        # load entry and title with html to populate form fields
        return render(request, "encyclopedia/edit_entry.html", {
            "entry": entry,
            "title": title
        })
