# -*- coding: utf-8 -*
"""
Script to test the map-matching algorithm on road-networks and their associated GPS-Logs, adjusted
for the case of multiple logs and the IVMM-algorithm.
"""

import os
import pandas as pd
from RoadNetwork import load_road_network_beijing
from Trip import load_gps_data_beijing, load_gps_data_melbourne
from Rtree import find_candidates, build_rtree_index_edges
from IVMM import ivmm_mapper


def get_optimal_path_edges(candidates, candidates_time, weights, optimal_path, debug=False):
    edge_list = []
    edge_id_list_time = []
    for i in range(len(candidates) - 1):
        to_id = optimal_path[i + 1]
        from_id = optimal_path[i]
        ind = from_id * len(candidates[i + 1]) + to_id
        sub_edge_list = weights[i].iloc[ind]['sp edges']
        # if len(edge_list)>0:
        #    if edge_list[-1]['geometry'] != sub_edge_list[0]['geometry']:
        #        print 'path broken!'
        if debug:
            print(i)
        for j in range(len(sub_edge_list) - 1):
            edge_list.append(sub_edge_list[j])
            edge_id_list_time.append(candidates_time[i])  # zu jeder Kante wird die zugehörige Zeit aus dem GPS-Log gespeichert
            if debug:
                print(sub_edge_list[j]['from'], sub_edge_list[j]['to'])
        if i == len(candidates) - 1:
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
        fWriter.write(opt_route.to_string(header=False, index=False))  # dataframe direkt in txt-file schreiben


def map_osm_edge_id(edges_gpd, opt_route):
    opt_route_osm_edge_id = []
    for edge_id in opt_route:
        opt_route_osm_edge_id.append((edges_gpd.iloc[edge_id]['osm_edge_id'], edges_gpd.iloc[edge_id]['from_to']))
    return opt_route_osm_edge_id


def save_to_file_matching_result_seattle(filename, opt_route):
    with open(filename, 'w') as fWriter:
        fWriter.write('%d\n' % len(opt_route))
        for i in range(len(opt_route)):
            fWriter.write('%d\t%d\n' % (opt_route[i][0], opt_route[i][1]))

def save_to_file_matching_result_beijing(filename, opt_route):
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
    to_crs = 'EPSG:3395'
    optimal_path = []
    candidates = []
    weights = []
    k = 3  # number of candidate points for each gps point
    for i in range(3, 10358): #number of GPS-Logs that are used for the map-matching #TODO: könnte angepasst werden, sodass alle Logs aus einem Ordner gematched werden
        log_number = i

        if data_name is 'Beijing':
            road_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Beijing/complete_osm_map/streets.txt'
            trip_file = '/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/data/Beijing/Beijing_Converted_GPS_Logs/uts_format/' + str(log_number) + '.txt'
            road_graph_utm, gpd_edges_utm = load_road_network_beijing(road_file, crs, to_crs)
            #trip = load_gps_data_beijing(trip_file, crs, to_crs)
            trip = load_gps_data_melbourne(trip_file, crs, to_crs)
            print(trip['geometry'])
        else:
            print('Unknown data name!\n')

        # print('The trip data and road network are loaded!')
        # finding candidates for each gps points using knn query
        edge_idx = build_rtree_index_edges(gpd_edges_utm)

        if algo_name in ['HMM', 'ST', 'IVMM', 'Ant', 'SIMP']:
            # print('The edge r-tree index prepared!')
            candidates, candidates_time = find_candidates(trip, edge_idx, k)
            print("candidates :" + str(candidates))
            # print('Candidates prepared!')

        if algo_name is 'IVMM':
            print('*******IVMM Map-Matching*******')
            optimal_path, weights = ivmm_mapper(road_graph_utm, gpd_edges_utm, trip, candidates, True)
            # visualize_matching_results(trip, candidates, edge_idx, weights, optimal_path, figname='temp.pdf')
        else:
            print('Unknown algorithm name!\n')

        # print optimal_path
        if algo_name in ['HMM', 'ST', 'IVMM', 'Ant', 'SIMP']:
            edge_list, edge_id_list, edge_id_list_time = get_optimal_path_edges(candidates, candidates_time, weights, optimal_path)

        # seq = [data_name, sample_rate,algo_name, 'matching_result.txt']
        seq = [data_name, algo_name, 'matching_result', str(log_number),'.txt']
        Path = "/Users/luismasuchibanez/PycharmProjects/t_drive/map_matching/MapMatchingPython/MapMatchingPython/mapmatching/output"
        connect_str = '_'
        filename = os.path.join(Path, connect_str.join(seq))
        edge_id_list_extended = pd.DataFrame((zip(edge_id_list, edge_id_list_time)), columns=['ID', 'Time'])  # Listen zusammengelegt, edge_id_list durch Zeit ergänzt
        #if data_name is 'Beijing':
            #filename = os.path.join(Path, 'Beijing_IVMM', str(log_number) + '.txt')
        #else:
            #filename = os.path.join(Path, connect_str.join(seq))
        if data_name is 'Beijing':
            #for edge_id in edge_id_list:
                #print("gpd_edges_utm: " + str(gpd_edges_utm.iloc[edge_id]['osm_edge_id']))
            #opt_route_osm_edge_id = map_osm_edge_id(gpd_edges_utm, edge_id_list)
            #save_to_file_matching_result_beijing(filename, opt_route_osm_edge_id)
            print("edge_id_list_extended: " + str(edge_id_list_extended))
            save_to_file_matching_result(filename, edge_id_list_extended)
        else:
            save_to_file_matching_result(filename, edge_id_list)

map_matching_test('Beijing', 'IVMM')

# visualize_matching_results(trip, candidates, edge_idx, weights, optimal_path, figname='temp.pdf')

