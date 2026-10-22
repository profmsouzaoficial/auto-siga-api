# 🚀 AUTO-SIGA-API (UFJF)

Uma API não oficial, ultrarrápida e baseada em requisições HTTP diretas para automatizar a gestão de turmas, criação de avaliações e lançamento de notas no SIGA da Universidade Federal de Juiz de Fora (UFJF).

Desenvolvido para eliminar o trabalho manual e repetitivo dos docentes, permitindo a integração do SIGA com ferramentas de automação (n8n, Make, Chatbots) ou painéis personalizados.

## ⚠️ Aviso Legal e Administrativo (Disclaimer)
**Este é um projeto open-source independente e não oficial.** 
Não possui qualquer vínculo com o CGCO, com a administração da UFJF ou com a empresa desenvolvedora do SIGA. O código foi desenvolvido estritamente para fins de pesquisa e automação pessoal. 
**Segurança:** A execução deste código e o tráfego de credenciais federais (CPF e Senha) são de inteira e exclusiva responsabilidade do utilizador que clonar e hospedar esta API. Nunca compartilhe a sua instância hospedada com terceiros para evitar infrações à LGPD ou bloqueios por parte do firewall da instituição.

---

## ✨ CPrincipais Características
- **Velocidade Extrema:** Não utiliza navegadores virtuais (Playwright/Selenium). Toda a navegação é feita via `requests` e `BeautifulSoup`, reduzindo o tempo de operação de ~60 segundos para **1 a 2 segundos**.
- **Segurança de Acesso:** Protegido por uma chave API customizada (`X-API-Key`) exigida no cabeçalho (Header) das requisições.

---

## 🛠️ Como Instalar e Rodar Localmente

### 1. Clonar o repositório e preparar o ambiente
```bash
git clone https://github.com/profmsouzaoficial/auto-siga-api.git
cd auto-siga-api
```

### 2. Configurar as Variáveis de Ambiente
Na raiz do projeto, faça uma cópia do arquivo de exemplo `.env.example` e renomeie-o para `.env`. Preencha com as suas credenciais reais:
```env
SIGA_CPF=12345678900
SIGA_SENHA=SuaSenhaSecreta
API_SECRET_KEY=SuaChaveDeAPI_ParaProtegerORoteador
```
*(Nota: O arquivo `.env` está ignorado no `.gitignore` para nunca ser enviado acidentalmente para o GitHub).*

### 3. Opção A: Rodar via Python (Uvicorn)
Requer [Python 3.9+](https://www.python.org/).
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Opção B: Rodar via Docker (Recomendado)
```bash
docker build -t auto-siga-api .
docker run -p 8000:8000 --env-file .env auto-siga-api
```

---

## 📖 Como Usar (Endpoints)

Após iniciar o servidor, acesse a documentação interativa do Swagger no seu navegador:
👉 **`http://localhost:8000/docs`**

Para utilizar as rotas, deve autenticar-se no botão **Authorize** usando a sua `API_SECRET_KEY`.

### 1. Criar Avaliação (TVC)
`POST /api/criar-avaliacao`

**Exemplo de Payload (JSON):**
```json
{
  "turma": "CBV018GV-A",
  "num_tvc": 4,
  "peso": 10.0,
  "data": "30/10/2026",
  "descricao": "Trabalho Prático",
  "periodo": "2026/3"
}
```

### 2. Lançar Notas
`POST /api/lancar-notas`

**Exemplo de Payload (JSON):**
```json
{
  "turma": "CBV018GV-A",
  "descricao_avaliacao": "Trabalho Prático",
  "notas_json": {
    "202165001": 8.5,
    "202033002": 9.0,
    "202288003": 10.0
  },
  "periodo": "2026/3"
}
```
*(As chaves do objeto `notas_json` devem ser as matrículas reais dos alunos).*

---

## 🤝 Contribuição
Contribuições são muito bem-vindas! Se você mapeou novas rotas do SIGA (como lançamento de frequência, retificação de notas ou geração de pautas em PDF), sinta-se à vontade para abrir um *Pull Request* ou reportar nas *Issues*.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.