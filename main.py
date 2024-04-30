from flask import Flask, Response, request, jsonify
import ollama

app = Flask(__name__)

# Default completion route


@app.route('/', methods=['POST'])
def index():
    print("request", request.get_json())
    prompt = request.get_json()['prompt']
    print(prompt)
    # Run OLLAMA local server here
    output = ollama.generate(
        model="llama3", prompt=prompt, stream=False)
    print(output['response'])
    # return Response(output['response'], mimetype='text/html')
    return jsonify({"response": output['response']}), 201


@app.route("/subject", methods=['POST'])
def subjectize():
    body = request.get_json()
    comment = body['comment']
    subjects = body['subjects']
    messages = [
        {
            'role': 'system',
            'content': 'You are a comment classification bot. You will be given a list of subjects and a comment from a user. You will determine which subjects the comment belongs to and return a comma separated list of these subjects. Say YES if you understand.'
        }, {
            'role': 'assistant',
            'content': 'YES'
        }, {
            'role': 'system',
            'content': 'these are the subjects: cleanliness,customer service,product availability,pricing,shipping,timeliness,ease of purchase'
        }, {
            'role': 'user',
            'content': 'it was hard for me to find what I was looking for, and it cost more than I would have wanted.'
        }, {
            'role': 'assistant',
            'content': 'ease of purchase,product availability,pricing'
        }, {
            'role': 'system',
            'content': f'these are the subjects:{subjects}'
        }, {
            'role': 'user',
            'content': f'{comment}'
        }
    ]
    response = ollama.chat('llama3', messages=messages)
    print(response['message']['content'])
    return jsonify({'response': response['message']['content']})


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
