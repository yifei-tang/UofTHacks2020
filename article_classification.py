import os, io, webcolors, bokeh
from bokeh.colors import groups as grps
from google.cloud import vision 
from google.cloud.vision import types

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
        colors = [(int(color.color.red),int(color.color.green),int(color.color.blue),color.pixel_fraction) for color in properties.dominant_colors.colors] 
        colors.sort(key=lambda x:x[3], reverse = True)

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
        return color_grp

    def complementary(self,group):
        complements = {
            'black': ['black','blue','brown','cyan','green','orange','pink','purple','red','white','yellow'],
            'blue': ['black','white','purple','orange'],
            'brown':['black','white','blue'],
            'cyan':['red','white','black','purple'],
            'green':['black','white','purple','brown'],
            'orange':['black','white','brown'],
            'pink':['black','white','purple'],
            'purple':['black','white','pink'],
            'red':['black','white','cyan','blue'],
            'white':['black','blue','brown','cyan','green','orange','pink','purple','red','yellow'],
            'yellow':['black','white','blue'],
        }
        return complements[group]

# Call the following function 
def article_class(url):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccToken.json'

    # FILE_NAME = 'timbs.png'
    # FILE_NAME = 'goods_31_420664.jpg' #badd
    # FILE_NAME = '25543_BCW.jpg'
    # FILE_NAME = 'lulu.jpeg' #don't use 
    # FILE_NAME = 'Womens-CBC74-WB-tshirt-416x416.jpg'
    # FOLDER_PATH = r'/home/trudie/Desktop/UofTHacks2020/Images'

    client = vision.ImageAnnotatorClient()

    request = {
        'source' : {'image_uri':url},
    }

    response_lbl = client.label_detection(request)
    response_clr = client.image_properties(request)
    labels = response_lbl.label_annotations    #Labels 
    props = response_clr.image_properties_annotation    #Properties (Colours)

    article = clothes()
    group = article.colour_seen(props)

    return article.categorization(labels), article.complementary(group)    #type, recommend colours [str]

# Testing 
# url = "https://images.footlocker.com/is/image/EBFL2/55045000_a1?wid=640&hei=640&fmt=png-alpha" 
# print(article_class(url))