# -*- coding: utf-8 -*-
import pandas as pd

def get_default_options(xres, yres, freq, screen_width, screen_height):
    opt = dict()
    # General variables for eye-tracking data
    # maximum value of horizontal resolution in pixels
    opt['xres'] = xres
    opt['yres'] = yres
    # maximum value of vertical resolution in pixels
    # missing value for horizontal position in eye-tracking data (example data uses -xres). used throughout
    # internal_helpers as signal for data loss
    opt['missingx'] = -opt['xres']
    # missing value for vertical position in eye-tracking data (example data uses -yres). used throughout
    # internal_helpers as signal for data loss
    opt['missingy'] = -opt['yres']
    # sampling frequency of data (check that this value matches with values actually obtained from measurement!)
    opt['freq'] = float(freq)

    # Variables for the calculation of visual angle
    # These values are used to calculate noise measures (RMS and BCEA) of
    # fixations. The may be left as is, but don't use the noise measures then.
    # If either or both are empty, the noise measures are provided in pixels
    # instead of degrees.
    # screen size in cm
    opt['scrSz'] = [screen_width, screen_height]
    # distance to screen in cm.
    opt['disttoscreen'] = 65.0

    # STEFFEN INTERPOLATION
    # max duration (s) of missing values for interpolation to occur
    opt['windowtimeInterp'] = 0.1
    # amount of data (number of samples) at edges needed for interpolation
    opt['edgeSampInterp'] = 2
    # maximum displacement during missing for interpolation to be possible
    opt['maxdisp'] = opt['xres'] * 0.2 * np.sqrt(2)

    # # K-MEANS CLUSTERING
    # time window (s) over which to calculate 2-means clustering (choose value so that max. 1 saccade can occur)
    opt['windowtime'] = 0.2
    # time window shift (s) for each iteration. Use zero for sample by sample processing
    opt['steptime'] = 0.02
    # maximum number of errors allowed in k-means clustering procedure before proceeding to next file
    opt['maxerrors'] = 100
    opt['downsamples'] = [2, 5, 10]
    # use chebychev filter when down sampling? 1: yes, 0: no. requires signal processing toolbox. is what matlab's
    # down sampling internal_helpers do, but could cause trouble (ringing) with the hard edges in eye-movement data
    opt['downsampFilter'] = False

    # # FIXATION DETERMINATION
    # number of standard deviations above mean k-means weights will be used as fixation cutoff
    opt['cutoffstd'] = 2.0
    # number of MAD away from median fixation duration. Will be used to walk forward at fixation starts and backward at
    # fixation ends to refine their placement and stop algorithm from eating into saccades
    opt['onoffsetThresh'] = 3.0
    # maximum Euclidean distance in pixels between fixations for merging
    opt['maxMergeDist'] = 40.0
    # maximum time in ms between fixations for merging
    opt['maxMergeTime'] = 60.0
    # minimum fixation duration after merging, fixations with shorter duration are removed from output
    opt['minFixDur'] = 90.0


def fixation_detection(gazeData, options):
    """
    Parameters
    ----------
    @param gazeData: a dataframe containing the gaze data
        the dataframe should contain the following column:
            time        - time of the gaze sample (ms)
        and the dataframe should furthermore contain at least some of the
        following columns of eye data (either L, or R, or both L and R, or average):
            L_X         - left eye x position
            L_Y         - left eye y position
            R_X         - right eye x position
            R_Y         - right eye y position
            average_X   - average x position
            average_Y   - average y position
    """
    from .I2MC import I2MC

    fix, data, par = I2MC(gazeData, options, logging=False)
    df_fix = pd.DataFrame()
    df_fix["x"] = fix["xpos"]
    df_fix["y"] = fix["ypos"]
    df_fix["x_range"] = fix["fixRangeX"]
    df_fix["y_range"] = fix["fixRangeY"]
    df_fix["start_t"] = fix["startT"]
    df_fix["end_t"] = fix["endT"]
    df_fix["radius"] = df_fix[["x_range", "y_range"]].max(axis=1)

    return df_fix

__all__ = [
    "I2MC",
]
