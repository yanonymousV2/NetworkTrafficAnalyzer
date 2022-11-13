# Importing required libraries
from cgitb import html
import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx 
import geoip2.database
import pyfiglet
from pyvis.network import Network
 
# banner() function for ASCII Word Art in the terminal. banner() is called at start of every function after 
# clearing screen to stay on top of program
def banner():
    result = pyfiglet.figlet_format("Network Analyzer", font = "starwars") #pyfiglet module helps create the art
    print(result)

# Main menu function. Actual program starts with the start_screen() function
def menu2(data_file):
    banner()
    # menu option
    print("0. Go Back")
    print("1. Show Data")
    print("2. Build Graphs")
    print("3. Trace Suspected Address")
    print("4. Find public IP address GeoLocation")
    
    option_menu2 = int(input("Choose an option: \n")) # Take user choice for menu
    if(option_menu2 == 1):  #Proceeds to show_data() 
        os.system('cls')
        show_data(data_file)
    elif(option_menu2==2):  #Proceeds to graph_data()
        os.system('cls')
        graph_data(data_file)
    elif(option_menu2==3):  #Proceeds to suspect()
        os.system('cls')
        suspect(data_file)  
    elif(option_menu2==4):  #Proceeds to GeoLoc()
        os.system('cls')
        GeoLoc(data_file)
    elif(option_menu2==0):  #Goes back
        os.system('cls')
        start_screen()
    else:                   #If invalid option given by user
        os.system('cls')
        print("Invalid input given. Please try again.")
        os.system('pause')
        os.system('cls')
        menu2(data_file)        
 
#show_data function includes all the text-based diplayable options provided by the program. 
def show_data(data_file):
    banner()
    print("0. Go Back")  
    print("1. Show first 10 readings")
    print("2. Show source and counts")
    print("3. Show destination and counts")
    print("4. Show protocols and counts")
    print("5. Show all traffic of a protocol")

    sub_option2 = int(input("Choose option: "))
    if(sub_option2==1):
        try:
            print(data_file.head(10))   #pandas head() prints the first 10 results of csv 
            os.system('pause')
            os.system('cls')
            show_data(data_file)
        except KeyError:
            os.system('cls')
            banner()
            print("Invalid CSV Format provided. Please upload a valid CSV file of Wireshark export format.")
            os.system('pause')
            os.system('cls')
            start_screen()
    elif(sub_option2==2):
        try:
            sources=data_file.groupby("Source").Source.count()  #groups the csv data by the 'Source' filter and sorts them by their count
            print(sources.sort_values())
            os.system('pause')
            os.system('cls')
            show_data(data_file)
        except KeyError:
            os.system('cls')
            banner()
            print("Invalid CSV Format provided. Please upload a valid CSV file of Wireshark export format.")
            os.system('pause')
            os.system('cls')
            start_screen()
    elif(sub_option2==3):
        try:
            dest=data_file.groupby("Destination").Destination.count() #groups the csv data by the 'Destination' filter and sorts them by their count
            print(dest.sort_values())
            os.system('pause')
            os.system('cls')
            show_data(data_file)
        except KeyError:
            os.system('cls')
            banner()
            print("Invalid CSV Format provided. Please upload a valid CSV file of Wireshark export format.")
            os.system('pause')
            os.system('cls')
            start_screen()
    elif(sub_option2==4):
        try:
            protocol=data_file.groupby("Protocol").Protocol.count() #groups the csv data by the 'Protocol' filter and sorts them by their count
            print(protocol.sort_values())
            os.system('pause')
            os.system('cls')
            show_data(data_file)
        except KeyError:
            os.system('cls')
            banner()
            print("Invalid CSV Format provided. Please upload a valid CSV file of Wireshark export format.")
            os.system('pause')
            os.system('cls')
            start_screen()
    elif(sub_option2==5):
        try:
            ProtoSearch = input("Enter the protocol you want to search (case sensitive): ")  #User input to search all connections for a protocol.
            #Allowing more than default '10' values to be printed
            pd.set_option('display.max_rows', 500)                          
            print(data_file.loc[data_file['Protocol']==ProtoSearch, ["Time","Source","Destination","Protocol","Length"]])
            os.system('pause')
            os.system('cls')
            #Setting values back to 10 (default)
            pd.set_option('display.max_rows', 10)
            show_data(data_file)
        except KeyError:
            os.system('cls')
            banner()
            print("Invalid CSV Format provided. Please upload a valid CSV file of Wireshark export format.")
            os.system('pause')
            os.system('cls')
            start_screen()
    elif(sub_option2==0):   #Goes back to main menu
        os.system('cls')
        menu2(data_file)
    else:
        os.system('cls')
        print("Invalid input given. Please try again.")
        os.system('pause')
        os.system('cls')
        show_data(data_file)

