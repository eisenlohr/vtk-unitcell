#!/usr/bin/env python3

import numpy as np
import argparse
import damask                                                                   # see https://damask.mpie.de for installation instructions

hexagon = np.linspace(0,2*np.pi,6,endpoint=False)
square  = np.linspace(0,2*np.pi,4,endpoint=False)+np.pi/4

def VTK_CELLTYPE(count):
    try:
        type = [1,3,5][count-1]
    except IndexError:
        type = 7
    return type

def points(family,a,b,c,alpha,beta,gamma):
    return {
    'cubic' : np.sqrt(2.)*np.hstack((
                np.array([
                          np.cos(-square),
                          np.sin(-square),
                          np.zeros(len(square)),
                        ]),
                np.array([
                          np.cos(square),
                          np.sin(square),
                          np.ones(len(square))*np.sqrt(2.),
                        ])
                        )).T,
    'tetragonal' : np.sqrt(2.)*np.hstack((
                np.array([
                          np.cos(-square),
                          np.sin(-square),
                          np.zeros(len(square)),
                        ]),
                np.array([
                          np.cos(square),
                          np.sin(square),
                          np.ones(len(square))*np.sqrt(2.)*c/a,
                        ])
                        )).T,
    'hexagonal' : np.hstack((
                np.array([[0,0,0]]).T,
                np.array([
                          np.cos(-hexagon),
                          np.sin(-hexagon),
                          np.zeros(len(hexagon)),
                        ]),
                np.array([
                          np.cos(hexagon),
                          np.sin(hexagon),
                          np.ones(len(hexagon))*c/a,
                        ]),
                np.array([[0,0,1]]).T*c/a,
                        )).T,
    }[family]

unitcell = {
  'cubic' : [
             [0,1,2,3],
             [0,3,4,7],
             [3,2,5,4],
             [2,1,6,5],
             [1,0,7,6],
             [4,5,6,7],
            ],
  'tetragonal' : [
             [0,1,2,3],
             [0,3,4,7],
             [3,2,5,4],
             [2,1,6,5],
             [1,0,7,6],
             [4,5,6,7],
            ],
  'hexagonal' : [
             [ 1, 2, 3, 4, 5, 6],
             [ 1, 6, 8, 7],
             [ 6, 5, 9, 8],
             [ 5, 4,10, 9],
             [ 4, 3,11,10],
             [ 3, 2,12,11],
             [ 2, 1, 7,12],
             [ 7, 8, 9,10,11,12],
            ],
}

slipgeometry = {
 'cubic:f' : {
           'direction' : [
                           [7,3],
                           [3,5],
                           [5,7],
#
                           [5,1],
                           [1,7],
                           [7,5],
#
                           [3,7],
                           [7,1],
                           [1,3],
#
                           [1,5],
                           [5,3],
                           [3,1],
                         ],
           'plane' : [
                           [7,3,5],
                           [5,1,7],
                           [3,7,1],
                           [1,5,3],
                     ],
            },

 'hexagonal:hcp' : {
           'direction' : [
                           # <a>
                           [0,1],           # 0  a1
                           [0,6],           # 1 -a3
                           [0,5],           # 2  a2
                           [0,4],           # 3 -a1
                           [0,3],           # 4  a3
                           [0,2],           # 5 -a2
                           # <aa>
                           [1,5],           # 6 a2-a1
                           [5,3],           # 7 a3-a2
                           [3,1],           # 8 a1-a3
                           # <c+a>
                           [0, 7],          #  9  a1 + c
                           [0, 8],          # 10 -a3 + c
                           [0, 9],          # 11  a2 + c
                           [0,10],          # 12 -a1 + c
                           [0,11],          # 13  a3 + c
                           [0,12],          # 14 -a2 + c
                         ],
           'plane' : [
                           # basal
                           [ 1, 2, 3, 4, 5, 6],
                           # prism
                           [ 6, 5, 9, 8],
                           [ 4, 3,11,10],
                           [ 2, 1, 7,12],
                           # second order prism
                           [ 1, 5, 9, 7],
                           [ 5, 3,11, 9],
                           [ 3, 1, 7,11],
                           # first order pyramidal
                           [ 1, 6, 9,12],
                           [ 6, 5,10, 7],
                           [ 5, 4,11, 8],
                           [ 4, 3,12, 9],
                           [ 3, 2, 7,10],
                           [ 2, 1, 8,11],
                           # second order pyramidal
                           [ 1, 5,10,12],
                           [ 6, 4,11, 7],
                           [ 5, 3,12, 8],
                           [ 4, 2, 7, 9],
                           [ 3, 1, 8,10],
                           [ 2, 6, 9,11],
                     ],

         }
}

slipsystems = {
 'cubic:f' : [
          [0,0],
          [1,0],
          [2,0],
#
          [3,1],
          [4,1],
          [5,1],
#
          [6,2],
          [7,2],
          [8,2],
#
          [9,3],
          [10,3],
          [11,3],
        ],

 'hexagonal:hcp' : [
          # basal <a>
          [0,0],
          [2,0],
          [4,0],
          # prism <a>
          [0,1],
          [2,2],
          [4,3],
          # 2nd prism <aa>
          [6,4],
          [7,5],
          [8,6],
          # 1st pyramidal <a>
          [2, 7],
          [3, 8],
          [4, 9],
          [5,10],
          [0,11],
          [1,12],
          # 1st pyramidal <c+a>
          [12, 7],
          [13, 7],
          [13, 8],
          [14, 8],
          [14, 9],
          [ 9, 9],
          [ 9,10],
          [10,10],
          [10,11],
          [11,11],
          [11,12],
          [12,12],
          # 2nd pyramidal <c+a>
          [13,13],
          [14,14],
          [ 9,15],
          [10,16],
          [11,17],
          [12,18],
        ],
}


