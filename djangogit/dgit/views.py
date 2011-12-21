# Create your views here.
import os

from django.shortcuts import render_to_response, Http404, HttpResponse
from dulwich.repo import Repo, Tree, NotGitRepository

import settings


def index(request):
    """display the list of available git projects"""
    
    files = os.listdir(settings.REPOS_DIR)
    
    return render_to_response("index.html",
                              dict(name="World",
                                   files=files))
    
    
def repo(request, repo_name, ref):
    """main page for a single repo"""
    
    # attempt to open the repo, this may fail
    try:
        repo = Repo(os.path.join(settings.REPOS_DIR, repo_name))
    except NotGitRepository:
        raise Http404
    
    if ref != 'HEAD':
        ref = 'refs/heads/' + ref
    head = repo.refs[ref]
    
    
    refs = []
    for r in list(repo.refs.keys()):
        pos = r.rfind('/')
        if pos != -1:
            refs.append(r[pos + 1:])
    
    commit = repo.commit(head)
    tree = repo.tree(commit.tree)
    
    hist = repo.revision_history(head)[:5]
    
    return render_to_response("repo.html",
                              dict(name=repo_name,
                                   files=tree.entries(),
                                   refs=refs,
                                   commits=hist))
    
    
def file_(request, repo_name, sha):
    return HttpResponse("You requested file: {}".format(sha))

def commit(request, repo_name, sha):
    return HttpResponse("You requested commit: {}".format(sha))