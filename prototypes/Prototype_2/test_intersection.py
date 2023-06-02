# Ce prototype met en oeuvre le calcul d'intersection des rayons vers les objets

from Geometry3D import * 

# fonction qui vérifie l'intersection entre un rayon et un objet.
def printIntersection(ray:Segment,rayName:str, obj: ConvexPolyhedron, objName:str) :
    rencontre = obj.intersection(ray)
    if (isinstance(rencontre,Point)) : 
        print ("{0} intersecte {1} au {2}".format(rayName,objName,rencontre))
    elif (isinstance(rencontre,Segment)) :
        print ("{0} intersecte {1} au {2}".format(rayName,objName,rencontre.start_point))
    else :
        print("{0} n'a pas intersecté {1}".format(rayName, objName))

# Objets géométriques
sphere_1 = Sphere(Point(2,15,5),radius=6,n1=10,n2=5)
cube_1  = Parallelepiped(Point(-10,10,5), Vector(5,0,0),Vector(0,5,0), Vector(0,0,5))
cube_2 = Parallelepiped(Point(10,10,5), Vector(5,0,0),Vector(0,5,0), Vector(0,0,5))

# Rayons
departure = Point(0,-5,5)
ray_1 = Segment(departure, Vector(-8,25,3))
ray_2 = Segment(departure, Vector(0,25,0))
ray_3 = Segment(departure,Vector(0,25,-3))
ray_4 = Segment(departure,Vector(18,25,5))

# Test : mesure des intersections entre un rayon donné et un objet
printIntersection(ray_1,'ray_1', cube_1,'cube_bleu')
printIntersection(ray_2,'ray_2', sphere_1, 'sphere_rouge')
printIntersection(ray_3,'ray_3', cube_1,'cube_bleu')
printIntersection(ray_4,'ray_4', cube_2, 'cube_jaune')

# aperçu de la scène 3D
r = Renderer()
r.add((sphere_1,'r',1),normal_length=0)
r.add((cube_1, 'b',1),normal_length=0)
r.add((cube_2, 'y',1), normal_length=0)
r.add((departure,'g',1), normal_length=0)
r.add((ray_1,'g', 1), normal_length=0)
r.add((ray_2,'g', 1), normal_length=0)
r.add((ray_3,'purple', 1), normal_length=0)
r.add((ray_4,'purple', 1), normal_length=0)
r.show()
