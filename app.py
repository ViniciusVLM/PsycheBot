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
    # ...
    try:

        model = genai.GenerativeModel(
            model_name='gemini-3.1-flash'
        )
        

        response = model.generate_content(prompt)
        analise_html = markdown.markdown(response.text)
        
    except Exception as e:

        analise_html = f"<div class='erro'>Erro técnico: {e}</div>"

    return render_template('index.html', resultado=analise_html)

if __name__ == '__main__':
    app.run(debug=True)