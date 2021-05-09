# Source : https://www.normalesup.org/~doulcier/teaching/modeling/bistable_systems.html
from functools import partial 
from collections import defaultdict 
import numpy as np # Numerical computing library
import matplotlib.pyplot as plt # Plotting library
import scipy.integrate #Integration library
from mpl_toolkits.mplot3d import axes3d #Used for the 3d bifurcation plot
import matplotlib.patches as mpatches #used to write custom legends

# Exercise: 
# - Simulate this system using scipy.integrate.odeint
# - Draw the trajectories using matplotlib.pyplot.plot

# We will look at those set of parameters
scenarios = [{'alpha':1, 'beta':2}, {'alpha':1, 'beta':10}]
#scenarios = [{'alpha':1, 'beta':10}]
#for k in range(2,3):
#    scenarios.append({'alpha':10**k, 'beta': 1 })

# On this timespan
time = np.linspace(0, 30, 10000)

# Here is a list of interesting initial conditions:
initial_conditions = [(.1,1), (2,2),(1,1.3),(2,3),(2,1),(1,2)]

def cellular_switch(y,t,alpha, beta):
    """ ODE system modeling Gardner's bistable cellular switch
    Args:
        y (array): (concentration of u, concentration of v)
        t (float): Time
        alpha (float): maximum rate of repressor synthesis 
        beta (float): degree of cooperative behavior.
    Return: dy/dt
    """
    u, v = y # you can use y[0], y[1] instead. 
    return np.array([ np.exp(-v)*(alpha*(u**2))/(1+beta*(u**2)) ,
                     u*v])

def cellular_switch_orig(y,t,alpha, beta):
    """ ODE system modeling Gardner's bistable cellular switch
    Args:
        y (array): (concentration of u, concentration of v)
        t (float): Time
        alpha (float): maximum rate of repressor synthesis 
        beta (float): degree of cooperative behavior.
    Return: dy/dt
    """
    u, v = y # you can use y[0], y[1] instead. 
    return np.array([(alpha/(1+v**beta)) - u ,
                     (alpha/(1+u**beta)) - v])

def plot_flow(ax, param, uspace, vspace):
    """Plot the flow of the symmetric cellular switch system"""
    X,Y = np.meshgrid(uspace,vspace)
    a = cellular_switch([X,Y],0,**param)
    ax.streamplot(X,Y,a[0,:,:], a[0,:,:], color=(0,0,0,.1))
    ax.set(xlim=(uspace.min(),uspace.max()), ylim=(vspace.min(),vspace.max()))

def findroot(func, init): 
    """ Find root of equation function(x)=0
    Args:
        - the system (function),
        - the initial values (type list or np.array)

    return: correct equilibrium (type np.array) 
            if the numerical method converge or return nan
    """
    sol, info, convergence, sms = scipy.optimize.fsolve(func, init, full_output=1)
    if convergence == 1:
        return sol
    return np.array([np.nan]*len(init))

def find_unique_equilibria(flow, starting_points):
    '''Return the list of unique equilibria of a flow 
    starting around starting_points'''
    equilibria = [] 
    roots = [findroot(flow, init) 
             for init in starting_points]
    # Only keep unique equilibria 
    for r in roots:
        if (not any(np.isnan(r)) and
            not any([all(np.isclose(r, x)) for x in equilibria])):
            equilibria.append(r)
    return equilibria

def jacobian_cellular_switch(u,v, alpha, beta):
    """ Jacobian matrix of the ODE system modeling Gardner's bistable cellular switch
    Args:
        u (float): concentration of u, 
        v (float): concentration of v,
        alpha (float): maximum rate of repressor synthesis, 
        beta (float): degree of cooperative behavior.
    Return: np.array 2x2"""
    return - np.array([[1, alpha*beta*v**(beta-1) / (1+v**beta)**2  ],
                       [alpha*beta*u**(beta-1) / (1+u**beta)**2, 1]])

