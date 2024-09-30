import os
import numpy as np
import data_io
from prf_metrics import cal_prf_metrics
from segment_metrics import cal_semantic_metrics
import argparse

# Configuration des arguments
parser = argparse.ArgumentParser()
parser.add_argument('--metric_mode', type=str, default='prf', help='[prf | sem]')
parser.add_argument('--model_name', type=str, default='deepcrack-BN')
parser.add_argument('--results_dir', type=str, default='./demo')
parser.add_argument('--suffix_gt', type=str, default='label_viz', help='Suffix of ground-truth file name')
parser.add_argument('--suffix_pred', type=str, default='fused', help='Suffix of predicted file name')
parser.add_argument('--output', type=str, default='results.txt')
parser.add_argument('--thresh_step', type=float, default=0.01)
args = parser.parse_args()

if __name__ == '__main__':
    metric_mode = args.metric_mode
    results_dir = os.path.join(args.results_dir, args.model_name, 'test_latest', 'results')
    
    # Récupérer les paires d'images
    src_img_list, tgt_img_list = data_io.get_image_pairs(results_dir, args.suffix_gt, args.suffix_pred)

    final_results = []
    
    # Calcul des métriques
    if metric_mode == 'prf':
        final_results = cal_prf_metrics(src_img_list, tgt_img_list, args.thresh_step)
    elif metric_mode == 'sem':
        final_results = cal_semantic_metrics(src_img_list, tgt_img_list, args.thresh_step)
    else:
        print("Unknown mode of metrics.")
        exit(1)  # Sortir avec une erreur si le mode n'est pas reconnu

    # Sauvegarder les résultats
    if args.output:
        data_io.save_results(final_results, args.output)
        print(f"Results saved to {args.output}")
    else:
        print("No output file specified.")
