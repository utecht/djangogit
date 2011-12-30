import stat
import os
import cStringIO

import dulwich.patch

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

def getRepo(repo_name):
    try:
        repo = Repo(os.path.join(settings.REPOS_DIR, repo_name))
    except NotGitRepository:
        raise Http404
    
    return repo

def get_tree_diff(store, old_tree, new_tree):
    diff = []
    changes = store.tree_changes(old_tree, new_tree)

    for (oldpath, newpath), (oldmode, newmode), (oldsha, newsha) in changes:
        output = cStringIO.StringIO()
        dulwich.patch.write_object_diff(output, store, (oldpath, oldmode, oldsha),
                                    (newpath, newmode, newsha))
        
        diff.append(("{} -> {}".format(oldpath, newpath), output.getvalue()))

    return diff 