import os, json

def gerar_dashboard_html():
    """
    Consome as métricas do Apolo e gera uma página HTML estática leve
    que pode ser publicada no GitHub Pages como Status Page corporativa.
    """
    metricas_path = "modulo_4_apolo/apolo_metrics.json"
    dados = {}
    if os.path.exists(metricas_path):
        try:
            with open(metricas_path, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except Exception:
            pass

    cliente = dados.get("cliente", "Geral")
    timestamp = dados.get("timestamp", "N/A")
    tempo = dados.get("tempo_execucao_segundos", 0)
    status = dados.get("status_geral", "OPERACIONAL")

    html_content = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Olimpo AI — Enterprise Status Page</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 40px; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 24px; max-width: 600px; margin: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
        h1 {{ color: #58a6ff; font-size: 24px; margin-top: 0; }}
        .badge {{ background: #238636; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 14px; }}
        .metric-row {{ display: flex; justify-content: space-between; margin: 12px 0; border-bottom: 1px solid #30363d; padding-bottom: 8px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #8b949e; text-align: center; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🏛️ Olimpo AI — Status Corporativo</h1>
        <div class="metric-row">
            <span>Cliente / Tenant:</span>
            <strong>{cliente}</strong>
        </div>
        <div class="metric-row">
            <span>Estado da Ronda:</span>
            <span class="badge">{status}</span>
        </div>
        <div class="metric-row">
            <span>Última Execução (Cloud):</span>
            <span>{timestamp}</span>
        </div>
        <div class="metric-row">
            <span>Duração do Ciclo:</span>
            <span>{tempo} segundos</span>
        </div>
        <div class="footer">Gerado autonomamente pelo Módulo Apolo • 24/7 Cloud Engine</div>
    </div>
</body>
</html>
"""
    os.makedirs("modulo_4_apolo/dashboard", exist_ok=True)
    with open("modulo_4_apolo/dashboard/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("[APOLO DASHBOARD] Página de status HTML gerada com sucesso em 'modulo_4_apolo/dashboard/index.html'.")

if __name__ == "__main__":
    gerar_dashboard_html()
