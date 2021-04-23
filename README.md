## Heritage Connector Instructions

### Setup

First, make a virtualenv

```console
# install dependencies
pip install -r requirements.txt

# download models
chmod +x download_blink_models.sh
./download_blink_models.sh

# start API server
python app.py
```

### Using the REST API
Requests can be made using GET or POST. The endpoint is `<base-url>:8000/blink/multiple`.

**<details><summary>Example request:</summary>**
Each `text` item is the source text, with separators `[ENT_START]` and `[ENT_END]` around the entity. BLINK doesn't need predicted entity labels.

Notes: 
- `id` does not have to be unique. Response items *should* be returned in the same order that they were requested.
- parameters `get_qids` (whether to fetch Wikidata QIDs) and `threshold` are optional. They default to `True` (get QIDs) and `0` (no threshold) respectively.

```json
{
    "items": [
                {
                    "id": 0, 
                    "text": "Photographs of watercolours belonging to the [ENT_START]Earl of Elgin[ENT_END], of the Elgin Railway (i) plate rails and transverse stone sleepers (ii) switch File of photographs belonging to Dendy Marshall marked BRIT [British] RAILWAYS  17th and 18th Century Stockton and Darlington Sundries",
                    "metadata": "optional_test_metadata"
                },
                {
                    "id": "values_are_converted_to_string",
                    "text": "[ENT_START]Larry J. Schaaf[ENT_END], ‘Mayall, John Jabez Edwin (1813–1901)’, Oxford Dictionary of National Biography, Oxford University Press, 2004 [http://www.oxforddnb.com/view/article/52054]; Richards, L.L.& Gill, A.T., ‘The Mayall story’, History of Photography, 9 (1985), 89–107; http://www.spartacus.schoolnet.co.uk/DSmayall.htm \n  \n Born in England, Mayall started his photographic career in America, returning to London in 1847 where he set up a photographic studio. Exhibiting at the Great Exhibition of 1851, be is best known for his photographs of Queen Victoria and the Royal Family.  He became Mayor of Brighton in 1877'}",
                    "metadata": {
                        "can": "be",
                        "any": "format"
                    }
                }

                
        ],
    "threshold": 0.8, // optional, defaults to 0
    "get_qids": true, // optional, defaults to true
}
```
</details>

**<details><summary>Example response:</summary>**
The keys of the response respond to the `id` values provided in the request.

