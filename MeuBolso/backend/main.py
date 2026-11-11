
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="MeuBolso API",
    description="API para controle de gastos pessoais",
    version="1.0.0"
)

ARQUIVO = "dados.json"


# Modelo de um gasto
class Gasto(BaseModel):
    descricao: str
    valor: float
    categoria: str


# Ler os gastos salvos
def carregar_gastos():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# Salvar os gastos
def salvar_gastos(gastos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(gastos, arquivo, indent=4, ensure_ascii=False)


@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à API MeuBolso!",
        "status": "online"
    }


# Cadastrar um gasto
@app.post("/gastos")
def cadastrar_gasto(gasto: Gasto):
    gastos = carregar_gastos()

    novo_gasto = {
        "id": len(gastos) + 1,
        "descricao": gasto.descricao,
        "valor": gasto.valor,
        "categoria": gasto.categoria
    }

    gastos.append(novo_gasto)
    salvar_gastos(gastos)

    return novo_gasto



# Listar todos os gastos
@app.get("/gastos")
def listar_gastos():
    gastos = carregar_gastos()
    return gastos



# Consultar um gasto pelo ID
@app.get("/gastos/{gasto_id}")
def buscar_gasto(gasto_id: int):
    gastos = carregar_gastos()

    for gasto in gastos:
        if gasto["id"] == gasto_id:
            return gasto

    return {"erro": "Gasto não encontrado"}



# Editar um gasto
@app.put("/gastos/{gasto_id}")
def editar_gasto(gasto_id: int, gasto_atualizado: Gasto):
    gastos = carregar_gastos()

    for gasto in gastos:
        if gasto["id"] == gasto_id:
            gasto["descricao"] = gasto_atualizado.descricao
            gasto["valor"] = gasto_atualizado.valor
            gasto["categoria"] = gasto_atualizado.categoria

            salvar_gastos(gastos)

            return {
                "mensagem": "Gasto atualizado com sucesso!",
                "gasto": gasto
            }

    return {"erro": "Gasto não encontrado"}



# Excluir um gasto
@app.delete("/gastos/{gasto_id}")
def excluir_gasto(gasto_id: int):
    gastos = carregar_gastos()

    for gasto in gastos:
        if gasto["id"] == gasto_id:
            gastos.remove(gasto)
            salvar_gastos(gastos)

            return {
                "mensagem": "Gasto excluído com sucesso!"
            }

    return {"erro": "Gasto não encontrado"}



# Resumo financeiro
@app.get("/resumo")
def resumo_financeiro():
    gastos = carregar_gastos()

    total = sum(gasto["valor"] for gasto in gastos)
    quantidade = len(gastos)

    return {
        "total_gasto": round(total, 2),
        "quantidade_gastos": quantidade
    }
