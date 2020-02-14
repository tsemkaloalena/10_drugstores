import sys
from geocoder import get_coordinates, search, show_map

toponym_to_find = " ".join(sys.argv[1:])

lat, lon = get_coordinates(toponym_to_find)
address_ll = "{0},{1}".format(lat, lon)
span = "0.005,0.005"

organizations = search(address_ll, span, 'аптека', 10)
points_param = f"{address_ll},vkbkm"
for org in organizations:
    hours = org["properties"]["CompanyMetaData"]["Hours"]['Availabilities'][0]
    if 'TwentyFourHours' in hours and hours['TwentyFourHours'] == True:
        color = "pm2gnl"
    elif 'Intervals' in hours:
        color = "pm2bll"
    else:
        color = "pm2grl"

    point = org["geometry"]["coordinates"]
    org_lat = float(point[0])
    org_lon = float(point[1])
    points_param += f"~{org_lat},{org_lon},{color}"

show_map(address_ll, span, "map", point=points_param)
