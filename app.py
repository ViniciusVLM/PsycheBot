import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv  # Importa a função para carregar o .env

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

app = Flask(__name__)

# Pega a chave que está guardada no ambiente
minha_chave = os.getenv("GEMINI_API_KEY")

# Configura a IA usando a variável
genai.configure(api_key=minha_chave)

@app.route('/', methods=['GET', 'POST'])
def index():
    analise = None
    if request.method == 'POST':
        p1 = request.form.get('p1')
        p2 = request.form.get('p2')
        
        # O prompt que enviaremos para a IA
        prompt = f"""
        Aja como um psicólogo especializado em carreira. 
        Analise estas respostas de um jovem para uma gincana:
        1. Sobre pressão: {p1}
        2. Sobre trabalho em equipe: {p2}
        
        Dê um feedback humano, motivador e profissional com um ponto de melhoria.
        """

        try:
            # USANDO O MODELO QUE VOCÊ ENCONTROU NO DIAGNÓSTICO
            model = genai.GenerativeModel('models/gemini-3-flash-preview')
            
            response = model.generate_content(prompt)
            analise = response.text
        except Exception as e:
            analise = f"Erro ao conectar com a IA: {e}"

    return render_template('index.html', resultado=analise)

if __name__ == '__main__':
    app.run(debug=True)