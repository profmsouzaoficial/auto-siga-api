import os
import traceback
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from siga_bot import SigaAPI

app = FastAPI(title="API AUTO-SIGA UFJF (HTTP Direto)")

# ==========================================
# 1. SEGURANÇA E AUTENTICAÇÃO DA API
# ==========================================
api_key_header = APIKeyHeader(name="X-API-Key")

def validar_api_key(chave_recebida: str = Security(api_key_header)):
    chave_mestra = os.getenv("API_SECRET_KEY")
    if not chave_mestra or chave_recebida != chave_mestra:
        raise HTTPException(status_code=403, detail="Acesso negado. Chave de API inválida.")
    return chave_recebida

# ==========================================
# 2. MODELOS DE DADOS
# ==========================================
class LancarNotasRequest(BaseModel):
    turma: str
    descricao_avaliacao: str
    notas_json: dict
    periodo: str = "268"  # Agora usamos o ID numérico padrão do período

class CriarAvaliacaoRequest(BaseModel):
    turma: str
    num_tvc: int
    peso: float
    data: str
    descricao: str
    periodo: str = "268"

# ==========================================
# 3. ROTAS DA API
# ==========================================
@app.post("/api/lancar-notas")
def api_lancar_notas(req: LancarNotasRequest, api_key: str = Depends(validar_api_key)):
    cpf_siga = os.getenv("SIGA_CPF")
    senha_siga = os.getenv("SIGA_SENHA")

    if not cpf_siga or not senha_siga:
        raise HTTPException(status_code=500, detail="Credenciais ausentes no Coolify.")

    siga = SigaAPI() 
    try:
        siga.login(cpf=cpf_siga, senha=senha_siga)
        siga.lancar_notas(
            turma=req.turma,
            descricao_avaliacao=req.descricao_avaliacao,
            notas_json=req.notas_json,
            periodo=req.periodo
        )
        return {"status": "sucesso", "mensagem": f"Notas lançadas na turma {req.turma}"}
    except Exception:
        erro = traceback.format_exc()
        print(erro)
        raise HTTPException(status_code=500, detail=erro)
    finally:
        siga.fechar()

@app.post("/api/criar-avaliacao")
def api_criar_avaliacao(req: CriarAvaliacaoRequest, api_key: str = Depends(validar_api_key)):
    cpf_siga = os.getenv("SIGA_CPF")
    senha_siga = os.getenv("SIGA_SENHA")

    if not cpf_siga or not senha_siga:
        raise HTTPException(status_code=500, detail="Credenciais ausentes no Coolify.")

    siga = SigaAPI()
    try:
        siga.login(cpf=cpf_siga, senha=senha_siga)
        siga.criar_avaliacao(
            turma=req.turma,
            num_tvc=req.num_tvc,
            peso=req.peso,
            data=req.data,
            descricao=req.descricao,
            periodo=req.periodo
        )
        return {"status": "sucesso", "mensagem": f"Avaliação '{req.descricao}' criada."}
    except Exception:
        erro = traceback.format_exc()
        print(erro)
        raise HTTPException(status_code=500, detail=erro)
    finally:
        siga.fechar()
