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

### 휴가 기능

- 휴가 등록
- 휴가 조회
- 휴가 수정

### 결재 기능

- 휴가 결재 (수락 / 거절)
- 결재 내역 조회
- 결재 내역 수정

### 신청 기능

- 휴가 신청
- 신청 내역 조회
- 신청 취소

### 부여 기능

- 휴가 부여
- 휴가 삭제

# 도메인 모델 설계
<img width="761" alt="image" src="https://user-images.githubusercontent.com/23291627/171995959-8a29873e-f7ad-42f1-a678-20d64655944d.png">

# 엔티티 설계
<img width="1184" alt="image" src="https://user-images.githubusercontent.com/23291627/171995886-8717e63a-15e6-48fb-a4f3-fced98e6e8ad.png">

# URL 설계
```
"""
url
휴가 승인: /members/1/signs/5/confirm
휴가 반려: /members/1/signs/5/reject

휴가 신청: /members/1/orders/new
휴가 조회: /members/1/orders/

휴가 부여 /grants/new

휴가 생성 /leaves/new
"""
```


