# Logging

## Installation
```shell
poetry shell
poetry install
```

## Getting Started
```shell
python app/logger.py
```


## 1. Logging Basics

### 1.1 로그와 데이터
- 로그
    - 컴퓨터에 접속한 기록, 특정 행동을 한 경우 남는 것
    - 우리가 앱을 사용할 때 한 행동들은 ‘사용자 로그 데이터’, ‘이벤트 로그 데이터’ 등의 로그로 기록되는 것처럼, 머신러닝에서도 인퍼런스 요청 기록과 인퍼런스 결과 등을 로그로 저장해야 함
- 데이터의 종류
    - 데이터베이스 데이터 (서비스 로그, Database에 저장)
        - 서비스의 운영을 위해 필요한 데이터
        - ex. 가입일, 구매 목록 등
    - 사용자 행동 데이터 (유저 행동 로그, 주로 Object Storage나 데이터 웨어하우스에 저장)
        - 앱이나 웹에서 유저의 행동을 기록한 데이터
            - UX와 관련하여 인터렉션이 이루어지는 관점에서 발생하는 데이터
        - 서비스 운영을 위해 필수적인 데이터는 아니며, 주로 데이터 분석을 위해 저장됨
        - ex. 클릭, 조회, 스와이프 등
    - 인프라 데이터 (metric)
        - 백엔드 웹 서버가 제대로 동작하고 있는지 확인하는 데이터
        - ex. request 수, response 수, DB 부하 등

⇒ 이렇게 저장된 데이터를 활용하여 현재 시스템이 잘 동작하는지 알 수 있다. 만약 데이터가 저장되어 있지 않다면, 과거에 어떤 이벤트가 발생했었는지 알 수 없어 문제를 해결하거나 개선점을 찾기 어렵다. 

### 1.2 데이터 적재 방식
- Database(RDBMS)에 저장하는 방식
    - 행과 열로 구성되며, 데이터 간의 관계 존재
    - 영구적으로 저장해야 하는 데이터 및 웹, 앱 서비스에서 사용되는 데이터 저장
    - 데이터 추출 시 SQL(MySQL, PostgreSQL 등) 활용
- Database(NoSQL)에 저장하는 방식
    - 데이터가 많아지며 RDBMS로 트래픽을 감당하기 어려워져 개발되었으며, 일반적으로 RDBMS에 비해 쓰기와 읽기 속도가 빠름
    - NoSQL = Not Only SQL. 스키마가 strict한 RDBMS와 다르게 스키마가 없거나 느슨한 스키마만 적용
    - Elasticsearch, Logstash or Fluent, Kibana에서 활용하려는 경우 사용
    - 종류
        - Key Value Store: 키-값 쌍으로 데이터 저장. Redis, DynamoDB 등
        - Document Database: 키-값 쌍의 컬렉션인 ‘문서’ 개념을 사용하여 데이터 저장. MongoDB 등
        - Column Family: 컬럼 패밀리(관련 컬럼 집합)의 데이터를 함께 저장하는 방식. BigTable, Apache Cassandra 등
        - Graph Database: '노드'와 '엣지' 개념을 사용하여 데이터와 그들 사이의 관계를 저장. Neo4j, Amazon Neptune 등
- Object Storage에 저장하는 방식
    - 어떤 형태의 파일도 저장할 수 있는 저장소
    - 비즈니스에서는 사용되지 않지만 분석을 위해 필요한 데이터를 저장
    - 특정 시스템에서 발생하는 로그를 xxx.log(파일)에 저장한 후, 해당 파일을 Object Storage에 저장하는 형태
    - 필요 시 별도로 Database나 Data Warehouse로 옮기는 작업 필요
    - AWS S3, Cloud Storage 등
- Data Warehouse에 저장하는 방식
    - 여러 공간에 저장된 데이터를 모두 모아두는 통합적인 데이터 창고
    - AWS Redshift, GCP BigQuery, Snowflake 등


## 2. Logging in Python

### 2.1 Python Logging Module
- logging
    - 파이썬 기본 로깅 모듈
    - 심각도에 따라 debug, info, warning, error, critical의 카테고리로 데이터 저장 가능
- Log Level
    | level | Value | 설명 |
    | --- | --- | --- |
    | DEBUG | 10 | (문제 해결에 필요한) 자세한 정보를 공유 |
    | INFO | 20 | 작업이 정상적으로 작동하고 있는 경우 사용 |
    | WARNING | 30 | 예상하지 못한 일이거나 발생 가능한 문제일 경우. 작업은 정상적으로 수행 |
    | ERROR | 40 | 프로그램이 함수를 실행할 수 없는 심각한 상황 |
    | CRITICAL | 50 | 프로그램이 동작할 수 없는 심각한 문제 |
    - 기본 logging level은 WARNING으로, WARNING 이상의 레벨에 대한 로그만 보여줌
- logging vs print
    - print
        - console에만 output을 출력
    - logging
        - 파이썬이 다룰 수 있는 모든 format으로 output 출력 가능
        - output의 근원 파악 가능
        - 심각도에 따라 output 분류 가능

### 2.2 Logger
- logging.getLogger(name)으로 logger object 생성
    - name이 주어지면 해당 name의 logger를 사용하며, name이 없는 경우 root logger를 사용
    - 마침표로 계층 구조 구분
      ex. logging.getLogger('foo.bar') -> logging.getLogger('foo')의 자식 logger
- log를 생성하는 method 제공
- log level과 logger에 적용된 filter를 기반으로 처리가 필요한 log인지 판단
    - logging.setLevel(): logger에서 사용할 level 지정
- Handler에게 LogRecord 인스턴스 전달

### 2.3 Handler
- logger에서 만들어진 log를 적절한 위치로 전송 (파일로 저장, console에 출력 등)
- level과 formatter로 필터링 가능
- StreamHandler, FileHandler, HTTPHandler 등

### 2.4 Formatter
- 최종적으로 출력될 log message의 formatting 설정
- 시간, log 이름, 심각도, output, 함수 이름, line 정보, 메시지 등 다양한 정보 제공

### 2.5 Logging Flow
![logging flow](/Boostcamp Ai Tech/product_serving/Boostcamp-AI-Tech-Product-Serving/assets/images/스크린샷 2023-07-14 오전 11.28.42.png)

## 3. Online Serving Logging (BigQuery)

### 3.1 BigQuery 데이터 구조

### 3.2 BigQuery 데이터세트 만들기

### 3.3 BigQuery 테이블 만들기

### 3.4 BigQuery로 실시간 로그 데이터 수집하기