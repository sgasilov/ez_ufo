def enquote(string, escape=False):
    addition = '\\"' if escape else '"'

    return addition + string + addition

'''
Created on Apr 20, 2020

@author: gasilos
'''
import os

def save_params(args, ctsetname, ax, nviews, WH):
    if not args.dryrun and not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    tmp = os.path.join(args.outdir, ctsetname)
    if not args.dryrun and not os.path.exists(tmp):
        os.makedirs(tmp)
    if not args.dryrun and args.parfile:
        fname = os.path.join(tmp, 'reco.params')
        f = open( fname, 'w' )
        f.write('*** General ***\n')
        f.write( 'Input directory {}\n'.format(args.indir) )
        if ctsetname=='':
            ctsetname='.'
        f.write( 'CT set {}\n'.format(ctsetname) )
        if args.ax==1 or args.ax==2:
            f.write( 'Center of rotation {} (auto estimate)\n'.format(ax))
        else:
            f.write( 'Center of rotation {} (user defined)\n'.format(ax))
        f.write( 'Dimensions of projections {} x {} (height x width)\n'.format(WH[0],WH[1]) )
        f.write( 'Number of projections {}\n'.format(nviews) )
        f.write('*** Preprocessing ***\n')
        tmp='none'
        if args.pre:
            tmp=args.pre_cmd
        f.write( 'Image filters: {}\n'.format(tmp) )
        if args.inp:
            f.write('Remove large spots enabled\n')
            f.write('  threshold {}\n'.format(args.inp_thr) )
            f.write('  sigma {}\n'.format(args.inp_sig) )
        else:
            f.write( 'Remove large spots disabled\n')
        if args.PR:
            f.write('Phase retreival enabled\n')
            f.write('  energy {} keV\n'.format(args.energy))
            f.write('  pixel size {:0.1f} um\n'.format(args.pixel*1e6))
            f.write('  sample-detector distance {} m\n'.format(args.z))
            f.write('  delta/beta ratio {:0.0f}\n'.format(10**args.log10db))
        else:
            f.write( 'Phase retreival disabled\n')
        f.write('*** Region of interest ***\n')
        if args.vcrop:
            f.write('Vertical ROI defined\n')
            f.write('  first row {}\n'.format(args.y))
            f.write('  height {}\n'.format(args.yheight))
            f.write('  reconstruct every {}th row\n'.format(args.ystep))
        else:
            f.write( 'Vertical ROI: all rows\n')
        if args.crop:
            f.write('ROI in slice plane defined\n')
            f.write('  x {}\n'.format(args.x0))
            f.write('  width {}\n'.format(args.dx))
            f.write('  y {}\n'.format(args.y0))
            f.write('  height {}\n'.format(args.dy))
        else:
            f.write('ROI in slice plane not defined\n')
        f.write('*** Reconstructed values ***\n')
        if args.gray256:
            f.write('  {} bit\n'.format(args.bit) )
            f.write('  Min value in 32-bit histogram {}\n'.format(args.hmin) )
            f.write('  Max value in 32-bit histogram {}\n'.format(args.hmax) )
        else:
            f.write('  32bit, histogram untouched\n')
        f.write('*** Optional reco parameters ***\n')
        if args.a0>0:
            f.write('  Rotate volume by: {:0.3f} deg\n'.format(args.a0) )
        f.close()

