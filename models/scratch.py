import numpy as np



# construct couch index map
c0 = np.arange(270,360,1)
# print(c0)
i0 = np.arange(len(c0))
# print(i0)

c1 = np.arange(0,91,1)
COUCH = np.hstack((c0, c1))
# print(couch)
i1 = np.arange(len(c1)) + len(c0)
I = np.hstack((i0, i1))
# print(i)

g0 = np.arange(181,360,1)
# print(g0)
j0 = np.arange(len(g0))
# print(j0)

g1 = np.arange(0,181,1)
GANTRY = np.hstack((g0, g1))
# print(gantry)
j1 = np.arange(len(g1)) + len(g0)
J = np.hstack((j0, j1))
# print(j)

x_map = dict([(str(COUCH[i]), int(I[i])) for i in range(len(I))])
y_map = dict([(str(GANTRY[j]), int(J[j])) for j in range(len(J))])


export_image = np.zeros((len(GANTRY), len(COUCH)))

export_path = r"C:\__python__\Projects\MapApp\data\MapRT_Exports\507261791 For MapRT 20250404134828.csv"
with open(export_path, 'r') as f:
    for line in f:
        if not line.startswith('Gantry'):
            if len(line.split(';')) == 3:
                gantry, couch, collision = line.split(';')
                c = 1 if collision.strip() == 'false' else 0

                export_image[y_map[gantry], x_map[couch]] = c

            else:
                print(line)