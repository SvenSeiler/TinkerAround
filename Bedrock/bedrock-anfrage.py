from utils.bedrock_utils import *

# Alle Modelle in deiner Default-Region ausgeben
#models = list_bedrock_models(print_json=True)

# Nur Amazon-Modelle in eu-central-1 abfragen
#amazon_models = list_bedrock_models(region="eu-central-1",
#                                    provider="amazon",
#                                    print_json=True)

# Ersten modelId herauspicken
#first_id = amazon_models[0]["modelId"]
#print("Erstes Amazon-Modell:", first_id)


# Anfrage an Bedrock
antwort = invoke_bedrock_prompt(
    prompt="Schreibe mir ein Haiku über das Debuggen auf Windows.",
    model_id="amazon.titan-embed-text-v2:0",
    region="eu-central-1"
)

print("Antwort des Modells:\n", antwort)