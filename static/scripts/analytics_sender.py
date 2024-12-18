import time
import requests
import random


# Função para simular as visitas no Google Analytics G4
def send_to_google_analytics(url, palavras_chave, localizacao, visitas_diarias, tempo_visita, measurement_id):
    print(f"Iniciando envio de visitas simuladas para {url}...")

    for _ in range(visitas_diarias):
        # Simula o envio de eventos ao Google Analytics
        payload = {
            "client_id": f"{random.randint(100000, 999999)}.{random.randint(1000000000, 9999999999)}",
            "events": [{
                "name": "page_view",
                "params": {
                    "page_location": url,
                    "page_title": palavras_chave,
                    "location": localizacao
                }
            }]
        }

        # Endpoint do Google Analytics G4
        endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret=YOUR_API_SECRET"

        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 204:
                print("Visita enviada com sucesso!")
            else:
                print(f"Erro ao enviar visita: {response.text}")
        except Exception as e:
            print(f"Erro durante envio: {e}")

        time.sleep(tempo_visita / 60)  # Intervalo baseado no tempo de visita

    print("Envio de visitas concluído!")