``` json
{
    "items": [
        {
            "id": "0",
            "metadata": "test_metadata",
            "text": "Photographs of watercolours belonging to the [ENT_START]Earl of Elgin[ENT_END], of the Elgin Railway (i) plate rails and transverse stone sleepers (ii) switch File of photographs belonging to Dendy Marshall marked BRIT [British] RAILWAYS  17th and 18th Century Stockton and Darlington Sundries",
            "links": [
                {
                    "title": "Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Earl_of_Elgin",
                    "score": 0.9999476671218872,
                    "qid": null
                },
                {
                    "title": "James Bruce, 8th Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/James_Bruce,_8th_Earl_of_Elgin",
                    "score": 2.3686166969127953e-05,
                    "qid": null
                },
                {
                    "title": "Victor Bruce, 9th Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Victor_Bruce,_9th_Earl_of_Elgin",
                    "score": 2.092596514557954e-05,
                    "qid": null
                },
                {
                    "title": "Thomas Bruce, 7th Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Thomas_Bruce,_7th_Earl_of_Elgin",
                    "score": 4.30714226240525e-06,
                    "qid": null
                },
                {
                    "title": "Andrew Bruce, 11th Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Andrew_Bruce,_11th_Earl_of_Elgin",
                    "score": 1.405583020641643e-06,
                    "qid": null
                },
                {
                    "title": "Thomas Bruce, 1st Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Thomas_Bruce,_1st_Earl_of_Elgin",
                    "score": 1.0031710644398117e-06,
                    "qid": null
                },
                {
                    "title": "Charles Bruce, 5th Earl of Elgin",
                    "url": "https://en.wikipedia.org/wiki/Charles_Bruce,_5th_Earl_of_Elgin",
                    "score": 5.862896159669617e-07,
                    "qid": null
                },
                {
                    "title": "Robert Bruce, 1st Earl of Ailesbury",
                    "url": "https://en.wikipedia.org/wiki/Robert_Bruce,_1st_Earl_of_Ailesbury",
                    "score": 2.534624456984602e-07,
                    "qid": null
                },
                {
                    "title": "Thomas Bruce, 2nd Earl of Ailesbury",
                    "url": "https://en.wikipedia.org/wiki/Thomas_Bruce,_2nd_Earl_of_Ailesbury",
                    "score": 1.2343045341367542e-07,
                    "qid": null
                },
                {
                    "title": "John Scott, 1st Earl of Eldon",
                    "url": "https://en.wikipedia.org/wiki/John_Scott,_1st_Earl_of_Eldon",
                    "score": 2.3001267557276606e-09,
                    "qid": null
                }
            ]
        },
        {
            "id": "values_are_converted_to_string",
            "metadata": {
                        "can": "be",
                        "any": "format"
                    },
            "text": "[ENT_START]Larry J. Schaaf[ENT_END], ‘Mayall, John Jabez Edwin (1813–1901)’, Oxford Dictionary of National Biography, Oxford University Press, 2004 [http://www.oxforddnb.com/view/article/52054]; Richards, L.L.& Gill, A.T., ‘The Mayall story’, History of Photography, 9 (1985), 89–107; http://www.spartacus.schoolnet.co.uk/DSmayall.htm \n  \n Born in England, Mayall started his photographic career in America, returning to London in 1847 where he set up a photographic studio. Exhibiting at the Great Exhibition of 1851, be is best known for his photographs of Queen Victoria and the Royal Family.  He became Mayor of Brighton in 1877'}",
            "links": [
                {
                    "title": "Jim Schaaf",
                    "url": "https://en.wikipedia.org/wiki/Jim_Schaaf",
                    "score": 0.18495890498161316,
                    "qid": null
                },
                {
                    "title": "Joe Schaaf",
                    "url": "https://en.wikipedia.org/wiki/Joe_Schaaf",
                    "score": 0.13790211081504822,
                    "qid": null
                },
                {
                    "title": "Larry Schweikart",
                    "url": "https://en.wikipedia.org/wiki/Larry_Schweikart",
                    "score": 0.1316574066877365,
                    "qid": null
                },
                {
                    "title": "Johannes Schlaf",
                    "url": "https://en.wikipedia.org/wiki/Johannes_Schlaf",
                    "score": 0.11536765098571777,
                    "qid": null
                },
                {
                    "title": "Franklin J. Schaffner",
                    "url": "https://en.wikipedia.org/wiki/Franklin_J._Schaffner",
                    "score": 0.09967199712991714,
                    "qid": null
                },
                {
                    "title": "Daniel Pfeiffer",
                    "url": "https://en.wikipedia.org/wiki/Daniel_Pfeiffer",
                    "score": 0.0885220319032669,
                    "qid": null
                },
                {
                    "title": "James L. Kauffman",
                    "url": "https://en.wikipedia.org/wiki/James_L._Kauffman",
                    "score": 0.08521154522895813,
                    "qid": null
                },
                {
                    "title": "Bibliography of John Quincy Adams",
                    "url": "https://en.wikipedia.org/wiki/Bibliography_of_John_Quincy_Adams",
                    "score": 0.08375049382448196,
                    "qid": null
                },
                {
                    "title": "Frank J. Schlueter",
                    "url": "https://en.wikipedia.org/wiki/Frank_J._Schlueter",
                    "score": 0.038033004850149155,
                    "qid": null
                },
                {
                    "title": "Schaaf",
                    "url": "https://en.wikipedia.org/wiki/Schaaf",
                    "score": 0.03492482006549835,
                    "qid": null
                }
            ]
        }
    ],
    "threshold": 0.8
}
```
</details>

--------------------------------------------------------------------------------
![BLINK logo](./img/blink_logo_banner.png)
--------------------------------------------------------------------------------

BLINK is an Entity Linking python library that uses Wikipedia as the target knowledge base.

