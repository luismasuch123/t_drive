# MapMatching Algorithms 
***
Map matching is the processing of recognizing the true driving route in the road network accroding to discrete GPS sampling datas . It is a necessary processing step for many relevant applications such as GPS trajectory data analysis and position analysis.  
**Author: Shenglong Yan**    
**Created: 23/02/2019**  

# Main Contributions
***
**I have exposed several common map matching algorithms and some test datas for future reserach.**  

1.Hidden Markov Map Matching Through Noise and Sparseness(HMMM)

2.Map-matching for Low-sampling-rate GPS Trajectories(ST-matching)

3.An Interactive-Voting Based Map Matching Algorithm(IVMM)

4.AntMapper: An Ant Colony-Based Map Matching Approach for Trajectory-Based Applications(AntMapper)

5.Spatio-temporal trajectory simplification for inferring travel paths(SIMP)

6.Robust inferences of travel paths from GPS trajectories(OBRHMM)  

 
# Dependency
***
python 2.7(jupyter notebook,sublime text4)  
1.pandas/geoPandas  
2.numpy  
3.shapely  
4.networkx  
5.osmnx  
6.Rtree  
7.matplotlib  

#Anmerkungen Luis
***
Falls es Probleme mit dem osmnx-package gibt, muss ein neues environment aufgesetzt werden.
***
In der Klasse Test, sowie Test_Beijing können die Algorithmen auf die road_networks und deren zugehörige GPS-Logs angewendet werden. Bisher wurde nur IVMM getestet.
Unter road_file wird jeweils streets.txt der entsprechenden Stadt hinterlegt. Diese txt_Datei erhält man, indem man eine osm-Karte mit dem osm-parser umwandelt. 
Unter trip_file das GPS-Log bzw. der Ordner mit den GPS-Logs, die gematched werden sollen.
Aktuell wird immer nur ein Log gematched. Später sollen dann mehrere Logs hintereinander gematched werden.
***
Aktuell läuft das map-matching nur für Melbourne und das uts_format. Außerdem terminiert der Algorithmus nur für verkürzte GPS-Logs (z.B. gps_track_test.txt). 
Die Umwandlung in das standard_format verschafft keine Abhilfe. Mithilfe von ConvertBeijingGPSLogFormat.py können GPS-Logs aus Beijing (taxi_log_2008_by_id) in das uts_format oder das standard_format umgewandelt werden. 
Das uts_format ist das ursprüngliche Format der GPS-Logs für Melbourne, während das standard_format das Format ist, in dem die Daten für Seattle und Porto gegeben waren. 
Mithilfe von ConvertMelbourneGPSLogFormat.py können die GPS-Logs aus Melbourne in das standard_format übertragen werden.
***
gps_track.to_crs(to_crs) liefert Error für Beijing und Seattle. Dies könnte der Grund für den NodeNotReachable-Error sein.
Wenn beispielsweise für Beijing versucht wird, die Logs im uts_format zu laden und gps_track.to_crs(to_crs) in load_gps_data_beijing() nicht auskommentiert ist, erhält man den ValueError "The second input geometry is empty".
Debugging nicht möglich. ("AttributeError: module 'posixpath' has no attribute 'sep'")
NodeNotReachable reproduzierbar mit Beijing, standard_format und load_gps_data_beijing() in Test_Beijing_IVMM.py.
Auch für Melbourne erhält man NodeNotReachable, wenn in load_gps_data_melbourne gps_track.to_crs(crs) statt gps_track.to_crs(to_crs) aufgerufen wird.
In https://geopandas.org/en/stable/docs/user_guide/projections.html werden die Projections erklärt.
***
Die Anzahl der Kandidaten, die für jeden GPS-Punkt in Erwägung gezogen werden, kann in map_matching_test() gesetzt werden.
***
Unklar, worin Fehler genau liegt. Selbst wenn für Melbourne manuell GPS-Daten erfasst werden, erhält man NodeNotReachable.




