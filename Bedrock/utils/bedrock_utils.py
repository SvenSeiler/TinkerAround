# bedrock_utils.py
import boto3, json
from typing import List, Dict, Optional
DEFAULT_REGION = "eu-central-1" 

# ------------------------------------------------------------
# Modelle auflisten
# ------------------------------------------------------------
def list_bedrock_models(
    region: Optional[str] = None,
    provider: Optional[str] = None,
    print_json: bool = False
) -> List[Dict]:
    br = boto3.client("bedrock", region_name=region) if region else boto3.client("bedrock")
    models = br.list_foundation_models()["modelSummaries"]

    if provider:
        models = [m for m in models if m["providerName"].lower() == provider.lower()]

    if print_json:
        print(json.dumps(models, indent=2, ensure_ascii=False))

    return models


# ------------------------------------------------------------
# Prompt senden und Antwort zurückgeben
# ------------------------------------------------------------
def invoke_bedrock_prompt(
    prompt: str,
    model_id: str = "amazon.titan-text-express-v1",
    region: Optional[str] = DEFAULT_REGION,
    max_tokens: int = 512,
    temperature: float = 0.5,
) -> str:
    """
    Sendet einen Prompt an das angegebene Bedrock-Modell
    und liefert den generierten Text.

    Unterstützt aktuell Titan-Text und Anthropic Claude.
    """
    brt = boto3.client("bedrock-runtime", region_name=region) if region else boto3.client("bedrock-runtime")

    # --- Modell-spezifische Payload -------------------------------------------------
    if model_id.startswith("amazon.titan"):
        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                "topP": 0.9
            }
        }
    elif model_id.startswith("anthropic"):
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                { "role": "user", "content": prompt }
            ]
        }
    else:
        raise ValueError("Aktuell sind nur Titan- und Anthropic-Modelle abgedeckt.")

    # --- Aufruf --------------------------------------------------------------------
    response = brt.invoke_model(
        modelId    = model_id,
        body       = json.dumps(payload),
        contentType = "application/json",
        accept      = "application/json"
    )

    body = json.loads(response["body"].read())

    # --- Antwort extrahieren --------------------------------------------------------
    if model_id.startswith("amazon.titan"):
        return body["results"][0]["outputText"]
    else:                              # Anthropic
        return body["content"][0]["text"]


# -----------------------------------------------------------------------
# Kleiner Selbsttest bei direktem Aufruf  ->  python bedrock_utils.py
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("Verfügbare Amazon-Modelle:")
    list_bedrock_models(provider="amazon", print_json=True)

    print("\nBeispiel-Antwort:")
    text = invoke_bedrock_prompt(
        prompt="Erkläre 'Hello World' in einem Satz.",
        model_id = "amazon.titan-text-express-v1",
    )
    print(text)
