import csv
import argparse

def generate_point_mutations(fasta_file, output_csv):
    with open(fasta_file, 'r') as f:
        lines = f.readlines()
        sequence = ''.join(line.strip() for line in lines[1:])  # 跳过标题行

    # 定义氨基酸字母表
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    # 存储突变结果
    mutations = []

    # 生成单点突变
    for i, original in enumerate(sequence):
        for mutant in amino_acids:
            if mutant != original: 
                mutation = f"{original}{i+1}{mutant}" 
                mutations.append((mutation, 0)) 

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['mutant', 'DMS_score']) 
        for mutation, score in mutations:
            csv_writer.writerow([mutation, score]) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate point mutations from FASTA file')
    parser.add_argument('--fasta_file', type=str, required=True, help='Path to the FASTA file')
    parser.add_argument('--output_csv', type=str, required=True, help='Path to the output CSV file')
    args = parser.parse_args()

    generate_point_mutations(args.fasta_file, args.output_csv)
