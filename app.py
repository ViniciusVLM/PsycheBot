import os
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
        # 1. Pegando os dados do formulário
        p1 = request.form.get('p1', '')
        p2 = request.form.get('p2', '')
        q1 = request.form.get('q1', 'N/A')
        q2 = request.form.get('q2', 'N/A')
        q3 = request.form.get('q3', 'N/A')
        trajetoria = request.form.get('trajetoria', '')

        # 2. Criando o prompt (SÓ EXISTE AQUI DENTRO)
        prompt = f"""
        Analise este perfil profissional:
        - Pressão: {p1}
        - Equipe: {p2}
        - Escolhas (Alternativas): {q1}, {q2}, {q3}
        - Relato Pessoal: {trajetoria}
        
        Dê um parecer motivador e profissional em Markdown.
        """

        try:

            model = genai.GenerativeModel('gemini-3-flash-preview')
            

            response = model.generate_content(prompt)
            
            analise_html = markdown.markdown(response.text)
        except Exception as e:

            analise_html = f"Erro na conexão com Gemini 3: {e}"

        return render_template('index.html', resultado=analise_html)

if __name__ == '__main__':
    app.run(debug=True)