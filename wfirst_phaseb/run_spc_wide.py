import proper
import numpy as np
import matplotlib.pylab as plt
from matplotlib.colors import LogNorm
from trim import trim

def run_spc_wide():

    n = 512                 # output image dimension
    final_sampling = 0.1    # output sampling in lam0/D
    nlam = 9
    lam0 = 0.825
    lam_min = lam0 * 0.95
    lam_max = lam0 * 1.05
    lam = np.arange(nlam) / (nlam - 1.0) * (lam_max - lam_min) + lam_min

    # compute coronagraphic image

    (fields, sampling) = proper.prop_run_multi('wfirst_phaseb', lam, n, QUIET=True, \
        PASSVALUE={'cor_type':'spc-wide','lam0':lam0,'use_errors':0,'zindex':[4],'zval_m':[0.19e-9],'final_sampling_lam0':final_sampling} )
    images = np.abs(fields)**2
    image = np.sum( images, 0 ) / nlam

    # move source to 7 lam/D

    (fields, sampling) = proper.prop_run_multi('wfirst_phaseb_compact', lam, n, QUIET=True, \
        PASSVALUE={'cor_type':'spc-wide','lam0':lam0,'source_x_offset':7.0,'final_sampling_lam0':final_sampling} )
    psfs = np.abs(fields)**2
    psf = np.sum( psfs, 0 ) / nlam

    ni = image / np.max(psf)

    fig, ax  = plt.subplots()
    im = ax.imshow(ni, norm=LogNorm(vmin=1e-10,vmax=1e-7))
    fig.colorbar(im) 
    plt.show()
    
if __name__ == '__main__':
    run_spc_wide()