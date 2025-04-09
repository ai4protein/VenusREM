import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_attention_map(csv_file, output_file=None, figsize=(20, 10)):
    data = pd.read_csv(csv_file)

    mutations = data['mutant']
    scores = data['DMS_score']

    sequence_length = max(int(mutation[1:-1]) for mutation in mutations)
    original_aa = {}
    for mutation in mutations:
        pos = int(mutation[1:-1])
        original_aa[pos] = mutation[0]
    
    amino_acids = list('ACDEFGHIKLMNPQRSTVWY')

    score_matrix = np.zeros((len(amino_acids), sequence_length))

    for mutation, score in zip(mutations, scores):
        position = int(mutation[1:-1]) - 1
        target = mutation[-1]
        if target in amino_acids:
            score_matrix[amino_acids.index(target), position] = score

    plt.figure(figsize=figsize)
    ax = sns.heatmap(score_matrix, cmap='viridis', cbar=True, 
                     xticklabels=range(1, sequence_length+1),
                     yticklabels=amino_acids)
    
    plt.title('Amino Acid Substitution Scores', fontsize=16)
    plt.xlabel('Position in Protein Sequence', fontsize=14)
    plt.ylabel('Substituted Amino Acid', fontsize=14)
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()

plot_attention_map('scores/phi29_42.csv', output_file='amino_acid_attention_map.png')
