# From high-throughput evaluation to wet-lab studies: advancing mutation effect prediction with a retrieval-enhanced model

## 🚀 Introduction (VenusREM)

<img src="img/framework.png" alt="framework">

## 📑 Results

### News

- [2025.07.21] Our paper was online at [Bioinformatics](https://academic.oup.com/bioinformatics/article/41/Supplement_1/i401/8199374).
- [2025.04.19] We rank 1st in the [ProteinGym](https://proteingym.org/benchmarks) substitution leaderboard!
- [2025.04.09] Congratulations! Our paper was accepted by *ISMB/ECCB 2025*! See you in Liverpool, England.

### Downloads

- ProteinGym a2m homology sequences (EVCouplings): https://huggingface.co/datasets/AI4Protein/VenusREM/resolve/main/aa_seq_aln_a2m.tar.gz. The original a2m files are downloaded at [ProteinGym](https://github.com/OATML-Markslab/ProteinGym).
- ProteinGym a3m homology sequences (ColabFold): https://huggingface.co/datasets/AI4Protein/VenusREM/resolve/main/aa_seq_aln_a3m.tar.gz
- Uniref 100 database: https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref100/uniref100.fasta.gz

### Paper Results

<img src="img/tab1.png" alt="tab1">

## 🛫 Requirement

### Conda Enviroment

Please make sure you have installed **[Anaconda3](https://www.anaconda.com/download)** or **[Miniconda3](https://docs.conda.io/projects/miniconda/en/latest/)**.

```
conda env create -f environment.yml
conda activate venusrem

# We need HMMER and EVCouplings for MSA
# pip install hmmer
# pip install https://github.com/debbiemarkslab/EVcouplings/archive/develop.zip
```

### Other Requirement

Install plmc and change the path in `src/single_config_monomer.txt`
```shell
git clone https://github.com/debbiemarkslab/plmc.git
cd plmc
make all-openmp
```

### Hardware

- For direct use of inference, we recommend at least 10G of graphics memory, such as RTX 3080
- For searching homology sequences, 8 cores cpu.

## 🧬 Zero-shot Prediction for Mutants

### Evaluation on ProteinGym

#### Prepare for the processed data
```shell
cd data/proteingym_v1
wget https://huggingface.co/datasets/AI4Protein/VenusREM/resolve/main/aa_seq_aln_a2m.tar.gz
# unzip homology files
tar -xzf aa_seq_aln_a2m.tar.gz
# unzip fasta sequence files
tar -xzf aa_seq.tar.gz
# unzip pdb structure files
tar -xzf pdbs.tar.gz
# unzip structure sequence files
tar -xzf struc_seq.tar.gz
# unzip DMS substitution csv files
tar -xzf substitutions.tar.gz
```

#### Start inference
```shell
protein_dir=proteingym_v1
python compute_fitness.py \
    --base_dir data/$protein_dir \
    --out_scores_dir result/$protein_dir
```

### Your own dataset

#### What you need at least
If you don't have the substitution files, you can use the following command to generate them. It will generate the csv file with all 0 scores for all single mutants.
```shell
python src/data/get_sav.py \
    --fasta_file data/$protein_dir/$protein_name.fasta \
    --out_dir data/$protein_dir/substitutions
```

⚠ Please make sure all your protein names are the same as the original protein names in the original fasta files.
You should have the following directory structure.

```shell
data/<your_protein_dir_name>
|——aa_seq # amino acid sequences
|——|——protein1.fasta
|——|——protein2.fasta
|——aa_seq_aln_a2m # homology sequences of EVCouplings
|——|——protein1.a2m
|——|——protein2.a2m
|——pdbs # structures
|——|——protein1.pdb
|——|——protein2.pdb
|——struc_seq # structure sequences
|——|——protein1.fasta
|——|——protein2.fasta
|——substitutions # mutant files
|——|——protein1.csv
|——|——protein2.csv
```

#### Search homology sequences by JackHmmer
```shell
# step 1: search homology sequences
# your protein name, eg. fluorescent_protein
protein_dir=<your_protein_dir_name>
# your protein path, eg. data/fluorescent_protein/aa_seq/GFP.fasta
query_protein_name=<your_protein_name>
protein_path=data/$protein_dir/aa_seq/$query_protein_name.fasta
# your uniprot dataset path
database=<your_path>/uniref100.fasta
evcouplings \
    -P output/$protein_dir/$query_protein_name \
    -p $query_protein_name \
    -s $protein_path \
    -d $database \
    -b "0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9" \
    -n 5 src/single_config_monomer.txt
# ⚠ 👆 Repeat the searching process until all your proteins are done

# step 2: select a2m file
protein_dir=<your_protein_dir_name>
python src/data/select_msa.py \
    --input_dir output/$protein_dir \
    --output_dir data/$protein_dir
```

#### Get pdb files for your protein
You can use [AlphaFold3 server](https://alphafoldserver.com/), [AlphaFold database](https://alphafold.ebi.ac.uk/download), [ESMFold](https://huggingface.co/facebook/esmfold_v1) and other tools to obtain structures.

⚠ **For wet-lab experiments, please try to get high quality structures as possible as you can.**

#### Get structure sequences for PLM
```shell
protein_dir=<your_protein_dir_name>
python src/data/get_struc_seq.py \
    --pdb_dir data/$protein_dir/pdbs \
    --out_dir data/$protein_dir/struc_seq
```

#### Start inference
```shell
protein_dir=<your_protein_dir_name>
python compute_fitness.py \
    --base_dir data/$protein_dir \
    --out_scores_dir result/$protein_dir
```

### Other Directed Evolution Tools

You can use [ProtSSN (eLife 2024)](https://github.com/ai4protein/ProtSSN) or [ProSST (NeurIPS 2024)](https://github.com/ai4protein/ProSST).

### Questions

#### Q: How to quickly convert the input format of VenusREM to ProtSSN or ProSST?

A: For the conversion between VenusREM and ProtSSN input formats, you can refer to `script/data_format_convert.sh`. For the ProSST, jsut change the alpha to 0.

```shell
protein_dir=<your_protein_dir_name>
python compute_fitness.py \
    --base_dir data/$protein_dir \
    --out_scores_dir result/$protein_dir \
    --alpha 0 \
    --model_out_name ProSST-2048
```

#### Q: What is the difference between ProtSSN, ProSST and VenusREM?

A: ProtSSN uses modeling at the amino acid coordinate level, ProSST models on the local structure, and VenusREM explicitly introduces MSA information. They each have their own advantages and disadvantages in real experimental evaluation.

## 🙌 Citation

Please cite our work if you have used our code or data.

```
@article{tan2025venusrem,
    author = {Tan, Yang and Wang, Ruilin and Wu, Banghao and Hong, Liang and Zhou, Bingxin},
    title = {From high-throughput evaluation to wet-lab studies: advancing mutation effect prediction with a retrieval-enhanced model},
    journal = {Bioinformatics},
    volume = {41},
    number = {Supplement_1},
    pages = {i401-i409},
    year = {2025},
    month = {07},
    issn = {1367-4811},
    doi = {10.1093/bioinformatics/btaf189},
    url = {https://doi.org/10.1093/bioinformatics/btaf189},
    eprint = {https://academic.oup.com/bioinformatics/article-pdf/41/Supplement\_1/i401/63745466/btaf189.pdf},
}
```

## 📝 License

This project is licensed under the terms of the [CC-BY-NC-ND-4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode) license.
