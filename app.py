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
        # 1. Capturando exatamente o que está no seu HTML
        p1 = request.form.get('p1')
        p2 = request.form.get('p2')
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        trajetoria = request.form.get('trajetoria')

        # 2. Montando o prompt com as variáveis corretas
        prompt = f"""
        Aja como um psicólogo especializado em carreira. 
        Analise estas respostas de um jovem para uma gincana:
        
        PERGUNTAS ABERTAS:
        - Sobre pressão: {p1}
        - Sobre trabalho em equipe: {p2}
        
        DADOS ESTRUTURADOS (Alternativas):
        - Reação ao erro: {q1}
        - Reação à crítica: {q2}
        - Autopercepção: {q3}

        RELATO PESSOAL:
        "{trajetoria}"

        OBJETIVO:
        Crie um "Parecer do Especialista" motivador e profissional. 
        Analise a consistência entre as escolhas e o texto.
        Use títulos (###) e negrito (**) na resposta.
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