# Calendar
2019_공휴일안내_api




Django를 이용해 Restful한 API 서버를 구축 (두번째 프로젝트)
-------
   Google GCP
   Ubuntu 16.04-64-server
   Python 3.5.2
   Django 2.0.5
   django-rest-swagger 2.2.0

환경 세팅
-------
   $ sudo bash
   $ apt update
   $ python3 --version
   $ apt-get upgrade python3

   파이썬 버전을 확인해 준다. 파이썬 3.x 버전이 없다면 설치해준다.
   $ python --version
   $ python3 --version

     이어서 가상환경을 세팅해주기 위해 virtualenv를 설치해준다.
     $ apt-get install virtualenv
     $ exit
     virtualenv 설치가 완료되었다면 학습을 위한 가상환경을 생성한다.
     $ virtualenv -p python3 rest_env


     가상환경이 생성완료 되면, 가상환경을 activate 시켜준다. 정상적으로 가동되었다면 터미널 입력창 앞에 (rest_env)가 붙어있을 것이다.
     $ source ~/rest_env/bin/activate


     다음과 같이 프롬프트가 변경된다.
     (rest_env) jajangjajang@rest-api:~$  ← (rest_env) 가 앞에 붙는다.

     이어서 필요한 Django 및 파이썬 라이브러리들을 설치해준다.
     $ pip install django
     $ pip install djangorestframework
     $ pip install django-rest-swagger

Django 세팅
-------
     이제 startproject 명령어를 이용해 장고 프로젝트를 생성해 준다.
     $ cd ~/
     $ django-admin startproject rest_server
     $ cd rest_server


     이어서 rest_server/settings.py 파일을 열어서 다음과 같이 내용을 추가해준다.
     INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     
     'rest_framework',
     'rest_framework_swagger'
     ]
     
     $ (rest_env) root@rest-api:~/rest_server# pwd
        /home/jajangjajang/rest_server
     $ (rest_env) root@rest-api:~/rest_server#
     
     $ python manage.py startapp member
      그리고 rest_server/settings.py 파일에 Installed App에 방금 생성한 앱을 추가해준다.
      INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'rest_framework',
     'rest_framework_swagger',
     'member'
       ]

DB 세팅
-------- 
     이제 API를 이용해 접근할 수 있는 DB를 만들어준다. $ vim member/models.py 파일을 수정해준다.
      from django.db import models
      class Member(models.Model):
      name = models.CharField(max_length=200)
      mail = models.CharField(max_length=200)
      age = models.IntegerField(default=0) 
     
      모델을 수정한 경우 Django에서는 makemigration과 migrate를 해주어야 한다. 다음 명령어로 실행할 수 있다.
      $ python manage.py makemigrations member
      $ python manage.py migrate member

      이어서 생성한 모델에 값을 입력해준다. 장고는 터미널 상에서 manage.py shell 기능으로 편하게 DB를 수정할 수 있다.
      $ python manage.py shell
      >>> from member.models import Member
      >>> Member.objects.create(name='tester', mail='test@test.com', age=20)
      <Member: Member object (1)>
      >>> Member.objects.create(name='tester2', mail='test2@test.com', age=22)
      <Member: Member object (2)>
  
API 뷰 만들기
----
      이제 API요청에 따라 응답을 해주는 뷰를 작성해야 한다. 우선 member 폴더 하단에 api.py를 만들어주고 다음 내용을 작성한다.  
      $ vim member/api.py
      Seriallizer는 API를 통한 요청에 대한 응답의 형태를을 결정해주는 클래스이다. ViewSet은 요청을 처리하여 응답을 해주는 클래스이다. 
      추후에 이곳에 get, post, put, patch, delete에 대한 액션을 지정해주는 것이 가능하다.
      from .models import Member
      from rest_framework import serializers, viewsets

     class MemberSerializer(serializers.ModelSerializer):

     class Meta:
        model = Member
        fields = '__all__'

    class MemberViewSet(viewsets.ModelViewSet):
      queryset = Member.objects.all()
      serializer_class = MemberSerializer


      그리고 rest_server/urls.py 파일을 열어 api에 접근할 수 있도록 수정해준다. 
      $vim ./rest_srver/urls.py
      from django.conf.urls import url, include
      from django.contrib import admin
      from rest_framework import routers
      from rest_framework_swagger.views import get_swagger_view

      import member.api

      app_name='member'

      router = routers.DefaultRouter()
      router.register('members', member.api.MemberViewSet)

      urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/doc', get_swagger_view(title='Rest API Document')),
    url(r'^api/v1/', include((router.urls, 'member'), namespace='api')),
      ]
결과확인
-------
    $ python manage.py runserver 0.0.0.0:80
    결과확인 브라우저에서 http://localhost:8000/api/v1/members/

Django 재실행
-------
    $source ~/rest_env/bin/activate (가상머신 접근)
    $nohup python3 manage.py runserver 0.0.0.0:80 & (재실행)
    $ls -l
    $kill -9 <PID>


클라우드 서비스개발 전문가 과정 (2018.09.17 ~ 2019.02.28)
-------
[ 두번째 프로젝트 ]
-------
* 안응철 http://api.gcp.elimao.site/api/v1/calendar/
* 오동진 http://api.bestcloud.kr/api/v1/calendar/
* 신동민 http://api.gcp.ddms.me/api/v1/calendar/
* 한열   http://api.gcp.hanyeol.com/api/v1/calendar/
