import yaml 

def yaml_reader(yamlfile):
    # Read yaml file
    with open(yamlfile, 'r') as file:
        data = yaml.safe_load(file)
    return data

def yaml_link_parser(data):
    
    yaml_data = data.get('havadurumux_links', [])

    return yaml_data

def yaml_provincial_parser(data):

    yaml_data = data.get('English', {})

    return yaml_data

