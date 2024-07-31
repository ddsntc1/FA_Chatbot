
### main.py 실행-> 서버에서 실행 시켜놓으면 됩니당
```python
# 터미널 실행
uvicorn main:app --port <원하는 포트번호> --reload
```



### API 응답 호출 방법 -> django 내에서 모델 사용할 부분에 붙이시면 됩니다

```python
import requests
url = '주소:포트번호/query'
payload = {'query': 입력문}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=payload, headers=headers)
response.json() # 모델 응답 결과
# response.json()['response'].split(payload['query'])[-1]
```






