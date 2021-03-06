import logging
import os
import shutil

import numpy as np


def make_results_dir(exp_path, args):
    os.makedirs(exp_path, exist_ok=True)
    if args.opr == 'train' and os.path.exists(exp_path) and os.listdir(exp_path):
        if not args.force:
            raise FileExistsError('{} is not empty. Please use --force to overwrite it'.format(exp_path))
        else:
            shutil.rmtree(exp_path)
            os.makedirs(exp_path)
    return exp_path


def init_logger(file_path):
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s][%(filename)s>%(funcName)s] ==> %(message)s')
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.FileHandler(file_path, mode='w')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def select_action(node, temperature=1, deterministic=True):
    visit_counts = [(child.visit_count, action) for action, child in node.children.items()]
    if deterministic:
        action_pos = np.argmax([v for v, _ in visit_counts])
    else:
        action_probs = [visit_count_i ** (1 / temperature) for visit_count_i, _ in visit_counts]
        total_count = sum(action_probs)
        action_probs = [x / total_count for x in action_probs]
        action_pos = np.random.choice(len(visit_counts), p=action_probs)

    return visit_counts[action_pos][1]
