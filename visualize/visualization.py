import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{bm}']

import seaborn as sns

from .utils import get_params, get_params_mi

def weight_hist(net, path):
    sns.set()
    params = get_params(net)
    fig, ax = plt.subplots(1,1)
    ax.hist(params)
    ax.set_ylabel(r'count', fontsize=17)
    ax.set_xlabel(r'$\bm{\theta}$', fontsize=17)
    plt.tight_layout()
    plt.savefig(path)

def log_weight_hist(net, path):
    sns.set()
    params = get_params(net)
    log_params = np.log(np.abs(params))
    log_params[log_params < -1e10] = 0
    fig, ax = plt.subplots(1,1)
    ax.hist(log_params)
    ax.set_ylabel(r'count', fontsize=17)
    ax.set_xlabel(r'$\log|\bm{\theta}|$', fontsize=17)
    plt.tight_layout()
    plt.savefig(path)

def snr_hist(net, path):
    mus, sigmas = get_params_mi(net)
    snr = (np.abs(mus) / sigmas)
    fig, ax = plt.subplots(1,1)
    ax.hist(snr)
    ax.set_ylabel(r'count', fontsize=17)
    ax.set_xlabel(r'SNR', fontsize=17)
    plt.tight_layout()
    plt.savefig(path)

def log_snr_hist(net, path):
    mus, sigmas = get_params_mi(net)
    log_snr = np.log(np.abs(mus) / sigmas)
    fig, ax = plt.subplots(1,1)
    ax.hist(log_snr)
    ax.set_ylabel(r'count', fontsize=17)
    ax.set_xlabel(r'$\log(\textrm{SNR})$', fontsize=17)
    plt.tight_layout()
    plt.savefig(path)

def plot_uncert(err, sigma, freq_in_bin=None, outlier_freq=0.0):
    if freq_in_bin is not None:
        freq_in_bin = freq_in_bin[torch.where(freq_in_bin > outlier_freq)]  # filter out zero frequencies
        err = err[torch.where(freq_in_bin > outlier_freq)]
        sigma = sigma[torch.where(freq_in_bin > outlier_freq)]
    fig, ax = plt.subplots(1, 1, figsize=(2.5, 2.25))
    max_val = np.max([err.max(), sigma.max()])
    min_val = np.min([err.min(), sigma.min()])
    ax.plot([min_val, max_val], [min_val, max_val], 'k--')
    ax.plot(sigma, err, marker='.')
    ax.set_ylabel(r'mse')
    ax.set_xlabel(r'uncertainty')
    ax.set_aspect(1)
    fig.tight_layout()
    return fig, ax

def plot_conf(acc, conf):
    fig, ax = plt.subplots(1, 1, figsize=(2.5, 2.25))
    ax.plot([0,1], [0,1], 'k--')
    ax.plot(conf.data.cpu().numpy(), acc.data.cpu().numpy(), marker='.')
    ax.set_xlabel(r'confidence')
    ax.set_ylabel(r'accuracy')
    ax.set_xticks((np.arange(0, 1.1, step=0.2)))
    ax.set_yticks((np.arange(0, 1.1, step=0.2)))

    return fig, ax
