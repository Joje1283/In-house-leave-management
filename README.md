멤버의 휴가를 관리하기 위한 애플리케이션 개발

# 요구사항 분석

## 개요

- 회원을 등록할 수 있어야 한다.
- 휴가 종류를 등록할 수 있어야 한다.
- 회원에 의해 휴가 신청 및 결재(수락/거부)가 가능해야 한다.

## 상세

### 회원 기능

- 회원 등록
- 회원 조회
- 결재자 변경

### 휴가 기능

- 휴가 등록
- 휴가 조회
- 휴가 수정

### 결재 기능

- 휴가 결재 (수락 / 거절)
- 결재 내역 조회

### 신청 기능

- 휴가 신청
- 신청 내역 조회
- 신청 취소

### 부여 기능

- 휴가 부여
- 남은 휴가 확인

### 푸시 기능

- 휴가 신청, 취소 시 결재자에게 푸시
- 휴가 수락, 반려 시 신청자에게 푸시

# 도메인 모델 설계
<img width="572" alt="image" src="https://user-images.githubusercontent.com/23291627/172041701-46d2198e-8113-4c75-bdd8-860db97a44b4.png">


# 엔티티 설계
![image](https://user-images.githubusercontent.com/23291627/173229934-c638b071-3816-41ef-aff0-032acc35c764.png)

# CI/CD
- CI는 Git Action활용. 도커 빌드 후 홈서버 배포 (.github/workflows/home.yml 참고)
- github action secrets 설정
  - AWS SES : AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY, WELCOME_EMAIL_SENDER
  - Celery (RabbitMQ) : CELERY_BROKER_URL
  - Database: DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
  - Docker Hub: DOCKER_HUB_USERNAME, DOCKER_HUB_PASSWORD
  - Server: SERVER_HOST, SERVER_PASSWORD, SERVER_PORT, SERVER_USERNAME, STATIC_ROOT, DJANGO_SECRET_KEY
  - Debug: SENTRY_DSN
- 배포 과정
  1. CI 트리거는 main에 push할때이다. 
  2. 웹서버에 대한 도커 로그인, 이미지 빌드 및 푸시 수행 (도커 허브)  
  3. 푸시워커에 대한 도커 로그인, 이미지 빌드 및 푸시 수행 (도커 허브)  
  4. SSH로 홈서버에 접속한다.  
    - 웹서버 이미지를 풀 받고, 기존의 컨테이너를 멈춘 후 새로 받은 이미지를 실행한다. 
    - 푸시워커 이미지를 풀 받고, 기존의 컨테이너를 멈춘 후 새로 받은 이미지를 실행한다. 
    - 정적 리소스를 다운로드 받는다. (정적 리소스 위치에서 collectstatic 명령을 수행) 
# 아키텍처
<img width="578" alt="image" src="https://user-images.githubusercontent.com/23291627/178140662-32d6889e-b033-4dc2-98e3-8be4cbe60bdf.png">

- 프록시 서버(Nginx)는 정적 파일 요청 시 파일 시스템의 리소스를, 나머지는 웹서버 응답을 서빙한다. 
- 웹 서버(장고)는 데이터베이스(PostgreSQL)에 CRUD를 수행하고 푸시워커를 통해 비동기 작업을 수행한다.
- 푸시워커(RabbitMQ)는 웹서버가 예약한 task를 수행한다. (푸시 알림)
- AWS SES를 통해 이메일 알림을 구현했다.
- 모두 하나의 머신에서 구현하였고 데이터베이스, 웹서버, 푸시워커는 도커 컨테이너로 배포하였다. 프록시서버 및 정적리소스는 OS에 직접 설치 했다.
