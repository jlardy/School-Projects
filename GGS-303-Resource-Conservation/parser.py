def get_indexes(s):
    s = s.lstrip() # remove the spaces to the left
    try:
        return s[:s.index(' ')] , s[s.index(' '):] #return the value until the next whitespace and the string without the current
    except:
        return s.rstrip(), '' #once we're done return and empty string and the last value without newline

def parse_string(s):
    data = [] 
    while len(s): # while there is still a string parse it
        current, s = get_indexes(s)
        if current: data.append(current) # the last value is sometimes empty so only save good values
    return data 

use_first = False
fname = 'ch4_mm_gl'    

output = None # no idea how many columns
with open(fname+'.txt') as txt:
    for i, line in enumerate(txt):
        if line[0] == '#': continue #pass on all the garbage 

        if not output: # if output hasnt been initialized create a dict with number of columns
            output = {i:[val] for i, val in enumerate(parse_string(line))} 
        else:
            for i, val in enumerate(parse_string(line)): #otherwise just add to those columns
                output[i].append(val)


# save as a csv
import pandas as pd 
out = pd.DataFrame(output)

if use_first:
    # drop the repeated rows and set the column titles to the first row
    out = out.drop_duplicates()
    out.columns = out.iloc[0]
    out = out[1:].reset_index(drop=True)


out.to_csv(fname+'.csv')