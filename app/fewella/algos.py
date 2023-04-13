import numpy as np

### Mathematical models taken from:
### J. Desai and U. Tureli, "Evaluating Performance of Various Localization Algorithms in Wireless and Sensor Networks,"
### 2007 IEEE 18th International Symposium on Personal, Indoor and Mobile Radio Communications, 2007, pp. 1-5
###


def maximum_likelihood(gateways):
    ''' 
    gateways: [(x1, y1, r1), (x2, y2, r2), ...]
    returns: (x, y)
    '''

    x_n = gateways[len(gateways) - 1][0]
    y_n = gateways[len(gateways) - 1][1]
    r_n = gateways[len(gateways) - 1][2]

    A = np.zeros((len(gateways) - 1, 2))
    b = np.zeros((len(gateways) - 1, 1))
    for i, gateway in enumerate(gateways[:-1]):
        x_i = gateway[0]
        y_i = gateway[1]
        r_i = gateway[2]
        
        A[i] = [2 * (x_n - x_i), 2 * (y_n - y_i)]
        b[i] = [-(x_i**2) - (y_i**2) + (r_i**2) + (x_n**2) + (y_n**2) - (r_n**2)]

    res = np.linalg.lstsq(A, b, rcond=None)
    return (res[0][0][0], res[0][1][0])


def min_max(gateways):
    '''
    gateways: [(x1, y1, r1), (x2, y2, r2), ...]
    returns: (x, y)
    '''
    l = -np.inf
    r =  np.inf
    t =  np.inf
    b = -np.inf
    for gateway in gateways:
        rad = gateway[2] 
        lg  = gateway[0] - rad
        rg  = gateway[0] + rad
        tg  = gateway[1] + rad
        bg  = gateway[1] - rad
        
        l = max(l, lg)
        r = min(r, rg)
        t = min(t, tg)
        b = max(b, bg)
    
    return ( (l+r)/2, (t+b)/2 )


def test():
    gateways = [
        [
            (2.0, 3.0, 2.5),
            (1.0, 1.0, 1.0),
            (2.5, 1.0, 1.0)
        ],
        [
            (2.0, 3.0, 1.4),
            (1.0, 1.0, 1.0),
            (2.5, 1.0, 1.0)
        ],
        [
            (94, 0,  38),
            (64, 50, 42),
            (0,  0,  68)
        ]
    ]

    for gateway_coords in gateways:
        print(maximum_likelihood(gateway_coords))
        print(min_max(gateway_coords))


if __name__ == "__main__":
    test()