import os, io
import webcolors
import bokeh
from bokeh.colors import groups as grps
from google.cloud import vision 
from google.cloud.vision import types

# Properties (colours), Labels/Web (what it is), Safe Search (appropriate clothing?)
# Database of your current wardrobe 

class clothes:
    def __init__(self):
        pass
    def categorization(self,labels):        #Clothing Categories should iterate thru a dict like a list 
        # print('Labels:')
        Tops = {'T-shirt','shirt','sleeve'}
        Outerwear = {'Outerwear', 'Jacket', 'Sweater'}
        Bottoms = {'Pants','Leg','Trousers','Skirt','Short'}
        Shoes = {'Footwear','Shoe','Shoes','Boots','Heels'}

        for label in labels:
            # print(label.description)
            # category = ''
            if label.description in Tops:
                category = 'Tops'
            elif label.description in Outerwear:
                category = 'Outerwear'
            elif label.description in Bottoms:
                category = 'Bottoms'
            elif label.description in Shoes:
                category = 'Shoes'
        # print('CAT',category)
        return category

    def colour_seen(self,properties):
        colors = [(int(color.color.red),int(color.color.green),int(color.color.blue),color.pixel_fraction) for color in props.dominant_colors.colors] #triplets
        # print(colors)
        colors.sort(key=lambda x:x[3], reverse = True)
        # print(colors)
        # print(webcolors.rgb_to_name((0,0,0)))
        for color in colors[0:2]:
            try:
                closest_name = actual_name = (webcolors.rgb_to_name(color[0:3]))
            except ValueError:
                min_color = float('inf')
                for hex_val, name in webcolors.css3_hex_to_names.items():
                    r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
                    r_dist = (r_c - color[0])**2 
                    g_dist = (g_c - color[1])**2 
                    b_dist = (b_c - color[2])**2 
                    if color[3]*(r_dist+g_dist+b_dist) < min_color:
                        min_color = color[3]*(r_dist+g_dist+b_dist)
                        closest_name = name 
                        # print(closest_name)
    
        # print('fdas',closest_name)
        return self.colour_group_mapping(closest_name)
    
    def colour_group_mapping(self,closest_name):
        color_grp = ''
        (grps.brown._colors) = map(lambda x:x.lower(), grps.brown._colors)
        (grps.black._colors) = map(lambda x:x.lower(), grps.black._colors)
        (grps.blue._colors) = map(lambda x:x.lower(), grps.blue._colors)
        (grps.cyan._colors) = map(lambda x:x.lower(), grps.cyan._colors)
        (grps.green._colors) = map(lambda x:x.lower(), grps.green._colors)
        (grps.pink._colors) = map(lambda x:x.lower(), grps.pink._colors)
        (grps.orange._colors) = map(lambda x:x.lower(), grps.orange._colors)
        (grps.purple._colors) = map(lambda x:x.lower(), grps.purple._colors)
        (grps.white._colors) = map(lambda x:x.lower(), grps.white._colors)
        (grps.yellow._colors) = map(lambda x:x.lower(), grps.yellow._colors)
        (grps.red._colors) = map(lambda x:x.lower(), grps.red._colors)

        if closest_name in grps.black._colors:
            color_grp = 'black'         
        elif closest_name in grps.brown._colors:
            color_grp = 'brown'
        elif closest_name in grps.blue._colors:
            color_grp = 'blue'
        elif closest_name in grps.cyan._colors:
            color_grp = 'cyan'
        elif closest_name in grps.green._colors:
            color_grp = 'green'
        elif closest_name in grps.pink._colors:
            color_grp = 'pink'
        elif closest_name in grps.orange._colors:
            color_grp = 'orange'
        elif closest_name in grps.yellow._colors:
            color_grp = 'yellow'
        elif closest_name in grps.white._colors:
            color_grp = 'white'
        elif closest_name in grps.red._colors:
            color_grp = 'red'
        elif closest_name in grps.purple._colors:
            color_grp = 'purple'
        # print(color_grp) 
        return color_grp

    def complementary(self,group):
        print(group)
        complements = {
            'black': 'yellow',
            'blue':'yellow',
            'brown':'blue',
            'cyan':'red',
            'green':'brown',
            'orange':'blue',
            'pink':'red',
            'purple':'yellow',
            'red':'cyan',
            'white':'red',
            'yellow':'blue',
        }
        return complements[group]

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccToken.json'

    FILE_NAME = 'timbs.png'
    # FILE_NAME = 'goods_31_420664.jpg' #badd
    # FILE_NAME = '25543_BCW.jpg'
    # FILE_NAME = 'lulu.jpeg' #don't use 
    # FILE_NAME = 'Womens-CBC74-WB-tshirt-416x416.jpg'

    FOLDER_PATH = r'/home/trudie/Desktop/UofTHacks2020/Images'

    with io.open(os.path.join(FOLDER_PATH,FILE_NAME), 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content = content)
    client = vision.ImageAnnotatorClient()
    # print(client)
    #Labels 
    response_lbl = client.label_detection(image=image)
    labels = response_lbl.label_annotations

    #Properties (Colours)
    response_clr = client.image_properties(image=image)
    props = response_clr.image_properties_annotation
    
    article = clothes()
    print(article.categorization(labels))
    # print('fhsad',article.colour_seen(props))
    group = article.colour_seen(props)
    # print(group)
    print('complement:',article.complementary(group))

