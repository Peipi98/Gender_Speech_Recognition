from mlFunc import *
from validators import *
from classifiers import *

if __name__ == "__main__":
    DTR, LTR = load("Train.txt")

    DTE, LTE = load("Test.txt")
    # plot_hist(D, L)

    # We're starting with Multivariate Gaussian Classifier
    _, LPred2 = MGC(DTE, LTE, DTR, LTR)
    _, LP2n = naive_MGC(DTE, LTE, DTR, LTR)
    _, LP2t = tied_cov_GC(DTE, LTE, DTR, LTR)
    _, LP2nt = tied_cov_naive_GC(DTE, LTE, DTR, LTR)
    # logMGC accuracy
    log_acc, log_err = test(LTE, LPred2)
    log_acc_n, log_err_n = test(LTE, LP2n)
    log_acc_t, log_err_t = test(LTE, LP2t)
    log_acc_nt, log_err_nt = test(LTE, LP2nt)

    # print(holdout_validation(MGC, DTR, LTR))
    # print(holdout_validation(naive_MGC, DTR, LTR))
    # print(holdout_validation(tied_cov_GC, DTR, LTR))
    # print(holdout_validation(tied_cov_naive_GC, DTR, LTR))
    # 0.9683333333333334
    # 0.71
    # 0.9675
    # 0.7125

    # print(leave_one_out(MGC, DTR, LTR))
    # print(leave_one_out(naive_MGC, DTR, LTR))
    # print(leave_one_out(tied_cov_GC, DTR, LTR))
    # print(leave_one_out(tied_cov_naive_GC, DTR, LTR))
    kfold_cross(MGC, DTR, LTR, 10)

    # DA CHIEDERE
    # Notiamo che i risultati di leave-one-out sono rispettivamente
    # più bassi rispetto ai precedenti non naive, ma più alti dei naive.
    # 0.9753333333333334 
    # 0.7031666666666667
    # 0.9755
    # 0.7048333333333333

    # Notiamo che le features sono molto correlate tra loro,
    # quindi non possiamo fare l'assunzione di indipendenza di Naive Bayes

    # PCA(D, L)
    lamb = [1e-6, 1e-3, 0.1, 1.0, 0.0, 3.0]
    
    for l in lamb:
        LPred, _J= linear_reg(DTR, LTR, DTE, LTE, l)
        print(LPred)
        acc_LR, err_LR = test(LTE, LPred)
        print(str(acc_LR) + "\t" +str(err_LR))
    # for l in [1e-6, 1e-3, 0.1, 1.0]:
    #     logreg_obj = logreg_obj_wrap(DTR, LTR, l)
    #     _v, _J, _d = opt.fmin_l_bfgs_b(logreg_obj, numpy.zeros(DTR.shape[0]+1), approx_grad=True)
    #     _w = _v[0:DTR.shape[0]]
    #     _b = _v[-1]
    #     STE = numpy.dot(_w.T, DTE) + _b
    #     LP = STE > 0
    #     ER = 1 - numpy.array(LP == LTE).mean()
    #     print(l, round(_J, 3), str(100*round(ER, 3))+'%')