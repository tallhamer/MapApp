
https://stackoverflow.com/questions/38021869/getting-imageitem-values-from-pyqtgraph
def mouseMoved(self, viewPos):

    data = self.image.image  # or use a self.data member
    nRows, nCols = data.shape

    scenePos = self.image.getImageItem().mapFromScene(viewPos)
    row, col = int(scenePos.y()), int(scenePos.x())

    if (0 <= row < nRows) and (0 <= col < nCols):
        value = data[row, col]
        print("pos = ({:d}, {:d}), value = {!r}".format(row, col, value))
    else:
        print("no data at cursor")