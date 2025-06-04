import shlex

class House:
    
    def __init__(self,name,type,color,form,p0,p1,p2,p3):
        self.name = name
        self.type = type
        self.color = color
        self.form = form
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

class Road:
    
    def __init__(self,name,type,color,width,form,p0,p1):
        self.name = name
        self.type = type
        self.color = color
        self.width = width
        self.form = form
        self.p0 = p0
        self.p1 = p1

class Vegetation:

    def __init__(self,name,type,color,real_form,ref_form,center,radius):
        self.name = name
        self.type = type
        self.color = color
        self.real_form = real_form
        self.ref_form = ref_form
        self.center = center
        self.radius = radius

Bandelette_list = []

with open("manh_0.sxp","r") as file:
    lines = file.readlines()
    for i,line in enumerate(lines):
        if len(line.split()) == 0 :
            continue
        parts = line.strip().split()
        # parts = shlex.split(line)
        if (parts[0] == '(house') :
            #detecting line
            type = parts[0][1:]
            name = parts[1][1:-1]

            #next line for color
            parts = lines[i+1].strip().split()
            color = parts[1][1:-2]
            
            #next line for form
            parts = lines[i+2].strip().split()
            form = parts[0][1:]

            #4 next line for vertices
            parts = lines[i+3].strip().split()
            p0_x = parts[1]
            p0_y = parts[2][0:-1]
        
            parts = lines[i+4].strip().split()
            p1_x = parts[1]
            p1_y = parts[2][0:-1]
            
            parts = lines[i+5].strip().split()
            p2_x = parts[1]
            p2_y = parts[2][0:-1]

            parts = lines[i+6].strip().split()
            p3_x = parts[1]
            p3_y = parts[2][0:-1]

            h = House(name,type,color,form,(p0_x,p0_y),(p1_x,p1_y),(p2_x,p2_y),(p3_x,p3_y))
            Bandelette_list.append(h)
        elif (parts[0] == '(road') :
            #detecting line
            type = parts[0][1:]
            name = parts[1][1:-1]

            #next line for color
            parts = lines[i+1].strip().split()
            color = parts[1][1:-2]

            #next line for width
            parts = lines[i+2].strip().split()
            width = parts[1][0:-1]

            #next line for form
            parts = lines[i+3].strip().split()
            form = parts[0][1:]

            parts = lines[i+4].strip().split()
            p0_x = parts[1]
            p0_y = parts[2][0:-1]
            
            parts = lines[i+5].strip().split()
            p1_x = parts[1]
            p1_y = parts[2][0:-1]

            r = Road(name,type,color,width,form,(p0_x,p0_y),(p1_x,p1_y))
            Bandelette_list.append(r)
        elif (parts[0] == '(vegetation') :
            #detecting line
            type = parts[0][1:]
            name = parts[1][1:-1]

            #next line for color
            parts = lines[i+1].strip().split()
            color = parts[1][1:-2]

            #next line for real form
            parts = lines[i+2].strip().split()
            real_form = parts[0][1:]

            parts = lines[i+3].strip().split()
            ref_form = parts[0][1:6]
            center_x = parts[2]
            center_y = parts[3][0:-1]
            radius = parts[5][0:-2]

            v = Vegetation(name,type,color,real_form,ref_form,(center_x,center_y),radius)
            Bandelette_list.append(v)


for obj in Bandelette_list:
    print(obj.__class__.__name__, vars(obj))