def stability(jacobian):
    """ Stability of the equilibrium given its associated 2x2 jacobian matrix. 
    Args:
        jacobian (np.array 2x2): the jacobian matrix at the equilibrium point.
    Return:
        (string) status of equilibrium point 
    """
    determinant = np.linalg.det(jacobian)
    trace = np.matrix.trace(jacobian)
    if np.isclose(trace,0) and np.isclose(determinant,0):
        nature = "Center (Hopf)"
    elif np.isclose(determinant,0):
        nature = "Transcritical (Saddle-Node)"
    elif determinant < 0:
        nature = "Saddle"
    else:
        nature = "Stable" if trace < 0 else "Unstable"
        nature += " focus" if (trace**2 - 4 * determinant) < 0 else " node"
    return nature

EQUILIBRIUM_COLOR = {'Stable node':'C0',
                    'Unstable node':'C1', 
                    'Saddle':'C4',
                    'Stable focus':'C3',
                    'Unstable focus':'C2',
                    'Center (Hopf)':'C5',
                    'Transcritical (Saddle-Node)':'C6'}
def plot_equilibrium(ax, position, nature, legend=True):
    """Draw equilibrium points at position with the color 
       corresponding to their nature"""
    for pos, nat in zip(position,nature):
        ax.scatter(pos[0],pos[1],
                   color= (EQUILIBRIUM_COLOR[nat] 
                           if nat in EQUILIBRIUM_COLOR
                           else 'k'),
                   zorder=100)
        
    if legend:
        # Draw a legend for the equilibrium types that were used.
        labels = list(frozenset(nature))
        ax.legend([mpatches.Patch(color=EQUILIBRIUM_COLOR[n]) for n in labels], labels)

def numerical_continuation(f, initial_u, lbda_values):
    """ Find the roots of the parametrised non linear equation.  
    
    Iteratively find approximate solutions of `F(u, lambda) = 0` 
    for several values of lambda. The solution of the step i is
    used as initial guess for the numerical solver at step i+1. 
    The first inital guess is initial_u (for lbda_values[0]).        
    
    Args:
        f (function): Function of u and lambda.
        initial_u (float): Starting point for the contiunation.
        lbda_values (array): Values of the parameter lambda (in the order of the continuation process).
    
    Return: 
        (numpy.array) output[i] is the solutions of f(u,lbda_values[i]) = 0
         NaN if the algorithm did not converge.
    """
    eq = []
    for lbda in lbda_values:
        eq.append(findroot(lambda x: f(x,lbda),
                           eq[-1] if eq else initial_u))
    return eq

def func(u, lbda):
    return cellular_switch(u, t=0, alpha=1., beta=lbda)

def get_segments(values):
    """Return a dict listing the interval where values is constant.
    Return:
        A dict mapping (start, finish) index to value"""
    start = 0
    segments = {}
    for i,val in enumerate(values[1:],1):
        if val != values[start] or i == len(values)-1:
            segments[(start,i)] = values[start]
            start = i
    return segments

def plot_bifurcation(ax, branches, lbdaspace):
    """Function to draw nice bifurcation graph
    Args:
        ax: object of the plt.subplots
        branches: a list of two lists giving the position and
        the nature of the equilibrium.
        lbda_space: bifurcation parameter space
    """
    labels = frozenset()
    for eq, nature in branches:
        labels = labels.union(frozenset(nature))
        segments = get_segments(nature)
        for idx, n in segments.items():
            ax.plot(lbdaspace[idx[0]:idx[1]],eq[idx[0]:idx[1]],
                     color=EQUILIBRIUM_COLOR[n] if n in EQUILIBRIUM_COLOR else 'k')
    ax.legend([mpatches.Patch(color=EQUILIBRIUM_COLOR[n]) for n in labels],
              labels)

def asymmetrical_cellular_switch(y,t,alpha, beta1, beta2):
    """Flow of the asymmetrical cellular switch model.
    Args: 
        y: (concentration of u, concentration of v)
        t: time (unused, this system is autonomous)
        alpha: maximum production of u or v
        beta1: non-linearity parameter of the effect v->u
        beta2: non-linearity parameter of the effect u->v
    Return: (np.array) [du/dt, dv/dt]
    """
    u, v = y 
    return np.array([(alpha/(1+v**beta1)) - u ,
                     (alpha/(1+u**beta2)) - v])
