# annif-ems

This repository contains vocabulary, configuration and corpus data for setting up and using Annif with the Estonian Subject Thesaurus EMS.

For running the Python scripts in this repo, you need a recent version of Python (tested with 3.10) as well as a few dependencies that are listed in [requirements.txt](requirements.txt).

Install the dependencies in a Python virtual environment using `pip install -r requirements.txt`

# Annif installation & configuration file

You will need to install Annif using any of the [supported installation methods](https://github.com/NatLibFi/Annif-tutorial/blob/master/exercises/01_install_annif.md). To install it locally in a Python virtual environment (with the required YAKE and Omikuji features), use the command

    pip install annif[yake,omikuji]

The included configuration file [projects.cfg](projects.cfg) should be placed in the working directory where Annif is executed. It defines the following projects:

* `ems-yake-et`: simple YAKE lexical algorithm that doesn't require any training
* `ems-bonsai-et`: Omikuji Bonsai associative algorithm, needs to be trained on e.g. metadata records (titles + subjects)
* `ems-ensemble-et`: simple averaging ensemble project using the above two projects as sources (with omikuji-bonsai given a much bigger weight)

For training the Omikuji Bonsai project, see below.

# Estonian Subject Thesaurus EMS as SKOS

Annif requires subject vocabularies in SKOS or TSV/CSV format.

EMS was downloaded on 2024-04-02 in MARCXML format from the [ELNET open data portal](https://data.elnet.ee/marksonastik/).

The included script [marcxml-to-skos.py](marcxml-to-skos.py) converts the MARC data into simple SKOS. You can run it like this:

    python marcxml-to-skos ems_marc_tais.xml ems_marc_tais.ttl

The resulting file [ems_marc_tais.ttl](ems_marc_tais.ttl) can be loaded into Annif like this:

    annif load-vocab ems ems_marc_tais.ttl

# Training corpus based on ISE article metadata

The [Estonian article database ISE](https://data.elnet.ee/ise/) can be used as a source of training data. It is divided into many subsets ([ListSets via OAI-PMH](https://artiklid.elnet.ee/iii/oai/OAIRepository?verb=ListSets)) and each subset can be downloaded separately via OAI-PMH.

The included script [collect-ise.py](collect-ise.py) can be used for the data collection. It can be run like this (in this case on the `itehn` subset):

    python collect-ise.py itehn >ise.itehn.xml

The resulting file will have one OAI-DC XML record per line. It can be converted into TSV format for training Annif using the script [oai_dc-to-corpus.py](oai_dv-to-corpus.py) like this:

    python oai_dc-to-corpus.py <ise.itehn.xml >ise.itehn.tsv

Using these scripts, the ISE subsets `aa`, `ihari`, `ise`, `itehn`, `space1` and `yy` (quite a random selection!) were downloaded on 2024-04-02 and converted into a TSV corpus. The resulting corpus file [ise-corpus.tsv.gz](ise-corpus.tsv.gz) contains around 400k records/lines. It can be used to train the Omikuji Bonsai project like this:

    annif train ems-bonsai-et ise-corpus.tsv.gz

# Testing Annif

After training, you can test Annif by starting it with the command

    annif run

and opening the URL http://localhost:5000 in a web browser.
