from flask import Flask, redirect, render_template, request
import openai
import config

app = Flask('KDL OpenSource')

@app.route('/')
async def kdlindex():
    return 'Sorry, this page is not ready!', 403

def generate(mssg):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages = [{"role": "user", "content" : f"{mssg}"}]
        ).get("choices")[0]
        return completion
    except Exception as e:
        return { "finish_reason": "stop", "index": 0, "message": { "content": "Ошибка при обработке запроса! Пожалуйста подождите около 20 секунд и повторите попытку.", "role": "assistant" } }

@app.route('/privatekey/ai')
async def ai():
    requestgpt = request.args.get('rqst', default='')
    if requestgpt != '':
        try:
            ffn = generate(f'{requestgpt}')
            ffn2 = ffn['message']
            uresp = ffn2['content']
            return render_template('ai.html', resp=f'{uresp}')
        except:
            return render_template('ai.html', resp=f'Ошибка при обработке запроса! Пожалуйста подождите несколько секнуд и повторите попытку.'), 500
    return render_template('ai.html', resp='')

openai.api_key = config.OPENAI_TOKEN
app.run(debug=True)
