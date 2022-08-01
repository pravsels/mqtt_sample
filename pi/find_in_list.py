import requests 

min_list = ['small', 'smaller', 'tiny', 'tinier', 'little', 'littler', 'miniaturize']
max_list = ['large', 'larger', 'big', 'bigger', 'huge', 'huger', 'enormous', 'colossal', 'massive', 'enlarge']
player_list = ['mate', 'partner', 'colleague', 'ally', 'teammate']
min_list = set(min_list)
max_list = set(max_list)
player_list = set(player_list)

def find_in_list(sentence):
    make_small = False
    make_big = False
    player = False

    for word in sentence.split():
        if word in min_list:
            make_small = True
        if word in max_list:
            make_big = True
        if word in player_list:
            player = True

    if player and make_small:
        # submit GET request to /make_small
        print('making your team mate in VR smaller!')
        r = requests.get("http://www.google.com")
        #print(r.json())
    elif player and make_big:
        # submit GET request to /make_big
        print('making your team mate in VR bigger')
        r = requests.get("http://www.google.com")
        #print(r.json())
    else:
        print('I do not understand!')

while True:
    sentence = input('Tell me what to do..  ')
    find_in_list(sentence)
