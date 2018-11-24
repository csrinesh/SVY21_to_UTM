from conversion import from_latlon
from sy21_lat_lon import SVY21
import os
import glob
import datetime
import sys

start = datetime.datetime.now()
s = SVY21()

def func(inp='input', out='output_utm'):
    
    if os.path.isdir(inp):
        input_path = os.path.join(inp,'*.asc')
        for filepath in glob.glob(input_path):
            
            filename = filepath.split('\\')[-1]
            
            with open(filepath) as f:
                data = f.read()
                f.close()
            
            split_data = data.split('\n')
            
            xllcorner = split_data[2].split(' ')[1]
            yllcorner = split_data[3].split(' ')[1]
            
            b1, b2 = s.computeLatLon(float(yllcorner), float(xllcorner))
            
            utm1, utm2, letter, char = from_latlon(b1,b2)
            
            data1 = [w.replace('xllcorner ' + xllcorner, 'xllcorner ' + str(utm1)) for w in split_data]
            data1 = [w.replace('yllcorner ' + yllcorner, 'yllcorner ' + str(utm2)) for w in data1]
            
            data1 = '\n'.join(data1)
            try:
                os.mkdir(out)
                print("Directory  Created ") 
            except:
                pass  
            
            output_path = os.path.join(out, filename)
            f = open(output_path, 'w')    
            f.write(data1)
            f.close()
            print(f'Writing {filename} is complete')
        end = datetime.datetime.now()
        print('Total running time in seconds =',(end-start).total_seconds())    
    else:
        print('The input file does not exist!')

if __name__ == '__main__':        
    
    try:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        func(input_folder, output_folder)
    except IndexError:
        print('Input and Output arguments are not specified. Using default!')    
        func()
        