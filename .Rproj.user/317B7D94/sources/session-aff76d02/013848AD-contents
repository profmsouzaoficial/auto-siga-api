import requests
from bs4 import BeautifulSoup
import re

class SigaAPI:
    def __init__(self):
        self.session = requests.Session()
        # Disfarçamos o Python de Google Chrome do Linux, exatamente como você capturou
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive"
        })
        self.logado = False

    def login(self, cpf: str, senha: str):
        print("Iniciando login HTTP direto...")
        
        # 1. Acedemos DIRETAMENTE ao portal de autenticação da UFJF (saltando redirecionamentos de JS).
        # O parâmetro 'service' avisa a UFJF para nos devolver ao SIGA após o login.
        url_auth = "https://auth.ufjf.br/login?service=https%3A%2F%2Fsiga.ufjf.br%2Findex.php"
        res_login_page = self.session.get(url_auth)
        
        # 2. Inspeciona a página real de login para roubar os tokens
        soup_login = BeautifulSoup(res_login_page.text, "html.parser")
        form_login = soup_login.find("form")
        
        if not form_login:
            # Se ainda assim não achar, imprimimos o que o servidor devolveu para não lutarmos às cegas
            raise Exception("Formulário de autenticação não encontrado. O servidor respondeu:\n" + res_login_page.text[:500])
            
        payload_login = {}
        # Varre e guarda todos os inputs invisíveis de segurança gerados pela UFJF (ex: execution, _eventId)
        for input_tag in form_login.find_all("input"):
            nome = input_tag.get("name")
            valor = input_tag.get("value", "")
            if nome:
                payload_login[nome] = valor
                
        # 3. Injeta as suas credenciais no meio dos tokens capturados
        payload_login["username"] = cpf
        payload_login["password"] = senha
        
        # 4. Descobre a URL exata para onde o formulário deve ser enviado (action)
        action = form_login.get("action")
        if action:
            post_url = action if action.startswith("http") else "https://auth.ufjf.br" + action
        else:
            post_url = res_login_page.url
            
        # 5. Dispara as credenciais. A UFJF validará e fará um Redirecionamento 302 de volta para o SIGA.
        # O self.session segue automaticamente, recebendo os Cookies finais.
        self.session.post(post_url, data=payload_login)
        
        # 6. Força a atualização da página no painel acadêmico
        res_painel = self.session.get("https://siga.ufjf.br/index.php")
        
        if "Professor" in res_painel.text or "Siga" in res_painel.text:
            print("Login bem-sucedido! Tokens contornados e cookies capturados.")
            self.logado = True
        else:
            raise Exception("Falha de autenticação. Os tokens foram enviados, mas a UFJF rejeitou as credenciais.")

    def _obter_id_turma(self, turma_codigo: str, periodo: str) -> str:
        """
        Faz um POST direto no motor de busca do SIGA pedindo as turmas 
        específicas do seu ID de Docente no período selecionado.
        """
        url_busca = "https://siga.ufjf.br/index.php/siga/academico/nota/formNotaParcialPasso2"
        
        # O Payload milagroso capturado na sua engenharia reversa
        payload_busca = {
            "__LAYOUT": "default",
            "__ELEMENT": "centerPane",
            "__TEMPLATE": "base",
            "__ISFILEUPLOAD": "no",
            "__ISAJAXEVENT": "no",
            "__EVENTTARGET": "btnPost",
            "filter::idPeriodoLetivo": periodo,
            "filter::idDocente": "29230",  # O seu ID interno de Professor na UFJF!
            "ajaxResponseType": "json"
        }
        
        # Cabeçalhos para o SIGA achar que somos um formulário AJAX do navegador
        headers_ajax = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://siga.ufjf.br/index.php/siga/academico/nota/formNotaParcialPasso1/docente"
        }
        
        print(f"Pesquisando turmas do professor (ID 29230) no período {periodo}...")
        res_turmas = self.session.post(url_busca, data=payload_busca, headers=headers_ajax)
        
        # Decodifica possíveis retornos em JSON do Dojo Toolkit
        texto_html = res_turmas.text
        try:
            import json
            dados_json = res_turmas.json()
            texto_html = json.dumps(dados_json) # Transforma o JSON de volta em texto para o BeautifulSoup ler as tags
        except:
            pass
            
        soup = BeautifulSoup(texto_html, "html.parser")
        
        # Procura a string da turma (ex: "CBV018GV-A") no código retornado
        elemento_turma = soup.find(string=re.compile(turma_codigo))
        
        if not elemento_turma:
            raise Exception(f"Turma {turma_codigo} não encontrada na resposta do servidor para o período {periodo}.")
            
        # Sobe na estrutura HTML até achar a linha (<tr>) e o botão "Editar" que esconde o ID da turma
        linha = elemento_turma.find_parent("tr")
        if not linha:
            raise Exception("Turma encontrada, mas falha ao mapear a tabela HTML.")
            
        link_editar = linha.find("a", href=re.compile(r"formNotaParcialObject"))
        if link_editar and "href" in link_editar.attrs:
            url_destino = link_editar["href"]
            # Corta a URL para sobrar apenas o número (ex: 1248384)
            id_turma = url_destino.split("formNotaParcialObject/")[-1].split("?")[0].strip("/")
            return id_turma
            
        raise Exception("Botão de 'Editar' da turma não encontrado na tabela.")

    def criar_avaliacao(self, turma: str, num_tvc: int, peso: float, data: str, descricao: str, periodo: str = "268"):
        """
        Cria a TVC disparando os headers e payloads exatos que capturámos no F12.
        Nota: 'periodo' no SIGA geralmente é um ID (268) e não o texto (2026/3).
        """
        if not self.logado:
            raise Exception("Erro: Você precisa fazer o login primeiro.")
            
        print(f"Buscando ID interno da turma {turma}...")
        id_turma = self._obter_id_turma(turma_codigo=turma, periodo=periodo)
        print(f"ID da Turma capturado: {id_turma}")

        # Preparação do "míssil" de acordo com o seu print do Payload
        url_alvo = "https://siga.ufjf.br/index.php/siga/academico/nota/TVCSave/?go=formTVCFind"
        
        headers_especificos = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://siga.ufjf.br/index.php/siga/academico/nota/formNotaParcialObject/{id_turma}?filter::idDepartamento="
        }
        
        # A "Fórmula Secreta" que copiámos da sua imagem
        payload = {
            "__LAYOUT": "default",
            "__ELEMENT": "dialog",
            "__TEMPLATE": "base",
            "__ISFILEUPLOAD": "no",
            "__ISAJAXEVENT": "no",
            "__EVENTTARGET": "btnPostTvc",
            "turma::tipoCalculo": "Soma",
            "tvc::numTVC": str(num_tvc),
            "tvc::peso": str(peso),
            "tvc::dataAplicacao": data,
            "tvc::descricao": descricao,
            "tvc::idTVC": "", # Vazio porque estamos a criar um novo
            "tvc::idTurma": id_turma,
            "ajaxResponseType": "json"
        }

        print("Disparando requisição POST para salvar a avaliação...")
        resposta = self.session.post(url_alvo, data=payload, headers=headers_especificos)
        
        if resposta.status_code == 200:
            print(f"Sucesso Instantâneo! Avaliação '{descricao}' criada na turma {turma}.")
        else:
            raise Exception(f"Erro ao salvar: {resposta.status_code} - {resposta.text}")
            
    def fechar(self):
        # A API HTTP fecha automaticamente, não há navegadores a prender a memória.
        self.session.close()
