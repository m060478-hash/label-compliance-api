from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LabelInput(BaseModel):
    categoria: str
    texto_rotulo: str

def analisar_rotulo(categoria, texto):
    erros = []
    score = 100

    if "teor alcoólico" not in texto.lower():
        erros.append("Ausência de teor alcoólico")
        score -= 20

    if "contém glúten" not in texto.lower() and "não contém glúten" not in texto.lower():
        erros.append("Ausência de declaração de glúten")
        score -= 20

    if "importador" not in texto.lower():
        erros.append("Ausência de identificação do importador")
        score -= 20

    return {
        "score": score,
        "erros": erros,
        "status": "Conforme" if score >= 80 else "Não Conforme"
    }

@app.post("/analisar")
def analisar(dados: LabelInput):
    resultado = analisar_rotulo(dados.categoria, dados.texto_rotulo)
    return resultado
