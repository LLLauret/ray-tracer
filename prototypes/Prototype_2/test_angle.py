# Ce prototype permet de tester le calcul d'angle

# Le calcul de l'angle entre un segment (rayon) et une Géométrie n'est pas implémentée (raise NotImplementedException)
# Il faut passer par des étapes intermédiaires pour obtenir l'angle entre une ligne et un plan
# le plan se crée à partir d'une face de la Géométrie et la ligne se base sur la direction du segment

from Geometry3D import *

def creerPlanIntersection(obj : ConvexPolyhedron, rencontre : Point) -> Plane :
    if rencontre == None :
        return None
    polygon = None
    for cpg in obj.convex_polygons :
        if rencontre in cpg :
            polygon = cpg
            break
    return (cpg.plane)

#creer une ligne collinéaire à un segment
def SegmentToLine (seg : Segment) -> Line :
    ligne = Line(seg.start_point, seg.end_point)
    return ligne

# trouve le point d'intersection le plus proche
def trouverPointIntersection(obj : ConvexPolyhedron, ray: Segment) :
    # l'intersection peut retourner un Point(), ou un Segement(), ou None
    points = ray.intersection(obj)
    if isinstance(points, Point) :
        return points
    elif isinstance(points, Segment) :
        return points.start_point if distance(points.start_point,ray.start_point) < distance(points.end_point, ray.start_point) else points.end_point
    return None

r = Renderer()
# rayon
departure = Point(5,-10,5)
ray = Segment(departure, Vector(0,25,-7))

# Objet géométrique
cube_1 = Parallelepiped(base_point=Point(0,0,0), v1=Vector(10,0,0), v2=Vector(0,10,0), v3=Vector(0,0,10))

# rencontre = cube_1.intersection(ray)
pointRencontre = trouverPointIntersection(cube_1, ray)
print(pointRencontre)
if (pointRencontre != None) :
    r.add((pointRencontre, 'red', 10), normal_length=0)
    plan_rencontre = creerPlanIntersection(cube_1,pointRencontre)
    print (SegmentToLine(ray).angle(plan_rencontre))


r.add((departure, 'green', 10), normal_length=0)
r.add((ray,'green', 1), normal_length=0)
r.add((cube_1,'red', 1), normal_length=0)

r.show()