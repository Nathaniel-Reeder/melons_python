import csv

class Melon():

    def __init__(self, melon_id, common_name, price, image_url, color, seedless):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def __repr__(self):
        '''Convenience method to show information about melon in console'''

        return (
            f"<Melon: {self.melon_id}, {self.common_name}>"
        )

    def price_str(self):
        '''Return price formatted as a string $x.xx'''

        return f"${self.price:.2f}"

melon_dict = {}

with open('melons.csv', 'r', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    for item in reader:
        melon_id = item['melon_id']
        melon = Melon(
            melon_id, 
            item['common_name'],
            float(item['price']),
            item['image_url'],
            item['color'],
            eval(item['seedless'])
        )
        melon_dict[melon_id] = melon

def get_melon_by_id(id):
    return melon_dict[id]
    

def get_melon_list():
    return list(melon_dict.values())
