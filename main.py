from flask import Flask, Response, request
import ollama

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    print("request", request.get_json())
    prompt = request.get_json()['prompt']
    print(prompt)
    # Run OLLAMA local server here
    output = ollama.generate(
        model="llama3", prompt=prompt, stream=False)
    print(output['response'])
    return Response(output['response'], mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)
