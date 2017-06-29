import nibabel as nib
import matplotlib.pyplot as plt
import json
import AFQ.segmentation as seg
import os
import AFQ.utils.streamlines as aus
import AFQ.dti as dti
import nibabel as nib


def main():
    with open('config.json') as config_json:
        config = json.load(config_json)

    data_file = str(config['data_file'])
    data_bval = str(config['data_bval'])
    data_bvec = str(config['data_bvec'])

    print("Calculating DTI...")
    if not os.path.exists('./dti_FA.nii.gz'):
        dti_params = dti.fit_dti(data_file, data_bval, data_bvec, out_dir='.')
    else:
        dti_params = {'FA': './dti_FA.nii.gz',
                      'params': './dti_params.nii.gz'}
    FA_img = nib.load(dti_params['FA'])
    FA_data = FA_img.get_data()
    print("Extracting tract profiles...")
    for t in os.listdir(config['tracks']):
        if t.endswith('.trk'):
            t_str = aus.read_trk(t)
            fig, ax = plt.subplots(1)
            profile = seg.calculate_tract_profile(FA_data, t_str)
            ax.plot(profile)
            ax.set_title(t)
            path = os.getcwd() + '/tract/'
            fname = t + '.png'
            plt.savefig(path+fname)
main()
