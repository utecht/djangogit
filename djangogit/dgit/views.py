# Create your views here.
import os
import stat

from django.shortcuts import render_to_response, Http404, HttpResponse
from dulwich.repo import Repo, Tree, NotGitRepository, NotTreeError

import settings

# some helper functions
def getFiles(tree, repo):
    """get a pretty list of files from a tree"""
    
    #build the list of files
    files = []
    for e in tree.entries():
        mode, path, sha = e
        
        if mode & stat.S_IFDIR:
            kind = "tree"
        else:
            kind = "blob"
        
        #mode = oct(mode) #make it human-readable
    
        obj = repo.get_object(sha)
        size = 0
        if kind == 'blob':
            size = obj.raw_length()
    
        files.append((mode, path, sha, kind, size))
        
    return files

def getBranch(request):
    """get the branch name from GET, or return master"""
    
    # TODO: This could also check that the
    #       given branch is a real branch
    #       Would require passing repo as well.
    
    if 'b' in request.GET:
        branch = request.GET['b']
    else:
        branch = 'master'
        
    return branch

def getBranches(repo):
    # get the branches
    refs = []
    for r in list(repo.refs.keys()):
        pos = r.rfind('/')
        if pos != -1 and 'remotes' not in r:
            refs.append(r[pos + 1:])
    return refs

# the actual views
def index(request):
    """display the list of available git projects"""
    
    files = os.listdir(settings.REPOS_DIR)
    
    return render_to_response("index.html",
                              dict(name="World",
                                   files=files))
    
def commits(request, repo_name, sha='master'):
    """display the commit history for the given sha/branch"""
    
    # attempt to open the repo, this may fail
    try:
        repo = Repo(os.path.join(settings.REPOS_DIR, repo_name))
    except NotGitRepository:
        raise Http404
            
    # was the supplied sha really a ref?
    sha_ref = 'refs/heads/' + sha  
    if sha_ref in repo.refs:
        sha = repo.refs[sha_ref]

    try:
        commit = repo.commit(sha)
    except:
        raise Http404
    
    refs = getBranches(repo)
    
    tree = repo.tree(commit.tree)
    
    files = getFiles(tree, repo)
    
    hist = repo.revision_history(commit.id)
    
    return render_to_response("commits.html",
                              dict(name=repo_name,
                                   files=files,
                                   refs=refs,
                                   commits=hist))

def tree(request, repo_name, sha='master'):
    try:
        repo = Repo(os.path.join(settings.REPOS_DIR, repo_name))
    except NotGitRepository:
        raise Http404
    
    # was the supplied sha really a ref?
    sha_ref = 'refs/heads/' + sha 
    if sha_ref in repo.refs:
        sha = repo.refs[sha_ref]

    try:
        commit = repo.commit(sha)
    except:
        raise Http404
    
    # get the branches
    refs = getBranches(repo)
    
    tree = repo.tree(commit.tree)
    files = getFiles(tree, repo)

    parents = map(repo.get_object, commit.parents)

    return render_to_response("commit.html",
                              dict(name=repo_name,
                                   commit=commit,
                                   tree=tree,
                                   files=files,
                                   branches=refs,
                                   parents=parents))

def filetree(request, repo_name, sha, path=''):
    try:
        repo = Repo(os.path.join(settings.REPOS_DIR, repo_name))
    except NotGitRepository:
        raise Http404
    
    # this may be needed, depnding on how we do branches
    #branch = getBranch(request)
    
    # check to see if a specific commit has been passed
    # if not, then assume head

    sha_ref = 'refs/heads/' + sha 
    if sha_ref in repo.refs:
        sha = repo.refs[sha_ref]
       
    #raise Exception('%s - %s' % (sha, path))
    commit = repo.commit(sha)
    
    tree = repo.tree(commit.tree)
    
    # Lookup the path; may be a tree or a blob
    obj = tree.lookup_path(repo.get_object, path)[1]
    
    try: 
        # assume it's a tree
        new_tree = repo.tree(obj)
    except NotTreeError:
        # well maybe it was a file (blob)
        return file_(request, repo_name, repo, sha=obj, path=path)
        
    files = getFiles(new_tree, repo)
    
    return render_to_response("tree.html",
                              dict(name=repo_name,
                                   files=files,
                                   branch='master',
                                   path=path))

def file_(request, repo_name, repo, sha, path):

    try:
        blob = repo.get_blob(sha)
    except:
        raise Http404
    
    filename = path
    
    dotpos = filename.rfind('.')
    if dotpos != -1:
        ext = filename[dotpos+1:]
    else:
        ext = 'text'
    
    return render_to_response("file.html",
                              dict(name=repo_name,
                                   blob=blob,
                                   filename=filename,
                                   ext=ext))
