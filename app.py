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
        

        prompt = f"""
        Aja como um psicólogo especializado em carreira. 
        Analise estas respostas de um jovem para uma gincana:
        1. Sobre pressão: {p1}
        2. Sobre trabalho em equipe: {p2}
        
        Dê um feedback humano, motivador e profissional. 
        Finalize com um ponto de melhoria prático.
        """

        try:

            model = genai.GenerativeModel('gemini-1.5-flash')
            

            response = model.generate_content(prompt)
            

            analise_html = markdown.markdown(response.text)
            
        except Exception as e:
            analise_html = f"Erro técnico: {e}"

    return render_template('index.html', resultado=analise_html)

if __name__ == '__main__':
    app.run(debug=True)