
### main.py 실행
```python
# 터미널 실행
uvicorn main:app --reload
```



### API 응답 호출 방법 

```python
import requests
url = '주소:포트번호/query'
payload = {'query': 사용자가 입력한 query를 str형태로 입력받아융}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=payload, headers=headers)
print(response.json())```



