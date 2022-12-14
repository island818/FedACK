# -*- coding: utf-8 -*-

import argparse
import json
import os
base_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_path,'datas','NCLS-Processed','ZH2ENSUM')

def common_opts(parser):
    parser.add_argument("-vocab", type=str,default=[os.path.join(data_path,'all_bert_voc_dic.txt'),os.path.join(data_path,'all_bert_voc_dic.txt')], nargs="*", help="Vocab file")
#    parser.add_argument("-batch_size", type=int, default=8192, help="Batch size")
    parser.add_argument("-beam_size",  type=int, default=4, help="Beam size")
    parser.add_argument("-max_length", type=int, default=200, help="Maximum prediction length")
    parser.add_argument("-length_penalty",  type=float, default=0.6, help="Length penalty")
    parser.add_argument("-model_path", default="train", help="Path to model checkpoint file")
    parser.add_argument("-tf", action="store_true",default=True, help="Use teacher forcing for decoding")
    parser.add_argument("-mono", action="store_true", help="任务1为单语摘要")
    # parser.add_argument("-share_cn_embedding", default=True,action="store_false", help="原文和中文摘要共享词表")
#    parser.add_argument("-share_mt_cls_embedding", action="store_false", help="share_mt_cls_embedding")
    parser.add_argument("-min_length", type=int, default=1, help="Minimum prediction length")


def data_opts(parser):
    parser.add_argument("-train",default=[os.path.join(data_path,'ZH2ENSUM_train_en.txt'),os.path.join(data_path,'ZH2ENSUM_train_zh.txt')] ,type=str, nargs=5, help="Training data")
    parser.add_argument("-valid",default=[os.path.join(data_path,'ZH2ENSUM_valid_en.txt'),os.path.join(data_path,'ZH2ENSUM_valid_zh.txt')] , type=str, nargs=5, help="Validation data")
    parser.add_argument("-test",default=[os.path.join(data_path,'ZH2ENSUM_test_en.txt'),os.path.join(data_path,'ZH2ENSUM_test_zh.txt')] , type=str, nargs=5, help="Test data")
    parser.add_argument("-test_data_num", type=int, default=20000, help="number of testdata")
    parser.add_argument("-max_test_data", type=int, default=200, help="the max value in testdata")


def train_opts(parser):
#    parser.add_argument("-grad_accum", type=int, default=1, help="Accumulate gradients")
    parser.add_argument("-max_to_keep", type=int, default=5, help="How many checkpoints to keep")
    parser.add_argument("-report_every", type=int, default=50, help="Report every n steps")
    parser.add_argument("-save_every", type=int, default=500, help="Valid and save model for every n steps")

#    parser.add_argument("-train_from", type=str, default=None, help="Train from checkpoint")


def model_opts(parser):
    parser.add_argument("-layers", type=int, default=6, help="Number of layers")
    parser.add_argument("-heads", type=int, default=8, help="Number of heads")
    parser.add_argument("-hidden_size", type=int, default=512, help="Size of hidden states")
    parser.add_argument("-ff_size", type=int, default=2048, help="Feed forward hidden size")

    parser.add_argument("-lr", type=float, default=1.0, help="Learning rate")
    parser.add_argument("-adam_lr", type=float, default=0.0002, help="adam: learning rate")
    parser.add_argument("-b1", type=float, default=0.5, help="adam: decay of first order momentum of gradient")
    parser.add_argument("-b2", type=float, default=0.999, help="adam: decay of first order momentum of gradient")
    parser.add_argument("-train_dis", type=int, default=1, help="number for discriminator training")
#    parser.add_argument("-warm_up", type=int, default=8000, help="Warm up step")
    parser.add_argument("-label_smoothing", type=float, default=0.1, help="Label smoothing rate")
    parser.add_argument("-dropout", type=float, default=0.1, help="Dropout rate")


def translate_opts(parser):
    parser.add_argument("-input", type=str, help="Translation data")
    parser.add_argument("-truth", type=str, default=None, help="Truth target, used to calculate BLEU")
    parser.add_argument("-output", nargs=2, default=["output1.txt", "output2.txt"], help="Path to output the predictions")
    parser.add_argument("-bleu", action="store_true", help="Report BLEU")


def parse_train_args():
    parser = argparse.ArgumentParser()
    data_opts(parser)
    train_opts(parser)
    model_opts(parser)
    common_opts(parser)
    return parse_args(parser)


def parse_translate_args():
    parser = argparse.ArgumentParser()
    translate_opts(parser)
    common_opts(parser)
    return parse_args(parser)


def parse_args(parser):
    parser.add_argument("-config", type=str, help="Config file")
    parser.add_argument("-batch_size", type=int, default=2048, help="Batch size")
    parser.add_argument("-warm_up", type=int, default=8000, help="Warm up step")
    parser.add_argument("-latent_dim", type=int, default=256, help="latent dim")
    parser.add_argument("-kl_annealing_steps", type=int, default=800000, help="Warm up step")
    parser.add_argument("-grad_accum", type=int, default=3, help="Accumulate gradients")
    parser.add_argument("-share_cn_embedding", action="store_false", help="�~N~_�~V~G�~R~L中�~V~G�~Q~X�~A�~E�享�~M表")
    parser.add_argument("-share_mt_cls_embedding", action="store_false", help="share_mt_cls_embedding")
    parser.add_argument("-share_source_target_embedding",default=True, help="share_mt_cls_embedding")
    parser.add_argument('-gpu', default=3, type=int, help='node rank for distributed training')
    parser.add_argument("-train_from", type=str, default=None, help="Train from checkpoint")
    parser.add_argument("-split", type=float, default=1.0, help="split")
    parser.add_argument('-device', default=1, type=int, help='which device to run')
    opt = parser.parse_args()
    if opt.config:
        config = json.load(open(opt.config), object_hook=lambda d: {k: v for k, v in d.items() if k != "comment"})
        parser.set_defaults(**config)
        return parser.parse_args()
    else:
        return opt