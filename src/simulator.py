from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.data_store import DataStore


class Simulator(QGraphicsView):
    def __init__(self, parent):
        self.parent = None
        self.data = DataStore()
        self.scn = QGraphicsScene()
        QGraphicsView.__init__(self, self.scn)
        self.setup_station()
        self.show()
        self.fitInView(self.scn.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.door_positions = {}
        self.truck_positions = {}
        self.doors = {}
        self.truck_states = None
        self.pause = None
        self.dialog = []

    def reset(self):
        self.scn.clear()
        self.setup_station()
        self.setup_doors()
        self.setup_trucks()
        self.update()

    def setup_station(self):
        self.scn.addItem(QGraphicsRectItem(-400, -200, 800, 400))
        self.scn.addItem(QGraphicsLineItem(-100, -200, -100,200))
        line =self.scn.addItem(QGraphicsLineItem(100, -200, 100, 200))
        self.a = QGraphicsTextItem('Station')
        self.a.setPos(-20, -180)
        self.scn.addItem(self.a)
        self.fitInView(self.scn.itemsBoundingRect(), Qt.KeepAspectRatio)

    def setup_doors(self):
        try:
            step = 400 / self.data.number_of_receiving_doors
            for i in range(self.data.number_of_receiving_doors):
                name = 'receiving' + str(i)
                self.door_positions[name] = [-250, -200 + step * (i + 1) - step/2]
                door = QGraphicsTextItem(name)
                self.doors[name] = door
                door.setPos(-180, -200 + step * (i + 1) - step/2)
                self.scn.addItem(door)
                self.scn.addItem(QGraphicsLineItem(-100,-200 + step * i , -300, -200 + step * i))

            step = 400 / self.data.number_of_shipping_doors

            for i in range(self.data.number_of_shipping_doors):
                name = 'shipping' + str(i)
                door = QGraphicsTextItem(name)
                self.doors[name] = door
                door.setPos(100, -200 + step * (i + 1) - step/2)
                self.door_positions[name] = [200, -200 + step * (i + 1) - step/2]
                self.scn.addItem(door)
                self.scn.addItem(QGraphicsLineItem(100,-200 + step * i , 300, -200 + step * i))
        except:
            pass

    def setup_trucks(self):
        step = 50
        for i in range(self.data.number_of_inbound_trucks):
            name = 'inbound' + str(i)
            truck = QGraphicsTextItem(name)
            self.truck_positions[name] = truck
            truck.setPos(-480, -180 + i*step)
            self.scn.addItem(truck)

        for i in range(self.data.number_of_compound_trucks):
            name = 'compound' + str(i)
            truck = QGraphicsTextItem(name)
            self.truck_positions[name] = truck
            truck.setPos(-480, -180 + (i + self.data.number_of_inbound_trucks)*step)
            self.scn.addItem(truck)

        for i in range(self.data.number_of_outbound_trucks):
            name = 'outbound' + str(i)
            truck = QGraphicsTextItem(name)
            self.truck_positions[name] = truck
            truck.setPos(430, -180 + i*step)
            self.scn.addItem(truck)

    def update_scene(self):
        step = 50
        for i in range(self.data.number_of_inbound_trucks):
            name = 'inbound' + str(i)
            truck = self.truck_positions[name]
            if self.truck_states[name][0] == 'waiting_to_deploy':
                truck.setPos(-390, -180 + i*step)
            elif self.truck_states[name][0] == 'changeover':
                truck.setDefaultTextColor(Qt.red)
                truck.setPos(*self.door_positions[self.truck_states[name][1]])
            elif self.truck_states[name][0] == 'deploying':
                truck.setDefaultTextColor(Qt.green)
            elif self.truck_states[name][0] == 'changeover2':
                truck.setDefaultTextColor(Qt.red)
            elif self.truck_states[name][0] == 'done':
                truck.setPos(-400 + i*50, 220)

        for i in range(self.data.number_of_compound_trucks):
            name = 'compound' + str(i)
            truck = self.truck_positions[name]
            if self.truck_states[name][0] == 'waiting_to_deploy':
                truck.setPos(-390, -180 + (i + self.data.number_of_inbound_trucks)*step)
            elif self.truck_states[name][0] == 'changeover':
                truck.setPos(*self.door_positions[self.truck_states[name][1]])
            elif self.truck_states[name][0] == 'deploying':
                truck.setDefaultTextColor(Qt.green)
            elif self.truck_states[name][0] == 'changeover2':
                truck.setDefaultTextColor(Qt.red)
            elif self.truck_states[name][0] == 'truck_transfer':
                truck.setPos(-100 + i * 70, -220)
            if self.truck_states[name][0] == 'waiting_to_load':
                truck.setPos(320, -180 + (self.data.number_of_outbound_trucks + i)*step)
            elif self.truck_states[name][0] == 'changeover3':
                truck.setDefaultTextColor(Qt.red)
                truck.setPos(*self.door_positions[self.truck_states[name][1]])
            elif self.truck_states[name][0] == 'not_ready_to_load':
                truck.setDefaultTextColor(Qt.blue)
            elif self.truck_states[name][0] == 'ready_to_load':
                truck.setDefaultTextColor(Qt.yellow)
            elif self.truck_states[name][0] == 'must_load':
                truck.setDefaultTextColor(Qt.gray)
            elif self.truck_states[name][0] == 'loading':
                truck.setDefaultTextColor(Qt.green)
            elif self.truck_states[name][0] == 'changeover4':
                truck.setDefaultTextColor(Qt.red)
            elif self.truck_states[name][0] == 'done':
                truck.setPos(350 - (self.data.number_of_outbound_trucks + i)*80, 220)

        for i in range(self.data.number_of_outbound_trucks):
            name = 'outbound' + str(i)
            truck = self.truck_positions[name]
            if self.truck_states[name][0] == 'waiting_to_load':
                truck.setPos(320, -180 + i*step)
            elif self.truck_states[name][0] == 'changeover':
                truck.setDefaultTextColor(Qt.red)
                truck.setPos(*self.door_positions[self.truck_states[name][1]])
            elif self.truck_states[name][0] == 'not_ready_to_load':
                truck.setDefaultTextColor(Qt.blue)
            elif self.truck_states[name][0] == 'ready_to_load':
                truck.setDefaultTextColor(Qt.yellow)
            elif self.truck_states[name][0] == 'must_load':
                truck.setDefaultTextColor(Qt.gray)
            elif self.truck_states[name][0] == 'loading':
                truck.setDefaultTextColor(Qt.green)
            elif self.truck_states[name][0] == 'changeover2':
                truck.setDefaultTextColor(Qt.red)
            elif self.truck_states[name][0] == 'done':
                truck.setPos(350 - i*80, 220)

    def mouseDoubleClickEvent(self, event):
        self.parent.pause()
        item = self.itemAt(event.pos())
        name = item.toPlainText()
        self.show_dialog(name)

    def show_dialog(self, name):
        dialog = QTextEdit()
        dialog.setWindowTitle(name)
        if name in self.truck_positions.keys():
            dialog.setText(self.parent.solver.truck_list[name].good.goods_in_text())
        elif name in self.doors.keys():
            if name[0] == 'r':
                for good in self.parent.solver.door_list[name].goods_list:
                    dialog.append(good.goods_in_text())
            else:
                dialog.append(self.parent.solver.door_list[name].goods.goods_in_text())
        else:
                dialog.append( self.parent.solver.station.goods_list.goods_in_text())
        self.dialog.append(dialog)
        dialog.show()
