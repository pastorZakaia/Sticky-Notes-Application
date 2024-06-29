from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


# Create your views here.
def post_list(request):
    # View to display a list of all posts.
    #:param request: HTTP request object.
    # :return: Rendered template with a list of posts.

    posts = Post.objects.all()
    # Creating a context dictionary to pass data
    context = {
        'posts': posts,
        'page_title': 'List of Posts',
}
    return render(request, 'posts/post_list.html', context)

def post_detail(request, pk):

# View to display details of a specific post.   
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_create(request):
    """
    View to create a new post.
    :param request: HTTP request object.
    :return: Rendered template for creating a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

def post_update(request, pk):
    """
    View to update an existing post.
    :param request: HTTP request object.
    :param pk: Primary key of the post to be updated.
    :return: Rendered template for updating the specified post.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})


def post_delete(request, pk):
    """
    View to delete an existing post.
    :param request: HTTP request object.
    :param pk: Primary key of the post to be deleted.
    :return: Redirect to the post list after deletion.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def add_line_breaks(content, interval=15):
    """
    Utility function to add line breaks on individual sticky notes.
    """
    return '\n'.join(
        [content[i:i+interval] for i in range(0, len(content), interval)])

