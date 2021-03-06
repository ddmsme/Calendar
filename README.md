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
    $cd rest_server/
    $pwd
       /home/username/rest_server
    $ ls -l
       total 28
      drwxr-xr-x 4 root root 4096 Dec 11 02:19 calendar2019
      -rw-r--r-- 1 root root 5120 Dec 11 02:16 db.sqlite3
      -rwxr-xr-x 1 root root  543 Dec 11 00:56 manage.py
      drwxr-xr-x 4 root root 4096 Dec 11 01:14 member
      -rw------- 1 root root 1530 Dec 19 01:04 nohup.out
      drwxr-xr-x 3 root root 4096 Dec 11 02:23 rest_server
    $nohup python3 manage.py runserver 0.0.0.0:80 & (재실행)
    $ls -l
    $kill -9 <PID>
    
# (추가내용) Postman을 활용한 API 예제

__Postman이란?__

Postman은 개발한 API를 테스트하고, 테스트 결과를 공유하여 API 개발의 생산성을 높여주는 플랫폼 입니다.<br>
위에서 Django를 이용하여 작성한 API를 테스트하기 위하여 Postman을 설치후, API를 테스트하기 위한 환경설정 후 데이터 입/출력 테스트를 진행합니다.<br><br><br><br>

<br><br><br>
1. Postman 프로그램을 다운로드 받기위해 해당 사이트로 이동(회원가입이 필요합니다 ^^)<br><br><br>


![순서](https://github.com/ddmsme/Calendar/blob/master/img/1.jpg)<br><br><br>


<br><br><br>
2. Postman 프로그램을 실행하면 아래 그림과 같은 화면이 나타납니다.<br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/2.jpg)<br><br><br>


<br><br><br>
3. API 테스트를 위해 콜렉션(Collection)을 하나 생성합니다. Collection이름은 __calendar__ 로 지정하고 생성(Create) 버튼을 클릭합니다.<br>
참고로 Collection명은 임의로 설정 가능합니다.<br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/3.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/4.jpg)<br><br><br>

<br><br><br>
4. 해당 콜렉션(Collection)에 마우스 오른쪽 버튼을 클릭 후 __Request__ 를 하나 추가합니다. <br>
__Request Name__ 은 달력정보 가져오기 get 외에 임의로 지정 가능합니다.<br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/5.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/6.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/7.jpg)<br><br><br>

<br><br><br>
5. 해당 콜렉션에서 사용할 __환경변수__ 설정을 하기위해 Postman오른쪽 상단에 아래에 그림과 같은 설정 버튼을 클릭해주세요. <br>
클릭 후 __Manage Enviroment__ 창에 Add버튼을 클릭합니다. 환경변수 입력창에 이름과 등록할 환경 변수와 값을 입력합니다.(이미지 참고)<br><br><br>


![순서](https://github.com/ddmsme/Calendar/blob/master/img/8.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/9.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/10.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/11.jpg)<br><br><br>


<br><br><br>
6. 그럼 등록된 API주소에 접속하여 필요한 날짜 정보를 가져와보겠습니다. 우선 환경변수를 사용하기 위해 등록한 환경변수(calender_env)를 선택후<br>
Postman에 등록된 Request(달력 가져오기 get)을 클릭후 나타나는 오른쪽 화면에서 그림에 표시된 것 같이 __{{end_point)}__ 라는 값을 입력합니다.<br> {{end_point}}는 방금전 등록한 환경변수를 의미합니다. 정보가 정확히 입력되었다면 __send__ 버튼을 클릭하여 결과를 확인합니다.<br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/12.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/13.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/14.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/15.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/16.jpg)<br><br><br>


7. 그럼 다음엔 등록된 API를 이용하여 데이터를 입력하는 설정을 해보도록 하겠습니다. <br>
우선 위쪽에서 __Request__ 를 등록했던 부분과 동일하게 우선 Request를 하나 추가합니다. 이번에 등록할 Request의 이름은 달력정보 입력하기 - post<br>
입력 후 해당 Request를 클릭 후 요청정보를 get->post로 변경 후 저장(Save)합니다. <br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/17.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/18.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/19.jpg)<br><br><br>

7.2 등록한 __Request '달력정보 입력하기 - post'__ 주소입력창에 __환경변수 {{end_point}}__ 를 설정 후에 입력할 데이터를 지정하기 위해서 설정이 필요합니다. (두번째 이미지 참고) 여기서 __KEY__ 란? API에서 사용되는 변수명 __VALUE__ 는 입력될 데이터라 생각하시면 될 것 같습니다.

![순서](https://github.com/ddmsme/Calendar/blob/master/img/20.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/24.jpg)<br><br><br>

<br><br><br>
7.3 설정 후 __Send__ 를 클릭합니다. 값이 정상적으로 입력이 되면 화면 아래에 입력된 값이 표시됩니다.<br>
입력이 확인되었다면 __Request '달력정보 가져오기 - get'__ 을 실행해보면 등록된 값이 표시됩니다.
<br><br><br>

![순서](https://github.com/ddmsme/Calendar/blob/master/img/22.jpg)<br><br><br>
![순서](https://github.com/ddmsme/Calendar/blob/master/img/23.jpg)<br><br><br>



<br><br><br>
클라우드 서비스개발 전문가 과정 (2018.09.17 ~ 2019.02.28)
-------
[ 두번째 프로젝트 ]
-------
* 안응철 http://api.gcp.elimao.site/api/v1/calendar/
* 오동진 http://api.bestcloud.kr/api/v1/calendar/
* 신동민 http://api.gcp.ddms.me/api/v1/calendar/
* 한열   http://api.gcp.hanyeol.com/api/v1/calendar/
