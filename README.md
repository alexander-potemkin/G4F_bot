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
    base_url="http://localhost:8787",
    api_key='iddqd',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="whatever",
)
```

Server can work with the following models: `mistralai/Mixtral-8x7B-Instruct-v0.1`, `meta-llama/Llama-2-70b-chat-hf`, `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO`, `mistralai/Mistral-7B-Instruct-v0.2`, `openchat/openchat-3.5-0106` - the source code has to be adjusted; or server functionality needs to extended to support model choosing via request (ideally).
