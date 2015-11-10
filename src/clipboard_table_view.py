from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ClipboardTableView(QTableView):
    def __init__(self, parent):
        QTableView.__init__(self, parent)
        self.clip = QApplication.clipboard()

    def keyPressEvent(self, e):
        selected = self.selectedIndexes()
        row_number = 0
        values = [[]]
        if e.matches(QKeySequence.Copy):
            for i in selected:
                if i.row() == row_number:
                    values[row_number].append(str(self.model().data(i, Qt.DisplayRole).value()))
                else:
                    values.append([str(self.model().data(i, Qt.DisplayRole).value())])
                    row_number += 1
            s = ''
            for row in values:
                s += "\t".join(row) + '\n'
            self.clip.setText(s)

        if e.matches(QKeySequence.Paste):
            try:
                selected = self.selectedIndexes()
                row_number = selected[0].row()
                column_number = selected[0].column()
                a = self.clip.text()
                rows = a.split('\n')
                print(rows)
                rows.pop()
                values = []
                for row in rows:
                    values.append(row.split('\t'))
                print(values)
                for row_forward, rows in enumerate(values):
                    for column_forward, value in enumerate(rows):
                        model_index = self.model().createIndex(row_number + row_forward, column_number + column_forward)
                        self.model().setData(model_index, value, Qt.EditRole)
                self.update()

            except:
                pass

