"""
REST API for BLINK

to run: `python api.py`
"""

# blink
import blink.main_dense as main_dense
import argparse

# fastapi
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import List
import numpy as np
import requests

app = FastAPI()

class Item(BaseModel):
    uid: int
    text: str

class ItemList(BaseModel):
    items: List[Item]


# set global variables: initialised during startup and then used for API calls
global_vars = {}

@app.on_event("startup")
async def startup():
    models_path = "models/" # the path where you stored the BLINK models

    config = {
        "test_entities": None,
        "test_mentions": None,
        "interactive": False,
        "top_k": 10,
        "biencoder_model": models_path+"biencoder_wiki_large.bin",
        "biencoder_config": models_path+"biencoder_wiki_large.json",
        "entity_catalogue": models_path+"entity.jsonl",
        "entity_encoding": models_path+"all_entities_large.t7",
        "crossencoder_model": models_path+"crossencoder_wiki_large.bin",
        "crossencoder_config": models_path+"crossencoder_wiki_large.json",
        "fast": True, # set this to be true if speed is a concern
        "output_path": "logs/" # logging directory
    }

    global_vars['args'] = [argparse.Namespace(**config)]

    print("Loading models...")
    global_vars['models'] = [main_dense.load_models(global_vars['args'][0], logger=None)]

def convert_item_to_blink_input(item: Item) -> dict:
    return {
        "id": item.uid,
        "label": "unknown",
        "label_id": -1,
        "context_left": item.text.split("[[")[0].lower(),
        "mention": item.text.split("[[")[1].split("]]")[0].lower(),
        "context_right": item.text.split("]]")[1].lower(),
    }

def convert_items_to_blink_inputs(items: ItemList) -> List[dict]:
    """
    Input:
    [
        {"uid": 2, "text": ""}, ...
    ]

    Output:
    [{
        "id": 2,
        "label": "unknown",
        "label_id": -1,
        "context_left": "".lower(),
        "mention": "First World War".lower(),
        "context_right": " dressing, treated with cyanide, German".lower(),
    }, ...]
    """
    outputs = []

    for item in items:
        outputs.append(convert_item_to_blink_input(item))

    return outputs

def wikipedia_id_to_url(wiki_id: str):
    """Convert a wikipedia title as outputted by BLINK to a wikipedia URL"""

    return f"https://en.wikipedia.org/wiki/{'_'.join(wiki_id.split(' '))}"

def create_response_from_predictions_and_scores(predictions: List[list], scores: List[np.ndarray]) -> List[List[tuple]]:
    response = []

    for i in range(len(predictions)):
        item_preds = predictions[i]
        item_scores = scores[i]
    
        item_preds_and_scores = [(item_preds[idx], wikipedia_id_to_url(item_preds[idx]), item_scores[idx].tolist()) for idx in range(len(item_preds))]
        response.append(item_preds_and_scores)

    return response

@app.get("/blink/multiple")
async def blink(items: ItemList):
    processed_items = convert_items_to_blink_inputs(items.items)

    print(f"Making {len(processed_items)} predictions...")
    models = global_vars['models'][0]
    _, _, _, _, _, predictions, scores, = main_dense.run(global_vars['args'][0], None, *models, test_data=processed_items)

    return create_response_from_predictions_and_scores(predictions, scores)

@app.get("/blink/single")
async def blink(item: Item):
    processed_item = convert_item_to_blink_input(item)

    # print(f"Making {len(processed_items)} predictions...")
    models = global_vars['models'][0]
    _, _, _, _, _, predictions, scores = main_dense.run(global_vars['args'][0], None, *models, test_data=[processed_item])

    return create_response_from_predictions_and_scores(predictions, scores)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)