from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from .models import Post
from user.models import UserModel
from django.urls import reverse
from tweet.models import Post


def home(request):
    user = request.user.is_authenticated
    if user:
        all_post = Post.objects.all().order_by('-create_at')
        return render(request, 'tweet/home.html', {'all_post': all_post})
    else:
        return redirect('/sign-in')

# 게시글 작성 ,login_required를 사용하는대신, 사용자를 로그인 페이지로 이동시킨다.


def create_post(request):
    # 접근한 사용자가 로그인한 유저가 아니라면 로그인 페이지로 이동한다.
    user = request.user.is_authenticated
    if not user:
        return redirect(reverse('sign-in'))
    # GET : 글 작성 페이지 이동

    if request.method == 'GET':
        return render(request, 'tweet/create_post.html')

    # 데이터 수집 및 저장
    elif request.method == 'POST':
        url = request.POST.get('url', '')
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')
        owner = auth.get_user(request).user_id
        # 접근한 유저가 UserModel에 등록된 사용자가 아닐경우 방지
        try:
            owner = UserModel.objects.get(user_id=owner)
        except UserModel.DoesNotExist:
            return redirect('/')

        # 데이터 검사
        if not all([url, title, comment]):
            return render(request, 'tweet/create_post.html', {'error': '빈칸 없이 입력해주세요.'})
        # 게시글 저장,
        new_post = Post.objects.create(
            owner=owner, url=url, title=title, comment=comment)

        # 게시글 저장후, 상세페이지로 이동
        return render(request, 'tweet/create_post.html')
        # return redirect(reverse('상세페이지'))

# 게시글 수정


def set_post(request, post_id):
    # 탐색하는 게시글이 없을 경우 방지
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')
    # 작성자와,접근자 아이디가 불일치 할경우
    user = auth.get_user(request)
    if post.owner.user_id != user.user_id:
        return redirect('/')

    # GET일경우 기존 작성된 내용을 참고하여 데이터 출력
    if request.method == 'GET':
        return render(request, 'tweet/set_post.html', {'post': post})

    # POST의경우 전달된 데이터를 토대로 게시글 수정
    elif request.method == 'POST':
        post.url = request.POST.get('url', '')
        post.title = request.POST.get('title', '')
        post.comment = request.POST.get('comment', '')
        post.save()
        post = Post.objects.filter(post_id=post_id)

        # return redirect(reverse('상세페이지'))
        # return render(request, '상세페이지.html', {'post': post})


# 게시글 삭제
# @login_required() 현재 유저와, owner의 id값을 비교하는 분기문이 있으므로 사용할 필요가 없으리라 기대한다.
def delete_post(request, post_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        # 선택한 post_id의 id값을 읽어온다, 이미 삭제됬을 경우를 방지하여 try except를 사용한다.
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return redirect('/')

        # 현재 접근한 유저와, 소유자의  id와 같은지 판별하고 데이터를 삭제한다.
        user = auth.get_user(request)
        if user.user_id != post.owner.user_id:
            post.delete()

        return redirect('/')
        # return redirect(reverse('상세페이지'))


def my_page(request, user_id):
    # get일때, 유저 정보와 게시글들을 불러옴
    if request.method == "GET":
        # id로 선택한 유저의 정보를 가져옴
        click_user = UserModel.objects.get(user_id=user_id)
        # 유저 id가 post의 owner(fk)인 post를 가져와서
        # test = Post.objects.all()
        # print(test[0].title)
        print(click_user)
        post = Post.objects.filter(owner=click_user).order_by('create_at')
        context = {
            'click_user': click_user,
            'posts': post,
        }
        return render(request, 'tweet/my_page.html', context)


def set_profile(request,user_id):
    # 요청한 유저 id 와 프로필 페이지 유저 id가 다르면 자신의 프로필 수정으로 이동?

    # 메소드가 post일때, 유저네임, 프로필 사진, 프로필 메시지를 폼으로 받아온다.
    # 그리고 갱신하고 저장.
    if request.method == "POST":
        # user = UserModel.objects.get(user_id=user_id)
        # 여기 유저 검증 어떻게 해야하지?
        user = request.user

        user.username = request.POST.get('username', '')
        user.image = request.POST.get('image', '')
        user.description = request.POST.get('description', '')
        user.save()

        post = Post.objects.filter(owner=user).order_by('create_at')
        context = {
            'click_user': user,
            'posts': post,
        }
        return render(request, 'tweet/my_page.html', context)

    # get일때는, 유저 정보를 id로 받아와서, 수정창에 입력 돼 있게 하기.
    elif request.method == "GET":
        user = UserModel.objects.get(user_id=request.user.user_id)
        return render(request, 'tweet/set_profile.html', {'user': user})


def post_detail(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return redirect('/')  # 혹시 상세페이지 접속했을 때 게시글이 없다면 redirect
        # post_id를 받아와서 게시글 클릭하면 상세페이지로
        return render(request, 'tweet/post_detail.html',{'post':post}) #post_id를 받아와서 게시글 클릭하면 상세페이지로


