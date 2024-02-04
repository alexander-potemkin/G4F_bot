# Example

```python
import json

from openai import OpenAI

client = OpenAI(
        base_url="http://localhost:8787",
        api_key="sk-no-key-required"
    )

response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
response_dict = json.loads(response)
message = response_dict['choices'][0]['message']['content']

print(message)
```

С помощью данного кода можно обратиться к серверу, используя OpenAPI SDK

В ответ получим:

> Hello! How can I help you today?
>