#graph_data() provides options for graphical display of data
def graph_data(data_file):
    banner()
    print("0. Go Back")
    print("1. Display NodeView of traffic")
    print("2. Display EdgeView of traffic")
    print("3. Display network map based on traffic")
    print("4. Display bar graph based on protocol")
    
    sub2_option2=int(input("Choose an option:"))
    if(sub2_option2==1):
        #the map of the network with its start points and end points are first gathered before mapping.  
        network = nx.from_pandas_edgelist(data_file, source="Source", target="Destination", edge_attr=True) #file and other attributes mentioned and stored in network variable.
        print(network.nodes()) # Prints the nodal view of the network map
        os.system('pause')
        os.system('cls')
        graph_data(data_file)
    
    elif(sub2_option2==2):
        network = nx.from_pandas_edgelist(data_file, source="Source", target="Destination", edge_attr=True)
        print(network.edges())  #Prints the edge view of the network map with its source and destination
        os.system('pause')
        os.system('cls')
        graph_data(data_file)
    
    elif(sub2_option2==3):
        network = nx.from_pandas_edgelist(data_file, source="Source", target="Destination", edge_attr=True)
        graph_option=int(input("\n1. Show dynamic graph in HTML View.\n2. Show image graph (.png): "))
        if(graph_option==1):
            net=Network(notebook=False, height='1000px',width='1500px')
            net.from_nx(network)
            # To print out html, we need to extract the directory path as Python can't read relative paths directive
            dirname = os.path.dirname(__file__) #Stores directory path in 'dirname'
            filename = os.path.join(dirname, 'networkgraph.html')   #file is given appended to directory
            net.show(filename)  #full path is called through appending in the 'dirname' and 'filename'
            #print(html_plotter)
            os.system('pause')
            os.system('cls')
            graph_data(data_file)

        elif(graph_option==2):
            network = nx.from_pandas_edgelist(data_file, source="Source", target="Destination", edge_attr=True)
            nx.draw_circular(network, with_labels=True) #network map is drawn with the connections made from the network variable.
            #Network map is plotted (on a new window if running from terminal)
            plt.show()  
            os.system('pause')
            os.system('cls')
            graph_data(data_file)

        else:
            os.system('cls')
            print("Invalid input given. Please try again.")
            os.system('pause')
            os.system('cls')
            graph_data(data_file)       

    elif (sub2_option2==4):
        protocol=data_file.groupby("Protocol").Protocol.count()
        x = list(protocol.index)    #x is the list of protocols 
        y = list(protocol.values)   #y is the list of counts of the protocols
        plt.bar(x, y, width=0.5, color='red')
        plt.plot(x, y,marker='o', color='black')
        plt.xlabel('Protocol')
        plt.ylabel('Communications')
        plt.title('No. of Communications per Protocol')
        plt.show()  #plots the bar graph
        os.system('pause')
        os.system('cls')
        graph_data(data_file)


    elif(sub2_option2==0):
        os.system('cls')
        menu2(data_file)
    
    else:
        os.system('cls')
        print("Invalid input given. Please try again.")
        os.system('pause')
        os.system('cls')
        graph_data(data_file)

# If any suspected address found in network, suspect() marks it separately and displays information about its connections. 
def suspect(data_file):
    banner()
    
    #taking input of suspect
    suspect_ad=input("Enter suspected address: ")
    print("Suspect loaded\n")
    
    #loading network map data (as started in L116)
    network = nx.from_pandas_edgelist(data_file, source="Source", target="Destination", edge_attr=True)
    
    #Suspect source and destination connection information is grapped and stored in two different variable and printed.
    suspect_source_info=data_file.loc[data_file["Source"]==suspect_ad]    #takes the data from the captured file and cross-checks the suspect's connections as source
    suspect_dest_info=data_file.loc[data_file["Destination"]==suspect_ad] #takes the data from the captured file and cross-checks the suspect's connections as destination
    print("Captured source network information of suspect: \n",suspect_source_info)
    print("\n\nCaptured destination network information of suspect: \n",suspect_dest_info)
    
    #prompt to show graphical network map with suspected isolated with its connections.
    suspect_graph_option=input("\nPress Y to show suspect network graph (any other key to go back): ")
    if(suspect_graph_option=='y' or suspect_graph_option=='Y'):
        try:     
            pos=nx.spring_layout(network)   #the spring_layour positions nodes using Fruchterman-Reingold force-directed algorithm
            
            #Safe networks marked isolated and with green colour and other parameters
            nx.draw(network, pos, node_color="green", node_size=300, with_labels=True)
            #Suspect marked in red by program and larger size to show prominence
            options = {"node_size":1000, "node_color":"r"}
            nx.draw_networkx_nodes(network, pos, nodelist=[suspect_ad],**options)
            plt.show()  #Network map is plotted (on a new window if running from terminal)
            os.system('\npause')
            os.system('cls')
            menu2(data_file)
        except nx.exception.NetworkXError:
            os.system('cls')
            banner()
            print("Suspect not in network. Please try again.")
            os.system('pause')
            os.system('cls')
            menu2(data_file)

    
    else:
        os.system('cls')
        menu2(data_file)

