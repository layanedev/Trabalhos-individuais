from flask import Flask, render_template, jsonify, request, Response
import json
from datetime import datetime, timezone

app = Flask(__name__)


@app.get("/")
def index():
    """Abre a interface principal do raiz."""
    return render_template("index.html")


@app.get("/api/status")
def status():
    """Verifica se o servidor está funcionando."""
    return jsonify({
        "app": "raiz",
        "status": "online",
        "servidor": "Flask"
    })


@app.post("/api/backup")
def receber_backup():
    """Recebe um JSON enviado pelo aplicativo."""
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um objeto JSON válido."
        }), 400

    conteudo = json.dumps(
        dados,
        ensure_ascii=False,
        indent=2
    )

    nome = (
        "raiz-backup-"
        + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        + ".json"
    )

    return Response(
        conteudo,
        mimetype="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{nome}"'
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
