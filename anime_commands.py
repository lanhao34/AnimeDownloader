import pickle


def read(string):
    try:
        F = open(string, 'r')
        data = pickle.load(F)
        F.close()
    except Exception, e:
        print e
        data = []
    return data


def write(string, data):
    F = open(string, 'w')
    pickle.dump(data, F)
    F.close()