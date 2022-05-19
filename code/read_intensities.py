import pickle 


def read_intensities():
    with open('metdata/intensities_z1.pkl', 'rb') as f:
        z1 = pickle.load(f)
    with open('metdata/intensities_z2.pkl', 'rb') as f:
        z2 = pickle.load(f)
    with open('metdata/intensities_z3.pkl', 'rb') as f:
        z3 = pickle.load(f)
    return z1, z2, z3