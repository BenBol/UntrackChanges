import sys
import re
from os.path import splitext

def add_command(text):
    add_start_pos = [m.start() for m in re.finditer('\\\\added', text)]
    print(add_start_pos)
    add_end_pos = len(add_start_pos)*[None]
    add_strings = len(add_start_pos)*[None]
    n = len(text)
    
    for (i,v) in enumerate(add_start_pos):
        add_end_pos[i], add_strings[i] = find_interior(i,v,7,text)
    
    new_text = '%s' % text
    for i in reversed(range(len(add_start_pos))):
        new_text = new_text[:add_start_pos[i]] + add_strings[i] + new_text[add_end_pos[i]:]
    return new_text

def remove_command(text):
    remove_start_pos = [m.start() for m in re.finditer('\\\\removed', text)]
    remove_end_pos = len(remove_start_pos)*[None]
    remove_strings = len(remove_start_pos)*[None]
    n = len(text)
    
    for (i,v) in enumerate(remove_start_pos):
        remove_end_pos[i], remove_strings[i] = find_interior(i,v,9,text)
    
    new_text = '%s' % text
    for i in reversed(range(len(remove_start_pos))):
        new_text = new_text[:remove_start_pos[i]] + new_text[remove_end_pos[i]:]
    return new_text

def change_command(text):
    change1_start_pos = [m.start() for m in re.finditer('\\\\replaced', text)]
    change1_end_pos = len(change1_start_pos)*[None]
    change1_strings = len(change1_start_pos)*[None]
    change2_start_pos = len(change1_start_pos)*[None]
    change2_end_pos = len(change1_start_pos)*[None]
    change2_strings = len(change1_start_pos)*[None]
    n = len(text)
    
    for (i,v) in enumerate(change1_start_pos):
        # First text
        change1_end_pos[i], change1_strings[i] = find_interior(i,v,10,text)
        # Second text
        change2_start_pos[i] = change1_end_pos[i]
        change2_end_pos[i], change2_strings[i] = find_interior(i,change2_start_pos[i],1,text)
    
    new_text = '%s' % text
    for i in reversed(range(len(change1_start_pos))):
        new_text = new_text[:change1_start_pos[i]] + change1_strings[i] + new_text[change2_end_pos[i]:]
    return new_text

def find_interior(i,v,start,text):
    bracket_start_pos = v + start
    bracket_level = 1
    ind = bracket_start_pos
    comment = False
    print(start, len(text), bracket_start_pos)

    interior_string = ''
    while bracket_level > 0:
        #print(ind)
        #print(text[ind], text[ind-1])
        if text[ind] =='%' and text[ind-1] !='!':
            comment = True
        if r'%s'%text[ind] == '\n':
            comment = False

        if comment ==False:
            if text[ind] == '{':
                bracket_level += 1
            elif text[ind] == '}':
                bracket_level -= 1
        ind += 1
    interior_string = text[v + start:ind-1]
    
    return ind, interior_string, bracket_level

def bracket_balance(text):
    bracket_level = 0
    comment = False
    for i,char in enumerate([r'%s'%i for i in text ]):
        
        if char =='%' and text[i-1] !='!':
            comment = True
            print(True)
        if r'%s'%char == '\n':
            comment = False
            print(False)
        if comment ==False:
            if char == '{':
                bracket_level += 1
            elif char == '}':
                bracket_level -= 1
    return bracket_level

def check_validity(text):
    bracket_level = bracket_balance(text)
    if bracket_level == 0:
        print("Brackets balanced")
        return True
    else:
        raise ValueError(f"Brackets unbalanced, finished with bracket level: {bracket_level}")

def update_text(text):
    text = add_command(text)
    text = remove_command(text)
    text = change_command(text)
    return text

if __name__ == "__main__":
    filename = str(sys.argv[1])

    with open(filename) as f:
        raw_text = f.read()
        
    check_validity(raw_text)
    
    new_text = update_text(raw_text)
    
    filename_split = splitext(filename)
    new_filename = filename_split[0] + '-untrack' + filename_split[1]

    with open(new_filename, 'w') as f:
        f.write(new_text)
    print('Success!')
    
    
    
