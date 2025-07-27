import os
import io
import wave
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from piper import PiperVoice

app = Flask(__name__)
CORS(app)

voice_cache = {}

# A função load_voice e a rota /voices permanecem as mesmas
def load_voice(voice_name):
    if voice_name in voice_cache:
        print(f"[load_voice] Voz '{voice_name}' carregada do cache.")
        return voice_cache[voice_name]

    model_dir = os.path.join("voices", voice_name)
    model_path = os.path.join(model_dir, f"{voice_name}.onnx")
    config_path = os.path.join(model_dir, f"{voice_name}.onnx.json")

    print(f"[load_voice] Tentando carregar modelo da voz '{voice_name}':")
    print(f"  - Modelo ONNX: {model_path}")
    print(f"  - Config JSON: {config_path}")

    if not os.path.exists(model_path):
        msg = f"Arquivo de modelo ONNX não encontrado: {model_path}"
        print(f"[load_voice] ERRO: {msg}")
        raise FileNotFoundError(msg)

    voice = PiperVoice.load(model_path, config_path=config_path)
    voice_cache[voice_name] = voice
    print(f"[load_voice] Voz '{voice_name}' carregada com sucesso.")
    return voice

@app.route("/", methods=["GET"])
def health_check():
    """Retorna apenas o status HTTP 204 para indicar que a API está ativa."""
    return '', 204

@app.route("/voices", methods=["GET"])
def list_voices():
    try:
        voices = []
        base_dir = "voices"
        if not os.path.exists(base_dir):
            return jsonify([])

        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                model_file = os.path.join(folder_path, f"{folder}.onnx")
                if os.path.exists(model_file):
                    voices.append(folder)
        return jsonify(voices)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Erro interno ao listar vozes"}), 500


@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.json
        text = data.get("text")
        voice_name = data.get("voice")

        if not text or not voice_name:
            return jsonify({"error": "Parâmetros 'text' e 'voice' são obrigatórios."}), 400

        print(f"[tts] Gerando áudio para texto: '{text}' com voz: '{voice_name}'")
        voice = load_voice(voice_name)

        audio_generator = voice.synthesize(text)

        # 1. Consumir todo o gerador em uma lista de AudioChunks.
        all_chunks = list(audio_generator)

        # 2. ##-- MUDANÇA AQUI --##
        #    Se nenhum chunk de áudio for gerado, retorne um erro claro.
        if not all_chunks:
            msg = "Não foi possível gerar áudio para o texto fornecido. O texto pode ser inválido, muito curto ou conter apenas caracteres não suportados."
            print(f"[tts] ERRO: {msg}")
            return jsonify({"error": msg}), 400

        # 3. Pegar o primeiro chunk para extrair os parâmetros do WAV.
        first_chunk = all_chunks[0]
        num_channels = first_chunk.sample_channels
        sample_width = first_chunk.sample_width
        sample_rate = first_chunk.sample_rate
        print(f"[tts] Parâmetros do áudio obtidos do AudioChunk: Canais={num_channels}, Largura={sample_width}, Taxa={sample_rate}")

        # 4. Juntar os bytes de áudio de TODOS os chunks.
        audio_bytes = b"".join(chunk.audio_int16_bytes for chunk in all_chunks)
        print(f"[tts] Áudio bruto consumido com sucesso: {len(audio_bytes)} bytes")

        # 5. Construir o arquivo WAV em memória usando os parâmetros corretos.
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(num_channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_bytes)

        wav_io.seek(0)
        print("[tts] Arquivo WAV criado em memória com sucesso.")

        return send_file(
            wav_io,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="audio.wav"
        )

    except FileNotFoundError as e:
        print(f"[tts] ERRO: Voz não encontrada - {e}")
        return jsonify({"error": f"A voz '{voice_name}' não foi encontrada no servidor."}), 404
    except Exception as e:
        print("[tts] ERRO durante síntese:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("API iniciada - ouvindo na porta 5000")
    app.run(host="0.0.0.0", port=5000)