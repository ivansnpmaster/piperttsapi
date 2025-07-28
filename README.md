# 🗣️ Piper TTS API

Uma API Flask simples para conversão de texto em áudio (text-to-speech), usando o mecanismo **[Piper TTS](https://github.com/rhasspy/piper)** com modelos locais em ONNX.

Ideal para uso em aplicações web, automação ou bots — e pode ser facilmente implantada no [Railway](https://railway.app), Render, Heroku ou outros serviços.

---

## 🚀 Como usar

### 1. Clone o projeto

```bash
git clone https://github.com/ivansnpmaster/piperttsapi
cd piperttsapi
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Adicione modelos de voz Piper

Coloque os modelos `.onnx` e `.onnx.json` em uma subpasta dentro de `voices/`, caso ainda não existam. Exemplo:

```
voices/
└── pt_BR-cadu-medium/
    ├── pt_BR-cadu-medium.onnx
    └── pt_BR-cadu-medium.onnx.json
```

> Modelos disponíveis em: [huggingface.co/rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices)

---

## 📡 Endpoints disponíveis

### `GET /`
Verifica se a API está ativa.

### `GET /voices`
Retorna uma lista de vozes disponíveis (baseado nas pastas em `voices/`).

### `POST /tts`

**Corpo da requisição:**
```json
{
  "text": "Olá, tudo bem?",
  "voice": "pt_BR-cadu-medium"
}
```

**Resposta:** Arquivo `.wav` com o áudio gerado.

---

## 🛠️ Deploy no Railway

1. Crie um novo projeto no [Railway](https://railway.app).
2. Escolha **Deploy from GitHub** e selecione este repositório.
3. Railway detectará Flask automaticamente.
4. Certifique-se de ter:
   - `requirements.txt`
   - `Procfile`
   - pasta `voices/nome_modelo/` com o modelo desejado
5. A API será exposta em uma URL pública.

---

## 📄 Licença

Este projeto é distribuído sob a licença [GNU General Public License v3.0](LICENSE).

---

## Créditos e licenças de terceiros

Este projeto utiliza as seguintes bibliotecas:

-   **Flask:**: Licenciado sob a licença [BSD 3-Clause](https://github.com/pallets/flask/blob/main/LICENSE.txt).
-   **Flask-CORS:**: Licenciado sob a licença [MIT](https://github.com/corydolphin/flask-cors/blob/master/LICENSE).
-   **Piper TTS:**: Licenciado sob a licença [GNU General Public License v3.0](https://github.com/OHF-Voice/piper1-gpl/blob/main/COPYING).
