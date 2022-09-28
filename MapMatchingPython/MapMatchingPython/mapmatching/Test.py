# -*- coding: utf-8 -*
"""
Script to test the map-matching algorithm on road-networks and their associated GPS-Logs.  .
"""


import os

import pandas as pd

from RoadNetwork import load_road_network_graphml, load_road_network_seattle, load_road_network_melbourne
from Trip import load_gps_data_seattle, load_gps_data_porto, load_gps_data_melbourne
from Rtree import find_candidates, build_rtree_index_edges
from AntMapper import ant_mapper
from Visualize import visualize_matching_results
from STMatching import st_mapper
from IVMM import ivmm_mapper
from HMM import hmm_mapper
from SIMP import simp_mapper
from OBRHMM import obr_mapper_v1



def get_optimal_path_edges(candidates, candidates_time, weights, optimal_path, debug=False):
    edge_list = []
    edge_id_list_time = []
    for i in range(len(candidates)-1):
        to_id = optimal_path[i+1]
        from_id = optimal_path[i]
        ind = from_id * len(candidates[i+1]) + to_id
        sub_edge_list = weights[i].iloc[ind]['sp edges']
        # if len(edge_list)>0:
        #    if edge_list[-1]['geometry'] != sub_edge_list[0]['geometry']:
        #        print 'path broken!'
        if debug:
            print(i)
        for j in range(len(sub_edge_list)-1):
            edge_list.append(sub_edge_list[j])
            edge_id_list_time.append(candidates_time[i])  # zu jeder Kante wird die zugehörige Zeit aus dem GPS-Log gespeichert
            if debug:
                print(sub_edge_list[j]['from'], sub_edge_list[j]['to'])
        if i == len(candidates)-1:
            edge_list.append(sub_edge_list[-1])
            if debug:
                print(sub_edge_list[-1]['from'], sub_edge_list[-1]['to'])
    edge_id_list = []
    for edge in edge_list:
        edge_id_list.append(edge.name)
    return edge_list, edge_id_list, edge_id_list_time


def save_to_file_matching_result(filename, opt_route):
    with open(filename, 'w') as fWriter:
        fWriter.write('%d\n' % len(opt_route))
        ''' ursprünglich nur edge_id_list ohne time reingeschrieben
        for i in range(len(opt_route)):
            fWriter.write('%d\n' % opt_route[i])
        '''
        fWriter.write(opt_route.to_string(header=False, index=False)) #dataframe direkt in txt-file schreiben


def map_osm_edge_id(edges_gpd, opt_route):
    opt_route_osm_edge_id = []
    for edge_id in opt_route:
        opt_route_osm_edge_id.append((edges_gpd.iloc[edge_id]['osm_edge_id'], edges_gpd.iloc[edge_id]['from_to']))
        #opt_route_osm_edge_id.append((edges_gpd.iloc[edge_id]['Edge_ID'], edges_gpd.iloc[edge_id]['from'], edges_gpd.iloc[edge_id]['to']))
    return opt_route_osm_edge_id


def save_to_file_matching_result_seattle(filename, opt_route):
    with open(filename, 'w') as fWriter:
        fWriter.write('%d\n' % len(opt_route))
        for i in range(len(opt_route)):
            fWriter.write('%d\t%d\n' % (opt_route[i][0], opt_route[i][1]))

def save_to_file_matching_result_melbourne(filename, opt_route):
    with open(filename, 'w') as fWriter:
        fWriter.write('%d\n' % len(opt_route))
        for i in range(len(opt_route)):
            fWriter.write('%d\t%d\n' % (opt_route[i][0], opt_route[i][1]))


