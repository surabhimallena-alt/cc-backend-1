import copy
import argparse


endpoint_dict = {} 
#{"/courses":{"count":0,'"total_response_time":response_time,"max_response_time":response_time}}
total_requests = 0
status_code_dict = {}
ids = []
batch_dict = {'2022':0,'2023':0,'2024':0,'2025':0}
strategy_dict = {'Heuristic Backtracking':0, 'Iterative Random Sampling':0}
total_generated = 0
times_generated = 0
max_endpoint1 = ""
max_endpoint2 = ""

parser = argparse.ArgumentParser(description="Generate segments of the report.")
parser.add_argument("--endpoints", action="store_true", help="Generate endpoint popularity report")
parser.add_argument("--metrics", action="store_true", help="Generate performance metrics")
parser.add_argument("--insights", action="store_true", help="Generate application insights")
parser.add_argument("--ids", action="store_true", help="Generate ID analysis")
args = parser.parse_args()


def request_line(line):
    global endpoint_dict
    global total_requests
    global status_code_dict

    total_requests += 1
    line_list = line.split()[3::]
    #line_list -> ['POST','/courses','200','460.384Âµs']

    response_time = float(line_list[-1][:-3])/1000
    endpoint = line_list[1]
    if endpoint not in endpoint_dict:
        endpoint_dict[endpoint]={"count":1,"total_response_time":response_time,\
                                      "max_response_time":response_time}
    else:
        endpoint_dict[endpoint]["count"]+=1
        endpoint_dict[endpoint]["total_response_time"]+=response_time
        if response_time > endpoint_dict[endpoint]["max_response_time"]:
            endpoint_dict[endpoint]["max_response_time"] = response_time

    status_code = line_list[2]
    if status_code not in status_code_dict:
        status_code_dict[status_code] = 1
    else:
        status_code_dict[status_code] += 1

def id_line(line):
    global ids
    global batch_dict

    line_list = line.split()[3::]
    #line_list -> ['router:','/courses','[2024A8PS0885P]']
    id_no = line_list[2][1:-1] #removing square brackets
    year = id_no[:4]
    if id_no not in ids:
        ids.append(id_no)
        batch_dict[year] += 1
        

def strategy_line(line):
    global strategy_dict
    if 'Heuristic' in line:
        strategy_dict["Heuristic Backtracking"] += 1
    else:
        strategy_dict["Iterative Random Sampling"] += 1


def generate_line(line):
    global total_generated
    global times_generated

    line_list = line.split()[3::]
    #line_list -> ['---','Generation', 'Complete:','Found', \
    # '1','timetables','in','pool,','returning','1.','---']
    times_generated += 1
    generated = int(line_list[4])
    total_generated += generated

def calc_avg_max_time():
    global total_requests
    global endpoint_dict
    global max_endpoint1
    global max_endpoint2
    global perc1, perc2, max1, max2

    max_endpoint1 = max(endpoint_dict, key = lambda endpoint: endpoint_dict[endpoint]['count'])
    max1 = endpoint_dict[max_endpoint1]['count']
    perc1 = round((max1/total_requests*100),1)

    endpoint_dict2 = copy.deepcopy(endpoint_dict)
    del endpoint_dict2[max_endpoint1]

    max_endpoint2 = max(endpoint_dict2, key = lambda endpoint: endpoint_dict2[endpoint]['count'])
    max2 = endpoint_dict2[max_endpoint2]['count']
    perc2 = round((max2/total_requests*100),1)


