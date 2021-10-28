# CDM

1. Setting

- Server: Flask
- Design: webix
- install info...

```
pip install paramiko
pip install json
pip install cryptography
pip install Werkzeug
```
2. 가상환경 진입 후
```
1. export FLASK_APP=app
2. export FLASK_ENV=development
3. flask run
```

4. Login Info

```
# routes.py 파일에 로그인 정보 하드 코딩
id: "asd@asd.com"
pw: "asd"
```

- 경우에 따라 로그인 실패할 수 있음 ex) 302 오류
- 문제 원인 파악 중
- ## 오류 처리하는 코드는 27일 이후 추가 예정

4. SFTP

- paramiko 사용
- routes.py 파일에 연결할 SFTP 정보 하드 코딩

5. 수정 내용
* 모든 IP 허용하도록 수정 (CORS 정책 수정)

* Failed to load resource: the server responded with a status of 404 (NOT FOUND) → favicon.ico 없는 경우 에러 방지 처리
```
 <link rel="shortcut icon" href="data:image/x-icon" type="image/x-icon">
 ```
* IRB 페이지 로그인 문제 발생 시 에러 문구 추가
```
.fail((xhr) => {
    var response = JSON.parse(xhr.response);
    var message = response.error.message + " 다음과 같은 로그인 시 문제가 발생하였습니다.";
    console.log(message);
})
```
* swagger API 사용할 때 서버 연결 문제 발생 시 에러 문구 추가
```
.fail((xhr) => {
    alert("IRB 서버 연결 상태를 확인하세요.");
});
```