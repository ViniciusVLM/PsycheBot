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
        p1 = request.form.get('p1')
        p2 = request.form.get('p2')
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')

        trajetoria = request.form.get('trajetoria')

        prompt = f"""
        Aja como um psicólogo especializado em carreira. 
        Analise estas respostas de um jovem para uma gincana:
        1. Sobre pressão: {p1}
        2. Sobre trabalho em equipe: {p2}
        
        DADOS ESTRUTURADOS (Escolhas do candidato):
        1. Reação ao erro: {resp1}
        2. Reação à crítica: {resp2}
        3. Autopercepção de qualidades: {resp3}

        RELATO PESSOAL (Narrativa do candidato):
        "{trajetoria}"

        OBJETIVO:
        Crie um "Parecer do Especialista" que seja:
        - Motivador, mas realista.
        - Analise se as escolhas das alternativas batem com o que ele escreveu no texto.
        - Destaque as qualidades mencionadas.
        - Ofereça uma estratégia prática para ele lidar com os pontos que deseja aprimorar.
        - Use títulos (###) e negrito (**) para organizar a resposta.

        Dê um feedback humano, motivador e profissional. 
        Finalize com um ponto de melhoria prático.
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