from math import atan2, pi, sqrt
import os 
import pickle


def read_track_list(filename_in, keylist=['year', 'month', 'day', 'hour', 'minute','i_cell_center', 'j_cell_center', 'dist_nearest_cell', 'cell_size', 'x_centroid', 'y_centroid', 'r_major', 'r_minor', 'bubble_orientation', 'v_max', 'i_index_cell', 'j_index_cell', 'v_cell']):
    """
    Reads cell track data files.
    """
    print('read ', filename_in)
    tracks = {}
    fileformat_v2 = ".trackslena" in filename_in
    for key in keylist:
        tracks[key]=[]
    with open(filename_in, "rb") as input_file:
        st = os.stat(filename_in)
        file_size = st.st_size       
        if file_size == 0:
            return tracks; 
        eof = False
        while eof == False:
            res = pickle.load(input_file)   
            for key, track_list in tracks.items():
                if fileformat_v2 == True:
                    track_list.extend(res[key])
                else:
                    track_list.append(res[key])                    

            if input_file.tell() == file_size:  
                eof = True
                print("file size: ", round(st.st_size/1000000, 2))
    return tracks

def i_j_indices_to_coord(fh, i_index, j_index):
    """
    Reads lat lon from fh-file (not radolan coordinates!)
    lon: i_index_cell bzw. i_cell_center 
    lat: j_index_cell bzw. j_cell_center
    """
    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    lon = lons[j_index, i_index] # lons(lat, lon)
    lat = lats[j_index, i_index] # lats(lat, lon)
    # print('i_index (lon!!)=',i_index,',j_index',j_index,'converted to lat(°N)=',lat,', lon(°E)=', lon)
    return lat, lon

def windrichtung(dx,dy):
    #calculate direction TO which the wind blows
    alpha_deg = atan2(dy,dx)*180/pi
    winddir_deg = 90-alpha_deg
    if winddir_deg<0: #correction for negative angle (for 4th quadrant incl. wind from E to W)
        winddir_deg+=360
    #calculate direction FROM which the wind blows
    if winddir_deg < 180:
        winddir_deg=winddir_deg+180
    else:
        winddir_deg=winddir_deg-180    
    return winddir_deg

def calculate_euclidean_distance(my_tracks, i):
    """Calculates cumulative euclidean distance of track with index i in km. Cells appearing one timestep have length zero."""

    i_in = my_tracks['i_cell_center'][i]
    # if i_in == []:
    #     pass
    if len(i_in)==1:
        total=0
    else:             
        j_in = my_tracks['j_cell_center'][i]
        k = 1
        total = 0
        while k < len(i_in):
             dist = sqrt((i_in[k]-i_in[k-1])**2 + (j_in[k]-j_in[k-1])**2)
             total += dist
             k+=1
    return total


def get_color(inten):
    """define marker colors"""
    if 0<inten<=10:
        c = "#ecf0fc"
    if 10<inten<=15:
        c = "#d9e1f9"
    if 15<inten<=20:
        c = "#c6d2f6"
    if 20<inten<=25:
        c = "#b3c3f3"
    if 25<inten<=30:
        c = "#a0b4f0"
    if 30<inten<=35:
        c= "#8da5ed"
    if 35<inten<=40:
        c = "#7a96ea"
    if 40<inten<=45:
        c = "#6787e7"
    if 45<inten<=50:
        c = "#5478e4"
    if 50<inten:
        c = "#4169e1"
    return c