import os
import markdown  # Biblioteca para formatar a resposta da IA
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env (Segurança)
load_dotenv()

app = Flask(__name__)

# 2. Configuração da API do Google
minha_chave = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=minha_chave)

@app.route('/', methods=['GET', 'POST'])
def index():
    analise_html = None  # Variável que levará o texto formatado para o site
    
    if request.method == 'POST':
        p1 = request.form.get('p1')
        p2 = request.form.get('p2')
        
        # O prompt estruturado para o "PsycheBot"
        prompt = f"""
        Aja como um psicólogo especializado em carreira. 
        Analise estas respostas de um jovem para uma gincana:
        1. Sobre pressão: {p1}
        2. Sobre trabalho em equipe: {p2}
        
        Dê um feedback humano, motivador e profissional. 
        Use títulos e tópicos se necessário. Finalize com um ponto de melhoria prático.
        """

        try:

            model = genai.GenerativeModel('gemini-3.1-flash')
            
            response = model.generate_content(prompt)
            

            analise_html = markdown.markdown(response.text)
            
        except Exception as e:

            analise_html = f"<div class='erro'>Ocorreu um erro na conexão 3.1: {e}</div>"

    return render_template('index.html', resultado=analise_html)

if __name__ == '__main__':
    app.run(debug=True)