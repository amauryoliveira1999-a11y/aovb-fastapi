# Plano de verificação técnica – Aurora RC7 / AOVB Connect

Este roteiro reproduz os 8 questionamentos técnicos solicitados, com comandos e expectativas para validar o projeto localmente ou em um deploy Render.

## 1. Estrutura do projeto
- **Objetivo:** confirmar a estrutura básica de um app FastAPI pronto para deploy.
- **Como testar:**
  ```bash
  tree . -L 2
  ```
- **Esperado:** presença de `main.py`, pastas `templates/` e `static/`, além de `requirements.txt`, `render.yaml`, `memory_manager.py` e `drive_connector.py`.

## 2. Configuração do FastAPI (`main.py`)
- **Objetivo:** garantir que a instância `app = FastAPI()` está no escopo global e as rotas não dependem de `if __name__ == "__main__"`.
- **Como testar:** abrir `main.py` e verificar:
  - Import de `FastAPI` e rotas decoradas com `@app.get`/`@app.post`.
  - Montagem de estáticos e templates (`StaticFiles`, `Jinja2Templates`).
  - Rotas de painel (`/panel`), memória (`/memory/*`) e sincronização (`/drive/sync`).

## 3. Dependências (`requirements.txt`)
- **Objetivo:** checar bibliotecas mínimas para FastAPI com formulários e templates.
- **Como testar:**
  ```bash
  pip install -r requirements.txt
  ```
- **Esperado:** instalação sem erros das libs `fastapi`, `uvicorn`, `jinja2`, `pydantic` e `python-multipart`.

## 4. Configuração de deploy Render (`render.yaml`)
- **Objetivo:** confirmar comando de build/start compatível com Render.
- **Como testar:** revisar `render.yaml` e observar:
  ```yaml
  type: web
  env: python
  buildCommand: pip install -r requirements.txt
  startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
  ```
- **Esperado:** logs de deploy no Render concluindo com sucesso e aplicação acessível na URL fornecida pelo serviço.

## 5. Painel web e templates
- **Objetivo:** validar renderização do `panel.html` com CSS de `static/`.
- **Como testar:** iniciar o app (passo 7) e acessar `http://localhost:8000/panel`.
- **Esperado:** página com formulário de memórias e listagem das memórias existentes, estilizada pelo `style.css`.

## 6. Memória e conexões (`memory_manager.py`, `drive_connector.py`)
- **Objetivo:** garantir que memórias são persistidas e sincronizadas (modo de teste) com Drive.
- **Como testar:**
  ```bash
  curl -X POST http://localhost:8000/memory/store -d "entry=Teste"
  curl http://localhost:8000/memory/retrieve
  ```
- **Esperado:** retorno contendo a entrada recém-adicionada; sincronização simulada registrada nos logs.

## 7. Execução local
- **Objetivo:** validar execução sem erros em ambiente local.
- **Como testar:**
  ```bash
  uvicorn main:app --reload
  ```
- **Esperado:**
  - `http://127.0.0.1:8000/` retorna o status JSON da API.
  - `http://127.0.0.1:8000/panel` exibe o painel.

## 8. Boas práticas e conformidade geral
- **Objetivo:** revisar organização, segurança e legibilidade.
- **Checklist sugerida:**
  - `memory.json` ignorado no controle de versão (.gitignore).
  - Variáveis sensíveis em `.env` (quando necessário).
  - Logs informativos no ciclo principal (status, renderização, sincronização).
  - Código modular nas classes `MemoryManager` e `DriveConnector`.

---
Siga os passos na ordem para reproduzir a análise completa. Cada item foi alinhado ao estado atual do projeto para facilitar a verificação em pipelines locais ou no Render.