def jacobian_asymmetrical_cellular_switch(u,v, alpha, beta1, beta2):
    """Jacobian of the assymetrical cellular switch model.
    Args: 
        u: concentration of u
        v: concentration of v
        alpha: maximum production of u or v
        beta1: non-linearity parameter of the effect v->u
        beta2: non-linearity parameter of the effect u->v
    Return: (np.array) 2x2 Jacobian matrix. 
    """
    return - np.array([[1, alpha*beta1*v**(beta1-1) / (1+v**beta1)**2],
                       [alpha*beta2*u**(beta2-1) / (1+u**beta2)**2, 1]])

def plot_isocline(ax, uspace, vspace, alpha, beta, color='k', style='--', opacity=.5):
    """Plot the isoclines of the symmetric cellular switch system"""
    ax.plot(uspace, alpha/(1+uspace**beta), style, color=color, alpha=opacity)
    ax.plot(alpha/(1+vspace**beta),vspace, style, color=color, alpha=opacity)
    ax.set(xlabel='u',ylabel='v')

# Do the simulations.
# Remember that we define f as the partial application of cellular_switch. 
trajectory = {}
for i,param in enumerate(scenarios):
    for j,ic in enumerate(initial_conditions):
        trajectory[i,j] = scipy.integrate.odeint(partial(cellular_switch, **param),
                                                 y0=ic,
                                                 t=time)

# Draw the trajectories. 
fig, ax = plt.subplots(2,2,figsize=(20,10))
for i,param in enumerate(scenarios):
    for j,ic in enumerate(initial_conditions):
        ax[i][0].set(xlabel='Time', ylabel='Concentration of u', title='Trajectory of u, {}'.format(param))
        ax[i][1].set(xlabel='Time', ylabel='Concentration of v', title='Trajectory of v, {}'.format(param))
        l = ax[i][0].plot(time,trajectory[i,j][:,0], label=ic)
        ax[i][1].plot(time,trajectory[i,j][:,1], color=l[0].get_color())
    ax[i][0].legend(title='Initial conditions')

equilibria = {}
for i, param in enumerate(scenarios):
    
    # Find the position of the equilibirum around the endpoint of each trajectory. 
    flow = partial(cellular_switch,t=0, **param)
    starting_points = [trajectory[i,j][-1,:] for j 
                       in range(len(initial_conditions))] 
    equilibria[i] = find_unique_equilibria(flow, starting_points)
    print('{} Equilibrium point(s) for parameters: {}'.format(len(equilibria[i]), param))

# Find the nature of the equilibria
equilibria_nature = {}
for i, param in enumerate(scenarios):
    print('\nParameters: {}'.format(param))
    equilibria_nature[i] = []
    for (u,v) in equilibria[i]:
        equilibria_nature[i].append(stability(jacobian_cellular_switch(u,v, **param)))
        print("{} in ({} {})".format( equilibria_nature[i][-1], u,v,))

plt.show()

uspace = np.linspace(0,2,100)
vspace = np.linspace(0,2,100)

fig, ax = plt.subplots(1,2, figsize=(12,5))
for i, param in enumerate(scenarios):
    ax[i].set(xlabel='u', ylabel='v', title="Phase space, {}".format(param))
    plot_flow(ax[i], param, uspace=uspace, vspace=vspace)
    plot_isocline(ax[i], **param, uspace=uspace, vspace=vspace)
    for j in range(len(initial_conditions)):
        ax[i].plot(trajectory[i,j][:,0],trajectory[i,j][:,1], color='C3')
    plot_equilibrium(ax[i], equilibria[i], equilibria_nature[i])

plt.show()

""" beta_space = np.linspace(10,0.5,1000)
starting_points = [(.5, .99), (0.84, .84), (.99, .5)]

fig, ax = plt.subplots(1,1,figsize=(12,5))
ax.set(xlabel='Beta', ylabel='u')
for init in starting_points:
    
    # Plot the starting points
    dots = plt.scatter(beta_space[0],init[0], color='k')
    
    # Perform numerical continuation. 
    eq = numerical_continuation(func, np.array(init), beta_space)
    plt.plot(beta_space, [x[1] for x in eq], color='k') """

#plt.show()