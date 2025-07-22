# Introduction
Django + MySQL 기반 맛집 추천 웹 애플리케이션입니다.  
Elastic Beanstalk을 이용해 AWS에 배포합니다.

## 프로젝트 구조
AIRestaurant/
├── proj/ # Django 설정 모듈
├── restaurant/ # 앱
├── templates/ # 템플릿 HTML
├── .env # 환경변수 파일 (Git에 업로드 금지)
├── requirements.txt # 설치 패키지 목록
└── manage.py

## Preparation

가상 환경 설정 (WSL/macOS 공통)

cd AIRestaurant
python3 -m venv venv
source venv/bin/activate

패키지 설치

pip install -r requirements.txt

환경 변수 설정(.env)

PRODUCTION=1
DB_NAME=product_db
DB_USER=db_user
DB_PASSWORD=your_password
DB_HOST=your-db.xxxxx.rds.amazonaws.com
S3_BUCKET=your-s3-bucket-name

AWS CLI 설치
https://aws.amazon.com/ko/cli/

EB CLI 설치 (WSL)
WSL (Ubuntu 환경):

pip install --upgrade pip
pip install awsebcli --upgrade --user

EB CLI 설치 (macOS)
macOS (Homebrew 사용):

``bash
brew install awsebcli

## AWS 준비

- EC2 가 사용할 보안그룹을 하나 준비하고 해당 보안그룹아이디를 이용하여 EB 환경을 생성해야 합니다.
- RDS 인스턴스를 하나 생성하고 외부 접속을 허용한 다음 EC2가 사용할 보안그룹에도 MySQL 접속을 허용해줍니다.
- IAM에서 `aws-elasticbeanstalk-ec2-role` 에 S3 Full Access 등 해당 버킷의 쓰기 권한을 얼여줘야 합니다.

## Git

Git 설치
https://git-scm.com/book/ko/v2/시작하기-Git-설치

설치 후에

git init
git add .
it commit -m "Initial Commit"


## Deployment


eb init

# 설정 내용
eb create \
 --vpc.id vpcID \
 --vpc.securitygroups 보안그룹ID \
 --vpc.ec2subnets 서브넷ID,서브넷ID... \ 4개 서브넷 (만약 개수가 4개가 아니라면 region을 서울로 세팅 필요)
 --envvars PRODUCTION=1,DB_NAME=product_db,DB_USER=db_user,DB_PASSWORD=마스터암호,DB_HOST=DB엔드포인트,S3_BUCKET=버킷이름 \
 --vpc.elbpublic \
 --vpc.publicip

<!-- # 설정 내용
eb create \
 --vpc.id vpc-02027670f21362b27 \
 --vpc.securitygroups sg-0c21711ec6a322509 \
 --vpc.ec2subnets subnet-027472004f1664c04,subnet-055c529c1dccbf9f7,subnet-040a41f176ae3bde8,subnet-0cbb9caae23f924c4 \
 --envvars PRODUCTION=1,DB_NAME=restaurant_db,DB_USER=admin,DB_PASSWORD=9cML3Al9miqUpOeIz6bY,DB_HOST=airest-db.c1c6aqgaevrj.ap-northeast-2.rds.amazonaws.com,S3_BUCKET=airestaurants-dev \
 --vpc.elbpublic \
 --vpc.publicip -->