parser = argparse.ArgumentParser(description='VTK model of oriented unitcell',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('--quaternion',dest='quaternion',
                    nargs=4, type=float, metavar=('q','p1','p2','p3'),
                    help='orientation as unit quaternion')
group.add_argument('--axisangle',dest='axisangle',
                    nargs=4, type=float, metavar=('a1','a2','a3','angle'),
                    help='orientation as axis and angle')
group.add_argument('--euler',dest='euler',
                    nargs=3, type=float, metavar=('phi1','Phi','phi2'),
                    help='orientation as z-x-z Euler angles')

parser.add_argument('--family', dest='family',
                    default='cubic',choices=['cubic','tetragonal','hexagonal'],
                    help='crystal symmetry')
parser.add_argument('--lattice', dest='lattice',
                    default='p',choices=['p','i','f','hcp'],
                    help='lattice type')

parser.add_argument('--slipsystems', dest='slipsystems',
                    help='list of slip systems to include')
parser.add_argument('--plane', dest='plane', action='store_true',
                    help='plot slip planes')
parser.add_argument('--direction', dest='direction', action='store_true',
                    help='plot slip directions')
parser.add_argument('--no-unitcell', dest='unitcell',action='store_false',
                    help='omit unitcell')

parser.add_argument('--position',dest='position',
                    nargs=3, type=float, metavar=('x','y','z'), default=[0.0,0.0,0.0],
                    help='coordinates of unitcell center')
parser.add_argument('--scaling',dest='scaling',
                    type=float, default=1.,
                    help='scale factor for unitcell coordinates')

parser.add_argument('-a', dest='a',
                    type=float, default=1.,
                    help='unit cell a')
parser.add_argument('-b', dest='b',
                    type=float,
                    help='unit cell b')
parser.add_argument('-c', dest='c',
                    type=float,
                    help='unit cell c')
parser.add_argument('--alpha', dest='alpha',
                    type=float,
                    help='unit cell alpha')
parser.add_argument('--beta', dest='beta',
                    type=float,
                    help='unit cell beta')
parser.add_argument('--gamma', dest='gamma',
                    type=float,
                    help='unit cell gamma')
parser.add_argument('--degrees', dest='degrees', action='store_true',
                    help='angles are given in degrees')

args = parser.parse_args()

family  = args.family.lower()
lattice = args.family.lower()+':'+args.lattice.lower()
position = np.array(args.position)
systems = [] if args.slipsystems is None else list(map(lambda x: int(x)-1,args.slipsystems.split(',')))

if   args.quaternion is not None:
    rotation = damask.Rotation.from_quaternion(args.quaternion)
elif args.axisangle is not None:
    rotation = damask.Rotation.from_axis_angle(args.axisangle,degrees=args.degrees,normalize=True)
elif args.euler is not None:
    rotation = damask.Rotation.from_Euler_angles(args.euler,degrees=args.degrees)
else:
    rotation = damask.Rotation()

thePoints = points(family,*(damask.Crystal(lattice=family[0]+'P',
                                           a=args.a,b=args.b,c=args.c,
                                           alpha=args.alpha,beta=args.beta,gamma=args.gamma,
                                           degrees=args.degrees).parameters))
centerOfGravity = np.mean(thePoints,axis=0)

print('\n'.join([
  '# vtk DataFile Version 2.0 Cube example',
  'example',
  'ASCII',
  'DATASET UNSTRUCTURED_GRID',
  'POINTS {} float'.format(len(thePoints)),
  ]+
  list(map(lambda x: '{} {} {}'.format(*(position+args.scaling*(~rotation@x))),thePoints-centerOfGravity))  # orientation is a passive rotation; here an active rotation is needed
  ))

datacount = 0
polys = []
types = []
planes = []

if args.unitcell:
  for poly in unitcell[family]:
    l = len(poly)
    datacount += 1+l
    polys.append(' '.join(map(str,[l]+poly)))
    types.append(VTK_CELLTYPE(l))

for system in systems:
  dirID,planeID = slipsystems[lattice][system]
  if args.plane and planeID not in planes:
    planes.append(planeID)
    poly = slipgeometry[lattice]['plane'][planeID]
    l = len(poly)
    datacount += 1+l
    polys.append(' '.join(map(str,[l]+poly)))
    types.append(VTK_CELLTYPE(l))
  if args.direction:
    poly = slipgeometry[lattice]['direction'][dirID]
    l = len(poly)
    datacount += 1+l
    polys.append(' '.join(map(str,[l]+poly)))
    types.append(VTK_CELLTYPE(l))
    datacount += 1+1
    polys.append(f'1 {poly[-1]}')
    types.append(VTK_CELLTYPE(1))

print('\n'.join([
  f'CELLS {len(polys)} {datacount}',
  ]+
  polys
  ))

print('\n'.join([
  f'CELL_TYPES {len(polys)}',
  ]+
  list(map(str,types))
  ))
