import g4f
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import time


def create_fake_openapi_response(prompt, generated_text):
    fake_response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": generated_text,
                    "created": int(time.time())
                },
                "logprobs": None
            }
        ],
        "created": int(time.time()),
        "id": "fake-id",
        "model": "gpt-3.5-turbo",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": len(generated_text.split()),
            "prompt_tokens": len(prompt.split()),
            "total_tokens": len(prompt.split()) + len(generated_text.split())
        }
    }

    return json.dumps(fake_response, indent=2)


def convert_openapi_to_langchain(openapi_request):
    user_message = openapi_request.get('messages', [{}])[0].get('content', '')
    return {"prompt": user_message}


class MyRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        path = urlparse(self.path).path

        if path == '/chat/completions':
            content_length = int(self.headers['Content-Length'])
            openapi_request = json.loads(self.rfile.read(content_length).decode())

            langchain_request = convert_openapi_to_langchain(openapi_request)
            user_message = langchain_request["prompt"]

            try:
                response = g4f.ChatCompletion.create(
                    model="openchat/openchat-3.5-0106",
                    provider=g4f.Provider.HuggingChat,
                    messages=[{"role": "user", "content": user_message}],
                    stream=True,
                )

                response_string = ""

                for message in response:
                    response_string += str(message)

                fake_openapi_response = create_fake_openapi_response(user_message, response_string)
                json_response = json.dumps(fake_openapi_response, indent=2)

            except Exception as e:
                # Log the exception for debugging
                print(f"Error in g4f.ChatCompletion.create: {e}")
                import traceback
                traceback.print_exc()
                json_response = json.dumps({'error': 'Internal Server Error'}, indent=2)

        else:
            json_response = json.dumps({'error': 'Path not found'}, indent=2)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json_response.encode())


if __name__ == '__main__':
    args = sys.argv
    default_port = 8787
    port_arg = next((arg for arg in parse_qs(urlparse(args[0]).query).get('port', []) if arg.isdigit()), None)
    port = int(port_arg) if port_arg else default_port

    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)

    httpd.serve_forever()
