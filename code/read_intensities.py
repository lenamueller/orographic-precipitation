import pickle 


def read_intensities():
    # output: dictionaries z1 = {"1":[],...,"36:[]"} with intensities for each list (window size)
    with open('metdata/intensities/intensities_z1.pkl', 'rb') as f:
        z1 = pickle.load(f)
    with open('metdata/intensities/intensities_z2.pkl', 'rb') as f:
        z2 = pickle.load(f)
    with open('metdata/intensities/intensities_z3.pkl', 'rb') as f:
        z3 = pickle.load(f)
    return z1, z2, z3

def read_intensities_st():
    # output: dictionaries z1 = {"7394:[[],[],[],[],[],[],[]]"} with intensities in each list (window size)
    with open('metdata/intensities/intensities_z1_st.pkl', 'rb') as f:
        z1 = pickle.load(f)
    with open('metdata/intensities/intensities_z2_st.pkl', 'rb') as f:
        z2 = pickle.load(f)
    with open('metdata/intensities/intensities_z3_st.pkl', 'rb') as f:
        z3 = pickle.load(f)
    return z1, z2, z3