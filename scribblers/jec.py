# Tai Sakuma <tai.sakuma@gmail.com>
import copy

import pandas as pd
import numpy as np

from ._util.Binning import Binning

##__________________________________________________________________||
class ScalePtByFactorOfPtEtaFromTbl(object):
    def __init__(self, tbl_corr_path, valid_eta_range = (-5.0, 5.0), default_scale_factor = 1.0):
        self.tbl_corr_path = tbl_corr_path
        self.valid_eta_range = tuple(valid_eta_range)
        self.default_scale_factor = default_scale_factor
        self._read_file(tbl_corr_path)

    def _read_file(self, tbl_corr_path):
        tbl_corr = pd.read_table(tbl_corr_path, delim_whitespace = True)
        tbl = tbl_corr.sort_values(by = ['jet_eta', 'jet_pt']).reset_index(drop = True)

        eta_bin_boundaries = tbl['jet_eta'].unique()
        self.eta_binning =  Binning(boundaries = eta_bin_boundaries)

        self.pt_binning_dict = { } # key: eta_bin
        self.corr_dict = { } # key: (eta_bin, pt_bin)
        self.corr_minpt_dict = { } # key: eta_bin

        for eta, g in tbl.groupby('jet_eta'):
            pt_bin_boundaries = g['jet_pt'].values
            scale_factors =  g['corr'].values
            self.pt_binning_dict[eta] = Binning(boundaries = pt_bin_boundaries)
            self.corr_dict.update({(eta, pt): corr for pt, corr in zip(pt_bin_boundaries, scale_factors)})
            self.corr_minpt_dict[eta] = scale_factors[0]

    def __repr__(self):
        name_value_pairs = (
            ('tbl_corr_path', self.tbl_corr_path),
            ('valid_eta_range', self.valid_eta_range),
            ('default_scale_factor', self.default_scale_factor),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, pt, eta):
        return pt*self.scale_factor(pt, eta)

    def scale_factor(self,pt, eta):

        if not self.valid_eta_range[0] <= eta <= self.valid_eta_range[1]:
            return self.default_scale_factor

        eta_bin = self.eta_binning(eta)

        if np.isinf(eta_bin):
            return self.default_scale_factor

        pt_bin = self.pt_binning_dict[eta_bin](pt)

        if np.isinf(pt_bin) and pt_bin < 0:
            return self.corr_minpt_dict[eta_bin]

        return self.corr_dict[(eta_bin, pt_bin)]

##__________________________________________________________________||
class ApplyJEC(object):
    def __init__(self, scale_func_pt_eta, obj_pt_eta_names = ('pt', 'eta')):
        self.scale_func_pt_eta = scale_func_pt_eta
        self.obj_pt_eta_names = obj_pt_eta_names

        self.obj_pt_name, self.obj_eta_name = obj_pt_eta_names

    def __repr__(self):
        name_value_pairs = (
            ('scale_func_pt_eta', self.scale_func_pt_eta),
            ('obj_pt_eta_names', self.obj_pt_eta_names),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, obj):
        pt = getattr(obj, self.obj_pt_name)
        eta = getattr(obj, self.obj_eta_name)
        pt_corr = self.scale_func_pt_eta(pt, eta)
        ret = copy.copy(obj)
        setattr(ret, self.obj_pt_name, pt_corr),
        return ret

##__________________________________________________________________||