#GeoLoc() uses geoip2 and geolite2 tools to locate and return the origin country of a public IP Address
def GeoLoc(data_file):
    banner()
    
    print("\n GEOLOCATION TOOL: \nFinds country location of provided public address using GeoIP2 module.")
    print("NOTE: Requires GeoLite2-Country.mmdb file installed in path. Only works on PUBLIC IP addreses.\n")
    geo_option=input("Print 1 to continue, 0 to go back: ")
    if(geo_option=='1'):

        #loads the GeoLite2-Country.mmdb file into the geoip2 database
        reader = geoip2.database.Reader("E:\\finalYearProj\\Network-Analyzer-master\\netAnal\\GeoLite2-Country.mmdb")
        geoloc_input=input("Enter Public IP Address to locate: ")
        try:
            #Checks in the database for the input public IP address
            response = reader.country(geoloc_input) 
            print(response.country.name)
            os.system('pause')
            os.system('cls')
            menu2(data_file)
            
        #Private IP Address/Reserved IP Address are not located by geoip2 tool and error thrown
        except geoip2.errors.AddressNotFoundError: 
            os.system('cls')
            banner()
            print("Address not in database")
            os.system('pause')
            os.system('cls')        
            GeoLoc(data_file)

        except ValueError:
            os.system('cls')
            banner()
            print("Invalid Input")
            os.system('pause')
            os.system('cls')
            GeoLoc(data_file)

        except OSError:
            os.system('cls')
            banner()
            print("Invalid Input")
            os.system('pause')
            os.system('cls')
            GeoLoc(data_file)

        except TypeError:
            os.system('cls')
            banner()
            print("Invalid Input. Please provide an input")
            os.system('pause')
            os.system('cls')
            GeoLoc(data_file)
            
    elif(geo_option=='0'):
        os.system('cls')
        menu2(data_file)

    else:
        os.system('cls')
        banner()
        print("Invalid input given, please try again.")
        os.system('pause')
        os.system('cls')
        GeoLoc(data_file)

#Prompted exit menu of application
def exit():
    os.system('cls')
    banner()
    
    exit_option=input("Are You Sure?(Y/N): ")
    if(exit_option=='Y' or exit_option=='y'):
        os.system('cls')
        print("Thank you for using Network Analyzer!")
    elif(exit_option=='N' or exit_option=='n'):
        os.system('cls')
        start_screen()
    else:
        exit()

#APPLICATION STARTS WITH THIS FUNCTION
# Start screen with the basic menu options and that leads to other functions of the application. 
def start_screen():
    os.system('cls')
    banner()
    print("\n\t\t***** MENU *****\n")
    print("1. Start")
    print("2. Exit")
    try:
        menu_input=int(input("Enter your choice: "))    
        if(menu_input==1):
            os.system('cls')
            print("Let's start with Network Analysis:\n\n")
            try:
                # Complete file path of CSV file required. Error(L268) if missing file path provided.
                file_path = input("Enter complete csv file path with readings: ")
                # CSV file read and imported as pandas dataframes and stored in data_file variable.
                data_file = pd.read_csv(file_path) 
                os.system('cls')
                print("Data loaded successfully!\n\n")
                menu2(data_file)
            
            except FileNotFoundError:
                os.system('cls')
                banner()
                print("\n\nERROR: FILE NOT FOUND. Enter valid file path.")
                os.system('pause')
                os.system('cls')
                start_screen()

            except PermissionError:
                os.system('cls')
                banner()
                print("\n\nPermission Error: Admin privileges required to run this command. Please try again.")
                os.system('pause')
                os.system('cls')
                start_screen()

            except OSError:
                os.system('cls')
                banner()
                print("\n\nERROR: Invalid argument. Please enter without quote marks.")
                os.system('pause')
                os.system('cls')
                start_screen()
        
        elif(menu_input==2):
            exit()
        
        else:
            os.system('cls')
            banner()
            print("\n\nInvalid Input.")
            os.system('pause')
            os.system('cls')
            start_screen()
    
    # ValueError exception prevents program from crashing when no required inputs are passed
    except ValueError:
        os.system('cls')
        banner()
        print("\n\nPlease enter an input.")
        os.system('pause')
        os.system('cls')
        start_screen()

#Calls the start_screen() and effectively the application
start_screen()
