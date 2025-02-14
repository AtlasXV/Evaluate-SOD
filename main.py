import torch
import torch.nn as nn
import argparse
import os.path as osp
import os
import utils
from evaluator import Eval_thread
from dataloader import EvalDataset
# from concurrent.futures import ThreadPoolExecutor
def main(cfg):
    root_dir = cfg.root_dir
    if cfg.save_dir is not None:
        output_dir = cfg.save_dir
    else:
        output_dir = root_dir
    gt_dir = osp.join(root_dir, 'gt')
    pred_dir = osp.join(root_dir, 'pred')
    if cfg.methods is None:
        method_names = os.listdir(pred_dir)
    else:
        method_names = cfg.methods.split(' ')
    if cfg.datasets is None:
        dataset_names = os.listdir(gt_dir)
    else:
        dataset_names = cfg.datasets.split(' ')
    
    threads = []
    for dataset in dataset_names:
        for method in method_names:
            dataset_path = osp.join(pred_dir, method, dataset)
            if osp.exists(dataset_path):
                loader = EvalDataset(dataset_path, osp.join(gt_dir, dataset))
                thread = Eval_thread(loader, method, dataset, output_dir, cfg.cuda)
                threads.append(thread)
            else:
                print(dataset_path + ' does not exist, so ignore it here')

    for thread in threads:
        print(thread.run())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--methods', type=str, default=None)
    parser.add_argument('--datasets', type=str, default=None)
    parser.add_argument('--root_dir', type=str, default='./')
    parser.add_argument('--save_dir', type=str, default=None)
    parser.add_argument('--cuda', type=utils.str2bool, default=True)
    config = parser.parse_args()
    main(config)
