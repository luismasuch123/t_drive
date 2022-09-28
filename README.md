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
t_drive setzt das map-matching des IVMM-Algorithmus um.
***
Falls es Probleme mit dem osmnx-package gibt, muss ein neues environment aufgesetzt werden.
***
In der Klasse Test, sowie Test_Beijing können die Algorithmen auf die road_networks und deren zugehörige GPS-Logs angewendet werden. Bisher wurde nur IVMM getestet.
Unter road_file wird jeweils streets.txt der entsprechenden Stadt hinterlegt. Diese txt_Datei erhält man, indem man eine osm-Karte mit dem osm-parser umwandelt. 
Unter trip_file das GPS-Log bzw. der Ordner mit den GPS-Logs, die gematched werden sollen.
In Test wird immer nur ein Log gematched. In Test_multiple_logs_IVMM können mehrere Logs hintereinander gematched werden.
***
Die Logs können verschiedene Formate besitzen. Im Standard-Format besteht jede Zeile eines Logs aus 4 Spalten. Dem Datum, der Uhrzeit, dem Breitengrad und dem Längengrad.
Beim UTS-Format werden die ersten beiden Spalten zu einer Zahlenfolge zusammengefasst. Aktuell funktioniert der Algorithmus nur in Kombination mit dem UTS-Format und für die auf Melbourne zugeschnittenen Methoden, 
weshalb für alle Städte beim Laden des Straßennetzwerks, sowie der GPS-Logs jeweils die für Melbourne vorgesehenen Methoden genutzt werden. Mithilfe von ConvertBeijingGPSLogFormat.py können GPS-Logs aus 
Beijing (taxi_log_2008_by_id) in das uts_format oder das standard_format umgewandelt werden. 
Das uts_format ist das ursprüngliche Format der GPS-Logs für Melbourne, während das standard_format das Format ist, in dem die Daten für Seattle und Porto gegeben waren. 
Mithilfe von ConvertMelbourneGPSLogFormat.py können die GPS-Logs aus Melbourne in das standard_format übertragen werden. Für die restlichen Städte existieren äquivalente Klassen, die zusammengefasst werden könnten.
Es könnte versucht werden den Algorithmus für die anderen Formate zum Laufen zu bringen und so die vorgesehenen Methoden für die jeweiligen Städte zu nutzen. (Worin genau der Unterschied in den Methoden besteht oder 
ob der Unterschied nur in der Verarbeitung der unterschiedlichen Log-Formate besteht, habe ich nicht näher untersucht) Die Methoden müssten dann gegebenenfalls angepasst werden. Es müsste zum Beispiel berücksichtigt 
werden, dass die Zeitpunkte mit in die edge_id_list (Liste mit besuchten Kanten nach map-matching) geschrieben werden, was vorher nicht der Fall war.
***
In gps_track.to_crs(to_crs) wird eine Projektion von dem Format Längengra - Breitengrad auf ein anderes Koordinatensystem durchgeführt ('EPSG:3395' #projection to WGS84/World MErcator (World - between 80S. and 84N.)), damit Distanzen zwischen zwei Punkten unverzehrt sind. 
Falls Fehler auftreten sollte überprüft werden, ob die Längen- und Breitengrade in den GPS-Logs vertauscht sind.
In https://geopandas.org/en/stable/docs/user_guide/projections.html werden die Projections erklärt.
***
Die Anzahl der Kandidaten, die für jeden GPS-Punkt in Erwägung gezogen werden, kann in map_matching_test() gesetzt werden.
***
Überpüfen, ob der Algorithmus für manuell erfasste GPS-Punkte funktioniert.