def print_traffic_analysis():
    print("-"*55)
    print("TRAFFIC & USAGE ANALYSIS")
    print("-"*55)

    global total_requests 
    print(f"Total API Requests Logged: {total_requests}")
    print()

    #Endpoint Popularity
    global endpoint_dict
    global max_endpoint1
    global max_endpoint2
    global perc1, perc2, max1, max2

    '''max_endpoint1 = max(endpoint_dict, key = lambda endpoint: endpoint_dict[endpoint]['count'])
    max1 = endpoint_dict[max_endpoint1]['count']
    perc1 = round((max1/total_requests*100),1)

    endpoint_dict2 = copy.deepcopy(endpoint_dict)
    del endpoint_dict2[max_endpoint1]

    max_endpoint2 = max(endpoint_dict2, key = lambda endpoint: endpoint_dict2[endpoint]['count'])
    max2 = endpoint_dict2[max_endpoint2]['count']
    perc2 = round((max2/total_requests*100),1)'''

    print("Endpoint Popularity:")
    print(f"    - {max_endpoint1}: {max1} requests ({perc1})")
    print(f"    - {max_endpoint2}: {max2} requests ({perc2})")
    print()

    #print_status_codes
    global status_code_dict

    print("HTTP Status Codes:")
    for code in status_code_dict:
        print(f"    - {code}: {status_code_dict[code]} times")
    

def print_metrics():
    global endpoint_dict
    #{"/courses":{"count":0,'"total_response_time":response_time,"max_response_time":response_time}}
    global max_endpoint1
    global max_endpoint2

    avg_time1 = round((endpoint_dict[max_endpoint1]["total_response_time"]/endpoint_dict[max_endpoint1]["count"]),2)
    max_time1 = round(endpoint_dict[max_endpoint1]["max_response_time"],2)
    avg_time2 = round((endpoint_dict[max_endpoint2]["total_response_time"]/endpoint_dict[max_endpoint2]["count"]),2)
    max_time2 = round(endpoint_dict[max_endpoint2]["max_response_time"],2)

    print("-"*55)
    print("PERFORMANCE METRICS")
    print("-"*55)
    print(f"Endpoint: {max_endpoint1}")
    print(f"    - Average Response Time: {avg_time1} ms")
    print(f"    - Max Response Time: {max_time1} ms")
    print(f"Endpoint: {max_endpoint2}")
    print(f"    - Average Response Time: {avg_time2} ms")
    print(f"    - Max Response Time: {max_time2} ms")
    

def print_app_insights():
    global status_code_dict
    global total_generated
    global times_generated

    print("-"*55)
    print("APPLICATION-SPECIFIC INSIGHTS")
    print("-"*55)
    print("Timetable Generation Strategy Usage:")
    print(f"    - Heuristic Backtracking: {strategy_dict['Heuristic Backtracking']} times")
    print(f"    - Iterative Random Sampling: {strategy_dict['Iterative Random Sampling']} times")
    print()
    print(f"Average Timetables Found per /generate call: {round(total_generated/times_generated,2)}")
    print(f"Total number of timetables generated: {total_generated}")

def print_id_analysis():
    global batch_dict
    global ids

    print("-"*55)
    print("UNIQUE ID ANALYSIS")
    print("-"*55)
    print(f"Total Unique IDs found: {len(ids)}")
    print(f"Batch of 2022: {batch_dict['2022']} unique IDs")
    print(f"Batch of 2023: {batch_dict['2023']} unique IDs")
    print(f"Batch of 2024: {batch_dict['2024']} unique IDs")
    print(f"Batch of 2025: {batch_dict['2025']} unique IDs")


timetable = open("timetable.log", "r")

for line in timetable:
    line = line.strip()
    if "POST" in line:
        request_line(line)
    elif line.endswith("]"):
        id_line(line)
    elif "Strategy" in line:
        strategy_line(line)
    elif "Generation" in line:
        generate_line(line)
    else:
        continue

calc_avg_max_time()


'''print_traffic_analysis()
print_metrics()
print_app_insights()
print_id_analysis()'''

any_flag = args.endpoints or args.metrics or args.insights or args.ids

if args.endpoints or not any_flag:
    print_traffic_analysis()

if args.metrics or not any_flag:
    print_metrics()

if args.insights or not any_flag:
    print_app_insights()

if args.ids or not any_flag:
    print_id_analysis()
