# 🚀 AUTO-SIGA-API (UFJF)

Uma API não oficial, ultrarrápida e baseada em requisições HTTP diretas para automatizar a gestão de turmas, criação de avaliações e lançamento de notas no SIGA da Universidade Federal de Juiz de Fora (UFJF).

Desenvolvido para eliminar o trabalho manual e repetitivo dos docentes, permitindo a integração do SIGA com ferramentas de automação (n8n, Make, Chatbots) ou painéis personalizados.

## ⚠️ Aviso Legal e Administrativo (Disclaimer)
**Este é um projeto open-source independente e não oficial.** 
Não possui qualquer vínculo com o CGCO, com a administração da UFJF ou com a empresa desenvolvedora do SIGA. O código foi desenvolvido estritamente para fins de pesquisa e automação pessoal. 
**Segurança:** A execução deste código e o tráfego de credenciais federais (CPF e Senha) são de inteira e exclusiva responsabilidade do utilizador que clonar e hospedar esta API. Nunca compartilhe a sua instância hospedada com terceiros para evitar infrações à LGPD ou bloqueios por parte do firewall da instituição.

---

## ✨ Características
- **Velocidade Extrema:** Não utiliza navegadores virtuais (Playwright/Selenium). Toda a navegação é feita via `requests` e `BeautifulSoup`, reduzindo o tempo de operação de ~60 segundos para **1 a 2 segundos**.
- **Tradução Dinâmica:** Capacidade de ler períodos letivos em formato humano (ex: `"2026/3"`) e encontrar automaticamente os IDs internos das turmas e avaliações.
- **Engenharia Reversa do Dojo Toolkit:** Contorna perfeitamente a proteção de tokens CSRF do `auth.ufjf.br` e interage diretamente com o banco de dados do SIGA.
- **Segurança de Acesso:** Protegido por uma chave API customizada (`X-API-Key`) exigida no cabeçalho (Header) das requisições.

---

## 🛠️ Como Instalar e Rodar Localmente

### 1. Clonar o repositório e preparar o ambiente
```bash
git clone [https://github.com/profmsouzaoficial/auto-siga-api.git](https://github.com/profmsouzaoficial/auto-siga-api.git)
cd auto-siga-api