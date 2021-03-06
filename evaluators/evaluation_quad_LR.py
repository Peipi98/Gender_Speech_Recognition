# -*- coding: utf-8 -*-
import sys

import numpy as np

sys.path.append('../')
from validators import *
from prettytable import PrettyTable


def validate_LR(scores, LR_labels, appendToTitle, l):
    scores_append = np.hstack(scores)
    scores_tot = compute_min_DCF(scores_append, LR_labels, 0.5, 1, 1)

    # plot_ROC(scores_append, LR_labels, appendToTitle + 'LR, lambda=' + str(l))

    # Cfn and Ctp are set to 1
    # bayes_error_min_act_plot(scores_append, LR_labels, appendToTitle + 'LR, lambda=' + str(l), 0.4)

    t = PrettyTable(["Type", "minDCF"])
    t.title = appendToTitle + "minDCF: π=0.5"
    t.add_row(['QUAD_LR, lambda=' + str(l), round(scores_tot, 3)])
    print(t)

    ###############################

    # π = 0.1
    scores_tot = compute_min_DCF(scores_append, LR_labels, 0.1, 1, 1)

    t = PrettyTable(["Type", "minDCF"])
    t.title = appendToTitle + "minDCF: π=0.1"
    t.add_row(['QUAD_LR, lambda=' + str(l), round(scores_tot, 3)])

    print(t)

    ###############################

    # π = 0.9
    scores_tot = compute_min_DCF(scores_append, LR_labels, 0.9, 1, 1)

    t = PrettyTable(["Type", "minDCF"])
    t.title = appendToTitle + "minDCF: π=0.9"
    t.add_row(['QUAD_LR, lambda=' + str(l), round(scores_tot, 3)])

    print(t)


def evaluate_LR(DTR, LTR, DTE, LTE, l, appendToTitle, PCA_Flag=True):
    scores_append = []
    PCA_LR_scores_append = []
    PCA2_LR_scores_append = []
    LR_labels = []

    def vecxxT(x):
        x = x[:, None]
        xxT = x.dot(x.T).reshape(x.size ** 2, order='F')
        return xxT

    expanded_DTR = numpy.apply_along_axis(vecxxT, 0, DTR)
    expanded_DTE = numpy.apply_along_axis(vecxxT, 0, DTE)
    phi = numpy.vstack([expanded_DTR, DTR])

    phi_DTE = numpy.vstack([expanded_DTE, DTE])

    scores = quad_logistic_reg_score(phi, LTR, phi_DTE, l)
    scores_append.append(scores)

    LR_labels = np.append(LR_labels, LTE, axis=0)
    LR_labels = np.hstack(LR_labels)

    if PCA_Flag is True:
        # PCA m=10
        P = PCA(DTR, LTR, m=10)
        DTR_PCA = numpy.dot(P.T, DTR)
        DTE_PCA = numpy.dot(P.T, DTE)

        PCA_LR_scores = quad_logistic_reg_score(DTR_PCA, LTR, DTE_PCA, l)
        PCA_LR_scores_append.append(PCA_LR_scores)

        # PCA m=9
        P = PCA(DTR, LTR, m=9)
        DTR_PCA = numpy.dot(P.T, DTR)
        DTE_PCA = numpy.dot(P.T, DTE)

        PCA2_LR_scores = quad_logistic_reg_score(DTR_PCA, LTR, DTE_PCA, l)
        PCA2_LR_scores_append.append(PCA2_LR_scores)

    validate_LR(scores_append, LR_labels, appendToTitle, l)
    if PCA_Flag is True:
        validate_LR(PCA_LR_scores_append, LR_labels, appendToTitle + 'PCA_m10_', l)

        validate_LR(PCA2_LR_scores_append, LR_labels, appendToTitle + 'PCA_m9_', l)

def kfold_LR_calibration(DTR, LTR, l):
    k = 5
    Dtr = numpy.split(DTR, k, axis=1)
    Ltr = numpy.split(LTR, k)

    scores_append = []
    LR_labels = []

    for i in range(k):
        D = []
        L = []
        if i == 0:
            D.append(np.hstack(Dtr[i + 1:]))
            L.append(np.hstack(Ltr[i + 1:]))
        elif i == k - 1:
            D.append(np.hstack(Dtr[:i]))
            L.append(np.hstack(Ltr[:i]))
        else:
            D.append(np.hstack(Dtr[:i]))
            D.append(np.hstack(Dtr[i + 1:]))
            L.append(np.hstack(Ltr[:i]))
            L.append(np.hstack(Ltr[i + 1:]))

        D = np.hstack(D)
        L = np.hstack(L)

        Dte = Dtr[i]
        Lte = Ltr[i]

        scores = logistic_reg_score(D, L, Dte, l)
        scores_append.append(scores)

        LR_labels = np.append(LR_labels, Lte, axis=0)
        LR_labels = np.hstack(LR_labels)

    return np.hstack(scores_append), LR_labels


def evaluation_quad_LR(DTR, LTR, DTE, LTE, L, appendToTitle, PCA_Flag=True):
    for l in L:  # l is a constant, not an array
        evaluate_LR(DTR, LTR, DTE, LTE, l, appendToTitle, PCA_Flag)
