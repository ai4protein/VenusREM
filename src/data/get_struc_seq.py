import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import argparse
from tqdm import tqdm
from structure.get_sst_seq import SSTPredictor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb_dir", type=str, default=None, help="Directory containing PDB files",)
    parser.add_argument("--pdb_file", type=str, default=None, help="PDB file",)
    parser.add_argument("--vocab_size", type=int, default=[2048], nargs='+', help="Vocabulary size",)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files",)
    parser.add_argument("--output_dir", type=str, default=None, help="Output directory",)
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    for v in args.vocab_size:
        os.makedirs(os.path.join(args.output_dir, str(v)), exist_ok=True)
    
    if args.pdb_dir is not None:
        pdb_files = sorted(os.listdir(args.pdb_dir))
        pdb_files = [os.path.join(args.pdb_dir, pdb_file) for pdb_file in pdb_files]
    elif args.pdb_file is not None:
        pdb_files = [args.pdb_file]
    else:
        raise ValueError("Either pdb_dir or pdb_file must be provided")
    
    for v in args.vocab_size:
        processor = SSTPredictor(structure_vocab_size=v)
        results = processor.predict_from_pdb(pdb_files)
        for result in results:
            name = result['name'].split('.')[0]
            sst_seq = result[f'{v}_sst_seq']
            sst_seq = [str(i) for i in sst_seq]
            with open(os.path.join(args.output_dir, str(v), name+'.fasta'), "w") as f:
                f.write(f'>{name}\n')
                f.write(','.join(sst_seq))
                