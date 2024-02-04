# README

Quick and dirty OpenAI API compatible server for HF chat.

```shell
git clone https://github.com/alexander-potemkin/HFChatServer.git && cd HFChatServer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 server.py &
```

## How to use

`pip install openai`

Use example, in Python, slightly altered version of [the official doc]([url](https://github.com/openai/openai-python)):

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key='iddqd',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
```

Available list of models is the following: ``, ``, ``.
