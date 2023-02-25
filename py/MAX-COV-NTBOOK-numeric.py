import numpy as np

# Generate points in moon distribution
# from sklearn.datasets import make_moons
# points,_ = make_moons(Npoints,noise=0.15)

def generate_problem(no_facilities, no_psuppliers, ratio, no_clients = None):
#     no_facilities = 300
    facilities = np.random.rand(no_facilities, 2)
    
    if(no_clients is None):
        no_clients = no_facilities - no_psuppliers
    
    choosen = np.random.choice(len(facilities), (no_psuppliers+no_clients), replace=False)
    idx_psups = choosen[:no_psuppliers]
    idx_clis = choosen[no_psuppliers:]
    
    psuppliers = facilities[idx_psups]
    clients = facilities[idx_clis]
                               
    weights = np.random.randint(1,10, no_clients)
    
    fullclients = list(zip(idx_clis, weights))
    
    return (no_facilities, no_psuppliers, idx_psups, no_clients, fullclients, ratio, facilities)
  
  
  def printf(facilities, idx_psups, idx_clis):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        radius: the radius of circle
    '''
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(8,8))
    
    plt.scatter(facilities[:,0],facilities[:,1],c='C0')
    psups = facilities[idx_psups]
    plt.scatter(psups[:,0],psups[:,1], marker='x', c='C4')
    
    clis = facilities[[ci[0] for ci in idx_clis]]
    ws = [ci[1] for ci in idx_clis]
    
#     plt.scatter(clis[:,0],clis[:,1],c=ws)
    plt.scatter(clis[:,0],clis[:,1], c='C2')
    
    
    
    ax = plt.gca()
    ax.axis('equal')
    ax
#     ax.tick_params(axis='both',left=False, top=False, right=False,
#                        bottom=False, labelleft=False, labeltop=False,
#                        labelright=False, labelbottom=False)



nf, nop, ip, noc, c, r, f = generate_problem(100, 20, 2, 70)
# print(nf, nop, ip, noc, c, r, f)
printf(f, ip, c)

