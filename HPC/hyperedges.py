#!/usr/bin/env python
# Program to generate list of hyperedges for an n-dimensional
#   hypercube that the user provides. Dumps out as a list of
#   edge tuples, assuming uniquely labeled graph nodes. Useful for
#   thinking through hypercube networks.

class TooManyDimensionsError(Exception):
   pass

from os import _exit as exit

while True:
   try:
      dimensions = int(input('For what dimension should I create a list of hypercube edges? '))
      break
   except ValueError:
      print(input + ' is not a valid dimension number.')

try:
   if dimensions > 10:
      raise TooManyDimensionsError({'message':'Really? {:d} dimensions?'.format(dimensions)})
except TooManyDimensionsError as e:
   print(e.args[0]['message'])
   exit(1)

edges = {} # Each key is a layer of edges that are added with each iteration as the hypercube grows
for dim in range(1, dimensions+1):
   if dim == 1:
      edges[1] = [(1,2)]
      continue
   else:
      # Generate edges from existing ones
      for lower_dim in range(1,dim):
         num_edges = len(edges[lower_dim])
         for edge_index in range(0, num_edges):
            increment = 2**(dim-1)
            edge_to_transform = edges[lower_dim][edge_index]
            edges[lower_dim].append( (edge_to_transform[0] + increment, edge_to_transform[1] + increment) )
      # Generate new edges connecting existing hypercube to another -> higher dimension cube
      edges[dim] = [ (i, i+increment) for i in range(1, increment+1) ]

for i in range(1, max(edges.keys())+1):
   print(i, end=': ')
   print(edges[i])
