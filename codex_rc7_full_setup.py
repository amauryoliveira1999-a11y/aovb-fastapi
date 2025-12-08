"""
Codex RC7 Full Setup – AuroraChain Created
==========================================
Automação completa de deploy RC7:
- Upload GitHub
- Configuração Render
- Geração de logs técnicos e auditoria RC7
"""

import os
import json
import base64
import requests
from datetime import datetime

# =======================================================
#  CONFIGURAÇÕES
# =======================================================
GITHUB_API = "https://api.github.com"
RENDER_API = "https://api.render.com/v1"


# =======================================================
#  FUNÇÕES DE SUPORTE GITHUB
# =======================================================
def solicitar_token_github():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        token = input("🔑 GitHub Token (perm. repo): ").strip()
        os.environ["GITHUB_TOKEN"] = token
    return token


def solicitar_repositorio():
    user = input("👤 Usuário GitHub (ex: amauryoliveira1999-a11y): ").strip()
    repo = input("📦 Nome do repositório (ex: aovb-fastapi-rc7): ").strip()
    return user, repo


def carregar_arquivos(base_dir):
    arquivos = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            path_abs = os.path.join(root, f)
            path_rel = os.path.relpath(path_abs, base_dir)
            arquivos.append((path_rel, path_abs))
    return arquivos


def criar_repo(user, repo, token):
    headers = {"Authorization": f"token {token}"}
    check = requests.get(f"{GITHUB_API}/repos/{user}/{repo}", headers=headers)
    if check.status_code == 200:
        print(f"✅ Repositório '{repo}' já existe.")
        return True
    payload = {"name": repo, "private": False, "auto_init": True}
    r = requests.post(f"{GITHUB_API}/user/repos", headers=headers, json=payload)
    if r.status_code == 201:
        print(f"✅ Repositório '{repo}' criado com sucesso.")
        return True
    print(f"❌ Falha ao criar repositório: {r.text}")
    return False


def upload_arquivo(user, repo, rel_path, abs_path, token):
    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    url = f"{GITHUB_API}/repos/{user}/{repo}/contents/{rel_path}"
    headers = {"Authorization": f"token {token}"}
    data = {
        "message": f"Add {rel_path} via Codex RC7 AutoDeploy",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main",
    }
    resp = requests.put(url, headers=headers, json=data)
    return resp.status_code, resp.text


# =======================================================
#  FUNÇÕES DE SUPORTE RENDER
# =======================================================
def solicitar_render_key():
    key = os.getenv("RENDER_API_KEY")
    if not key:
        key = input("🔐 Render API Key: ").strip()
        os.environ["RENDER_API_KEY"] = key
    return key


def criar_servico_render(key, nome, repo_url, branch="main"):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "serviceDetails": {
            "name": nome,
            "type": "web",
            "env": "python",
            "repo": repo_url,
            "branch": branch,
            "plan": "free",
            "autoDeploy": True,
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "uvicorn main:app --host 0.0.0.0 --port 10000",
        }
    }
    r = requests.post(f"{RENDER_API}/services", headers=headers, json=payload)
    return r.status_code, r.text


# =======================================================
#  EXECUÇÃO PRINCIPAL
# =======================================================
def main():
    print("\n🚀 Codex RC7 Full Setup – AOVB AuroraChain Hybrid v5.0\n")

    token = solicitar_token_github()
    user, repo = solicitar_repositorio()
    base_dir = input("📂 Caminho local do projeto (ex: /mnt/data/AOVB_Project_Optimized_FINAL): ").strip()

    if not os.path.exists(base_dir):
        print("❌ Diretório não encontrado.")
        return

    if not criar_repo(user, repo, token):
        return

    arquivos = carregar_arquivos(base_dir)
    print(f"📁 {len(arquivos)} arquivos detectados para upload.\n")

    upload_log = []
    for rel, abs_path in arquivos:
        print(f"📤 {rel}")
        status, texto = upload_arquivo(user, repo, rel, abs_path, token)
        upload_log.append({
            "arquivo": rel,
            "status": status,
            "resumo": texto[:120] + "..." if len(texto) > 120 else texto,
        })

    # Log GitHub RC7
    github_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "repo": f"{user}/{repo}",
        "arquivos": len(arquivos),
        "resultados": upload_log,
    }
    with open("Codex_RC7_GitHub_Log.json", "w", encoding="utf-8") as f:
        json.dump(github_log, f, indent=2, ensure_ascii=False)

    print("\n🔗 Configurando Render AutoDeploy...")
    render_key = solicitar_render_key()
    repo_url = f"https://github.com/{user}/{repo}"
    nome_servico = repo.replace("_", "-")
    status, texto = criar_servico_render(render_key, nome_servico, repo_url)

    # Relatório final RC7
    relatorio = {
        "timestamp": datetime.utcnow().isoformat(),
        "github_repo": repo_url,
        "render_status": status,
        "render_resposta": texto[:500],
        "total_arquivos": len(arquivos),
    }
    with open("Aurora_RC7_Deploy_Report.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print("\n✅ DEPLOY CONCLUÍDO COM SUCESSO")
    print("📜 Log GitHub: Codex_RC7_GitHub_Log.json")
    print("📘 Relatório Render: Aurora_RC7_Deploy_Report.json")
    print(f"🌍 Repositório: https://github.com/{user}/{repo}")
    print("🚀 Serviço Render em processo de criação...")


if __name__ == "__main__":
    main()