The process of linking entities to Wikipedia is also known as [Wikification](https://en.wikipedia.org/wiki/Wikification).


### news
- (September 2020) added [ELQ](https://github.com/facebookresearch/BLINK/tree/master/elq) - end-to-end entity linking on questions
- (3 July 2020) added [FAISS](https://github.com/facebookresearch/faiss) support in BLINK - efficient exact/approximate retrieval


## BLINK architecture

The BLINK architecture is described in the following paper:

```bibtex
@inproceedings{wu2019zero,
 title={Zero-shot Entity Linking with Dense Entity Retrieval},
 author={Ledell Wu, Fabio Petroni, Martin Josifoski, Sebastian Riedel, Luke Zettlemoyer},
 booktitle={EMNLP},
 year={2020}
}
```

[https://arxiv.org/pdf/1911.03814.pdf](https://arxiv.org/pdf/1911.03814.pdf)

In a nutshell, BLINK uses a two stages approach for entity linking, based on fine-tuned BERT architectures. In the first stage, BLINK performs retrieval in a dense space defined by a bi-encoder that independently embeds the mention context and the entity descriptions. Each candidate is then examined more carefully with a cross-encoder, that concatenates the mention and entity text. BLINK achieves state-of-the-art results on multiple datasets.


## ELQ architecture

ELQ does end-to-end entity linking on questions. The ELQ architecture is described in the following paper:

```bibtex
@inproceedings{li2020efficient,
 title={Efficient One-Pass End-to-End Entity Linking for Questions},
 author={Li, Belinda Z. and Min, Sewon and Iyer, Srinivasan and Mehdad, Yashar and Yih, Wen-tau},
 booktitle={EMNLP},
 year={2020}
}
```

[https://arxiv.org/pdf/2010.02413.pdf](https://arxiv.org/pdf/2010.02413.pdf)

For more detail on how to run ELQ, refer to the [ELQ README](https://github.com/facebookresearch/BLINK/tree/master/elq).



## Use BLINK

### 1. Create conda environment and install requirements

(optional) It might be a good idea to use a separate conda environment. It can be created by running:
```
conda create -n blink37 -y python=3.7 && conda activate blink37
pip install -r requirements.txt
```

### 2. Download the BLINK models

The BLINK pretrained models can be downloaded using the following script:
```console
chmod +x download_blink_models.sh
./download_blink_models.sh
```

We additionally provide a [FAISS](https://github.com/facebookresearch/faiss) indexer in BLINK, which enables efficient exact/approximate retrieval for biencoder model.

- [flat index](http://dl.fbaipublicfiles.com/BLINK//faiss_flat_index.pkl)
- [hnsw (approximate search) index](http://dl.fbaipublicfiles.com/BLINK/faiss_hnsw_index.pkl)


To build and save FAISS (exact search) index yourself, run
`python blink/build_faiss_index.py --output_path models/faiss_flat_index.pkl`


### 3. Use BLINK interactively
A quick way to explore the BLINK linking capabilities is through the `main_dense` interactive script. BLINK uses [Flair](https://github.com/flairNLP/flair) for Named Entity Recognition (NER) to obtain entity mentions from input text, then run entity linking. 

```console
python blink/main_dense.py -i
```

Fast mode: in the fast mode the model only uses the bi-encoder, which is much faster (accuracy drops slightly, see details in "Benchmarking BLINK" section). 

```console
python blink/main_dense.py -i --fast
```

To run BLINK with saved FAISS index, run:
```console
python blink/main_dense.py --faiss_index flat --index_path models/faiss_flat_index.pkl
```
or 
```console
python blink/main_dense.py --faiss_index hnsw --index_path models/faiss_hnsw_index.pkl
```


Example: 
```console
Bert and Ernie are two Muppets who appear together in numerous skits on the popular children's television show of the United States, Sesame Street.
```
Output:
<img align="middle" src="img/example_result_light.png" height="480">


Note: passing ```--show_url``` argument will show the Wikipedia url of each entity. The id number displayed corresponds to the order of entities in the ```entity.jsonl``` file downloaded from ```./download_models.sh``` (starts from 0). The ```entity.jsonl``` file contains information of one entity per row (includes Wikipedia url, title, text, etc.).

### 4. Use BLINK in your codebase

```console
pip install -e git+git@github.com:facebookresearch/BLINK#egg=BLINK
```

```python
import blink.main_dense as main_dense
import argparse

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

args = argparse.Namespace(**config)

models = main_dense.load_models(args, logger=None)

data_to_link = [ {
                    "id": 0,
                    "label": "unknown",
                    "label_id": -1,
                    "context_left": "".lower(),
                    "mention": "Shakespeare".lower(),
                    "context_right": "'s account of the Roman general Julius Caesar's murder by his friend Brutus is a meditation on duty.".lower(),
                },
                {
                    "id": 1,
                    "label": "unknown",
                    "label_id": -1,
                    "context_left": "Shakespeare's account of the Roman general".lower(),
                    "mention": "Julius Caesar".lower(),
                    "context_right": "'s murder by his friend Brutus is a meditation on duty.".lower(),
                }
                ]

_, _, _, _, _, predictions, scores, = main_dense.run(args, None, *models, test_data=data_to_link)

```

## Benchmarking BLINK

We provide scripts to benchmark BLINK against popular Entity Linking datasets.
Note that our scripts evaluate BLINK in a full Wikipedia setting, that is, the BLINK entity library contains all Wikipedia pages.

To benchmark BLINK run the following commands:

```console
./scripts/get_train_and_benchmark_data.sh
python scripts/create_BLINK_benchmark_data.py
python blink/run_benchmark.py
```

The following table summarizes the performance of BLINK for the considered datasets.

| dataset | biencoder accuracy (fast mode) | biencoder recall@10 | biencoder recall@30 | biencoder recall@100 | crossencoder normalized accuracy | overall unnormalized accuracy | support |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |  ------------- |  ------------- |
| AIDA-YAGO2 testa | 0.8145 | 0.9425 | 0.9639 | 0.9826 | 0.8700 | 0.8212 | 4766 |
| AIDA-YAGO2 testb | 0.7951 | 0.9238 | 0.9487 | 0.9663 | 0.8669 | 0.8027 | 4446 |
| ACE 2004 | 0.8443 | 0.9795| 0.9836 | 0.9836 | 0.8870 | 0.8689 | 244 |
| aquaint | 0.8662 | 0.9618| 0.9765| 0.9897 | 0.8889 | 0.8588 | 680 |
| clueweb - WNED-CWEB (CWEB) | 0.6747 | 0.8223 | 0.8609 | 0.8868 | 0.826 | 0.6825 | 10491 |
| msnbc | 0.8428 | 0.9303 | 0.9546 | 0.9676| 0.9031 | 0.8509 | 617 |
| wikipedia - WNED-WIKI (WIKI) | 0.7976 | 0.9347 | 0.9546 | 0.9776| 0.8609 | 0.8067 | 6383 |
| TAC-KBP 2010<sup>1</sup> | 0.8898 | 0.9549 | 0.9706 | 0.9843 | 0.9517 | 0.9087 | 1019 |

<sup>1</sup> Licensed dataset available [here](https://catalog.ldc.upenn.edu/LDC2018T16).


## The BLINK knowledge base
The BLINK knowledge base (entity library) is based on the 2019/08/01 Wikipedia dump, downloadable in its raw format from [http://dl.fbaipublicfiles.com/BLINK/enwiki-pages-articles.xml.bz2](http://dl.fbaipublicfiles.com/BLINK/enwiki-pages-articles.xml.bz2)

## BLINK with solr as IR system
The first version of BLINK uses an [Apache Solr](https://lucene.apache.org/solr) based Information Retrieval system in combination with a BERT based cross-encoder.
This IR-based version is now deprecated since it's outperformed by the current BLINK architecture.
If you are interested in the old version, please refer to [this README](blink/candidate_retrieval/README.md).

## Troubleshooting

If the module cannot be found, preface the python command with `PYTHONPATH=.`

## License
BLINK is MIT licensed. See the [LICENSE](LICENSE) file for details.
