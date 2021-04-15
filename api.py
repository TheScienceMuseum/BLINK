"""
REST API for BLINK

to run: `python api.py`
"""

# blink
import blink.main_dense as main_dense
import argparse
import torch

# fastapi
from fastapi import FastAPI
from pydantic import BaseModel, confloat, HttpUrl
import uvicorn
from typing import List, Union, Optional, Any
import numpy as np
import requests

app = FastAPI()

# ------------- DATA MODELS -------------

class WikiLink(BaseModel):
    title: str
    url: HttpUrl
    score: confloat(ge=0, le=1)
    qid: Optional[str] = None

class Item(BaseModel):
    uid: str
    metadata: Any = None
    text: str
    links: Optional[List[WikiLink]] = None

class ItemList(BaseModel):
    items: List[Item]
    threshold: Optional[confloat(ge=0, le=1)] = None

# ---------------------------------------


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
        "fast": False, # set this to be true if speed is a concern
        "output_path": "logs/" # logging directory
    }

    global_vars['args'] = argparse.Namespace(**config)

    print("Loading models...")
    global_vars['models'] = main_dense.load_models(global_vars['args'], logger=None)

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

def create_response_from_itemlist(itemlist: ItemList, predictions: List[list], scores: List[np.ndarray], threshold: Union[float, None]) -> ItemList:
    softmax = torch.nn.Softmax(dim=0)
    output_items = []

    for idx, item in enumerate(itemlist.items):
        output_item = {"uid": item.uid, "metadata": item.metadata, "text": item.text}

        item_preds = predictions[idx]
        item_scores = scores[idx]

        if global_vars['args'].fast is False:
            item_scores = softmax(torch.FloatTensor(item_scores)).tolist()
        else:
            item_scores = item_scores.tolist()

        item_links = [{"title": item_preds[idx], "url": wikipedia_id_to_url(item_preds[idx]), "score": item_scores[idx]} for idx in range(len(item_preds))]
        
        if threshold is not None:
            item_links = [i for i in item_links if i['score'] >= threshold]

        output_item['links'] = item_links
        output_items.append(output_item)

    return {
        "threshold": threshold,
        "items": output_items
    }

@app.get("/blink/multiple", response_model=ItemList)
@app.post("/blink/multiple", response_model=ItemList)
async def blink(itemlist: ItemList):
    processed_items = convert_items_to_blink_inputs(itemlist.items)
    threshold = itemlist.threshold

    print(f"Making {len(processed_items)} predictions...")
    models = global_vars['models']
    _, _, _, _, _, predictions, scores, = main_dense.run(global_vars['args'], None, *models, test_data=processed_items)

    return create_response_from_itemlist(itemlist, predictions, scores, threshold)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)