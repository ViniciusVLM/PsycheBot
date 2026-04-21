import os
from xml.parsers.expat import model
import markdown
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


minha_chave = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=minha_chave)

@app.route('/', methods=['GET', 'POST'])
def index():
    analise_html = None
    
    if request.method == 'POST':
        # Tudo o que acontece APÓS o clique do botão fica aqui dentro
        p1 = request.form.get('p1', '')
        p2 = request.form.get('p2', '')
        q1 = request.form.get('q1', 'N/A')
        q2 = request.form.get('q2', 'N/A')
        q3 = request.form.get('q3', 'N/A')
        trajetoria = request.form.get('trajetoria', '')

        prompt = f"Analise: {p1}, {p2}, {q1}, {q2}, {q3}. Texto: {trajetoria}"
        try:

            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            response = model.generate_content(prompt)
            analise_html = markdown.markdown(response.text)
        except Exception as e:
            analise_html = f"Erro na IA: {e}"

    return render_template('index.html', resultado=analise_html)
if __name__ == '__main__':
    app.run(debug=True)