def map_matching_test(data_name, algo_name):
    """
    :param data_name: trajectory data name
    :param algo_name: algorithm name
    :return:
    """
    print('Set data name as %s' % data_name)
    print('Set algorithm name as %s' % algo_name)
    crs = 'EPSG:4326'
    to_crs = 'EPSG:3395' #projection to WGS84/World MErcator (World - between 80S. and 84N.)
    optimal_path = []
    candidates = []
    weights = []
    k = 3  # number of candidate points for each gps point
    if data_name is 'Seattle':
        #aktuell road_file und road_graph_utm, usw. auf Melbourne-Format angepasst
        #road_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Seattle/road_network.txt'
        road_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Seattle/complete_osm_map_osm_test/streets.txt'
        trip_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Seattle/Seattle_Converted_GPS_Logs/uts_format/gps_track.txt'
        #road_graph_utm, gpd_edges_utm = load_road_network_seattle(road_file, crs, to_crs)
        road_graph_utm, gpd_edges_utm = load_road_network_melbourne(road_file, crs, to_crs)
        #trip = load_gps_data_seattle(trip_file, crs, to_crs)
        trip = load_gps_data_melbourne(trip_file, crs, to_crs)

       
    elif data_name is 'Melbourne':
        road_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Melbourne/complete-osm-map/streets.txt'
        trip_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Melbourne/GPS_Logs/UTS_format/gps_track_test.txt'
        #trip_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Melbourne/GPS_Logs/standard_format/gps_track.txt'
        road_graph_utm, gpd_edges_utm = load_road_network_melbourne(road_file, crs, to_crs)
        trip = load_gps_data_melbourne(trip_file, crs, to_crs)
        print(trip['geometry'])
  

    elif data_name is 'Porto':
        # aktuell road_file und road_graph_utm, usw. auf Melbourne-Format angepasst
        #road_file = 'porto.graphml'
        #road_folder = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Porto'
        road_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Porto/map-porto/streets.txt'
        #trip_folder = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Porto/trips'
        #trip_file = 'trip_1.txt'
        trip_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Porto/GPS_Logs_converted/uts_format/0.txt'
        #road_graph_utm, gpd_edges_utm, wgs_crs, utm_crs = load_road_network_graphml(road_folder, road_file)
        #trip = load_gps_data_porto(trip_folder+'/'+trip_file, wgs_crs, utm_crs)
        #sample_rate=trip.iloc[1]["timestamp"]-trip.iloc[0]["timestamp"]
        road_graph_utm, gpd_edges_utm = load_road_network_melbourne(road_file, crs, to_crs)
        trip = load_gps_data_melbourne(trip_file, crs, to_crs)

    else:
        print('Unknown data name!\n')

    # print('The trip data and road network are loaded!')
        # finding candidates for each gps points using knn query
    edge_idx = build_rtree_index_edges(gpd_edges_utm)

    if algo_name in ['HMM', 'ST', 'IVMM', 'Ant', 'SIMP']:
        # print('The edge r-tree index prepared!')
        candidates, candidates_time = find_candidates(trip, edge_idx, k)
        # print('Candidates prepared!')

    if algo_name is 'Ant':
        print('*******Ant Mapper********')
        x_min, y_min, x_max, y_max = gpd_edges_utm.total_bounds  # bounding box of the road network
        optimal_path, weights = ant_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, x_min, y_min)
    elif algo_name is 'ST':
        print('*******ST Map-Matching*********')
        optimal_path, weights = st_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, True)
    elif algo_name is 'IVMM':
        print('*******IVMM Map-Matching*******')
        optimal_path, weights = ivmm_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, True)
        visualize_matching_results(trip, candidates, edge_idx, weights, optimal_path, figname='temp.pdf')
    elif algo_name is 'HMM':
        print('*******HMM Map-Matching**********')
        optimal_path, weights = hmm_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, True)
    # visualize_matching_results(trip, candidates, edge_idx, weights_st, optimal_path_st, fig_name)
    elif algo_name is 'OBRHMM':
        print('*******OBRHMM Map-Matching*******')
        if data_name is 'Seattle':
            d_error = 20  # error range of gps positioning
        elif data_name is 'Melbourne':
            d_error = 10
        a_error = 45  # angle difference bound
        edge_id_list = obr_mapper_v1(road_graph_utm, gpd_edges_utm, trip, d_error, a_error, True)
        # print optimal_path
    elif algo_name is 'SIMP':
        print('******SIMP Map-Matching*********')
        optimal_path, weights, filtered_candidates = \
            simp_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, debug=False)
        candidates = filtered_candidates
    else:
        print('Unknown algorithm name!\n')

    # print optimal_path
    if algo_name in ['HMM', 'ST', 'IVMM', 'Ant', 'SIMP']:
        edge_list, edge_id_list, edge_id_list_time = get_optimal_path_edges(candidates, candidates_time, weights, optimal_path)
    # seq = [data_name, sample_rate,algo_name, 'matching_result.txt']
    seq = [data_name, algo_name, 'matching_result.txt']
    Path="/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching//MapMatchingPython/MapMatchingPython/mapmatching/output"
    connect_str = '_'
    filename = os.path.join(Path,connect_str.join(seq))
    edge_id_list_extended = pd.DataFrame((zip(edge_id_list, edge_id_list_time)), columns = ['ID', 'Time']) #Listen zusammengelegt, edge_id_list durch Zeit ergänzt
    if data_name is 'Seattlee': #TODO: was bewirkt erster der beiden Schritte in if entgegen dem einzelnen Schritt in else?
        opt_route_osm_edge_id = map_osm_edge_id(gpd_edges_utm, edge_id_list)
        save_to_file_matching_result_seattle(filename, opt_route_osm_edge_id)
    else:
        save_to_file_matching_result(filename, edge_id_list_extended)
        print("edge_id_list_extended: " + str(edge_id_list_extended))


# data name includes:
# ['Seattle', 'Melbourne', 'Porto']
# algorithms name includes:
# ['HMM', 'ST', 'IVMM', 'Ant', 'SIMP', 'OBRHMM']


# map_matching_test('Seattle', 'OBRHMM')
# map_matching_test('Seattle', 'SIMP')
# map_matching_test('Melbourne', 'OBRHMM')
# map_matching_test('Melbourne', 'SIMP')
#map_matching_test('Melbourne', 'Ant')
map_matching_test('Porto', 'IVMM')

# map_matching_test('Porto', 'Ant')
# map_matching_test('Porto', 'IVMM')
# map_matching_test('Porto', 'ST')
# map_matching_test('Porto', 'HMM')
# map_matching_test('Porto', 'OBRHMM')
#visualize_matching_results(trip, candidates, edge_idx, weights, optimal_path, figname='temp.pdf')

