from compas.datastructures import Mesh

from compas_fofin.datastructures import Cablenet

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import normalize_vector

from compas.utilities import pairwise
from compas.utilities import geometric_key


class Membrane(Cablenet):

	def __init__(self, *args, **kwargs):
		super(Membrane, self).__init__(*args, **kwargs)
		self.name = 'Membrane'

		self.origin = [0.0, 0.0, 0.0]

		self.length = 10.0

		self.width_base = 1.0
		self.width_top = 6.0

		self.height_base = 0.0
		self.height_top = -3.0

		self.inset_top = 4.0

	def build(self):
		"""
		"""
		def add_vertex_xyz(xyz, key=None):
			x, y, z = xyz
			return self.add_vertex(key=key, x=x, y=y, z=z)

		# build top triplet
		top_pt = add_vectors(self.origin, [0.0, self.length, 0.0])
		trt = self._points_triplet(top_pt, self.width_top, self.height_top, -self.inset_top)
		
		# build bottom triplet
		trb = self._points_triplet(self.origin, self.width_base, self.height_base)

		# weave faces
		for line_a, line_b in zip(pairwise(trt), pairwise(trb)):
			a, b = [add_vertex_xyz(xyz) for xyz in line_a]
			c, d = [add_vertex_xyz(xyz) for xyz in line_b]
			face = [c, d, b, a]
			self.add_face(face)

		# set anchors
		gkey_key = self.gkey_key()
		anchors = []

		trt.pop(2)
		for pt in trt:
			anchors.append(gkey_key[geometric_key(pt)])

		for pt in trb[:1] + trb[-1:]:
			anchors.append(gkey_key[geometric_key(pt)])
		
		for anchor in anchors:
			self.vertex_attribute(anchor, 'is_anchor', True)

	def _points_triplet(self, base_pt, width, height, inset=None):
		"""
		"""
		a, e = [add_vectors(base_pt, [width * s, height, 0.0]) for s in [-1, 1]] 

		pts = []
		for pt in [a, e]:
			vec = subtract_vectors(pt, base_pt)
			pts.append(add_vectors(base_pt, scale_vector(vec, 0.5)))

		if inset is not None:
			base_pt = add_vectors(base_pt, [0.0, inset, 0.0])

		b, d = pts
		return [a, b, base_pt, d, e]


	def subdivide(self, u, v):
		"""
		"""
		return

	@property
	def anchors(self):
		return self.vertices_where({'is_anchor': True})

	@anchors.setter
	def anchors(self, anchors):
		self.vertices_attributes('is_anchor', True, anchors)


if __name__ == '__main__':
	import compas

	from compas.datastructures import mesh_subdivide_quad
	from compas.datastructures import mesh_delete_duplicate_vertices
	from compas.utilities import geometric_key

	from compas_fofin.datastructures import Cablenet
	from compas_fofin.fofin import update_xyz_numpy

	from compas_viewers.meshviewer import MeshViewer
	

	membrane = Membrane()
	membrane.build()
	subd = mesh_subdivide_quad(membrane, k=3)
	mesh_delete_duplicate_vertices(subd)

	cablenet = Cablenet()

	for vkey, attr in subd.vertices(True):
		cablenet.add_vertex(vkey, attr_dict=attr)

	for fkey, attr in subd.faces(True):
		face = subd.face_vertices(fkey)
		cablenet.add_face(face, fkey=fkey, attr_dict=attr)

	# self weight
	cablenet.attributes['density'] = 0.

	# anchors
	gkey_key = cablenet.gkey_key()

	for anchor in membrane.anchors:
		gkey = geometric_key(membrane.vertex_coordinates(anchor))
		vkey = gkey_key[gkey]
		cablenet.vertex_attribute(vkey, 'is_anchor', True)

	for edge in cablenet.edges_on_boundary():
		cablenet.edge_attributes(edge, ['q'], [1])
	
	# fd
	# update_xyz_numpy(cablenet)

	# visualize
	viewer = MeshViewer()
	viewer.mesh = cablenet
	viewer.show()

	
