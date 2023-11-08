import sys
import matplotlib
matplotlib.use('Qt5Agg')
from sympy import *
from time import perf_counter
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavToolbar
from matplotlib.figure import Figure
from sympy.parsing.sympy_parser import parse_expr
from sympy import Symbol
import sympy
from scipy.optimize import fsolve

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(1,1,1)
        self.axes.spines['bottom'].set_position('zero')
        super(MplCanvas, self).__init__(fig)
        
class _interfata():
    
    def __init__(self):
        pass
    
    def valoriF(self):
        a_label=QLabel('a = ')
        b_label=QLabel('b = ')
        f_label=QLabel('f = ')
        a_line=QLineEdit()
        b_line=QLineEdit()
        f_line=QLineEdit()
        a_line.setFixedWidth(150)
        b_line.setFixedWidth(150)
        f_line.setFixedWidth(150)
        
        
        layout=QGridLayout()
        layout.addWidget(a_label, 0, 0)
        layout.addWidget(a_line,0,1)
        layout.addWidget(b_label,1,0)
        layout.addWidget(b_line,1,1)
        layout.addWidget(f_label,2,0)
        layout.addWidget(f_line,2,1)
        layout.setColumnStretch(5, 1)
        return layout,a_line,b_line,f_line
    
    def valoriStop(self):
        groupboxStop=QGroupBox("Criterii de oprire")
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        hbox=QHBoxLayout()
        
        n_label=QLabel("n = ")
        n_line=QLineEdit()
        hbox.addWidget(n_label)
        hbox.addWidget(n_line)
        hbox.addStretch()
        layout.addLayout(hbox)
        

        e_label=QLabel("E(n) = ")
        e_line = QLineEdit()
        hbox=QHBoxLayout()
        hbox.addWidget(e_label)
        hbox.addWidget(e_line)
        hbox.addStretch()
        layout.addLayout(hbox)
        
        tol_label=QLabel("abs(x[n+1]-x[n])<=tol = ")
        tol_line=QLineEdit()
        hbox=QHBoxLayout()
        hbox.addWidget(tol_label)
        hbox.addWidget(tol_line)
        hbox.addStretch()
        layout.addLayout(hbox)
        
        groupboxStop.setLayout(layout)
        return e_line,tol_line,n_line,groupboxStop
    
    def metode(self):
        groupboxMetoda=QGroupBox("Metode")
        bisectie=QRadioButton("Metoda bisectiei")
        coarda=QRadioButton("Metoda coardei")
        hbox=QHBoxLayout()
        hbox.addWidget(bisectie)
        hbox.addWidget(coarda)
        groupboxMetoda.setLayout(hbox)
        return bisectie,coarda,groupboxMetoda
    
    def rezultate(self):
        Vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        xn_label=QLabel("Approx val xn = ")
        xn_line = QTextEdit()
        xn_line.setReadOnly(True)
        xn_line.setFixedSize(80, 26)
        hbox.addWidget(xn_label)
        hbox.addWidget(xn_line)
        hbox.addStretch()
        
        layoutEroare=QHBoxLayout()
        eroare_label=QLabel("Eroare: abs(xn-fzero) = ")
        eroare_line = QTextEdit()
        eroare_line.setFixedSize(80, 26)
        eroare_line.setReadOnly(True)
        layoutEroare.addWidget(eroare_label)
        layoutEroare.addWidget(eroare_line)
        layoutEroare.addStretch()
        
        layoutExecutie = QHBoxLayout()
        metoda_label = QLabel("Timp executie metoda = ")
        metoda_line = QTextEdit()
        metoda_line.setFixedSize(80, 26)
        metoda_line.setReadOnly(True)
        
        executie_label=QLabel("Timp executie plotare = ")
        executie_line = QTextEdit()
        executie_line.setFixedSize(80, 26)
        executie_line.setReadOnly(True)
        
        exec_eroare_line = QLineEdit()
        exec_eroare_label = QLabel("Timp executie eroare = ")
        exec_eroare_line.setReadOnly(True)
        exec_eroare_line.setFixedSize(80,26)
        
        l = QHBoxLayout()
        l.addWidget(exec_eroare_label)
        l.addWidget(exec_eroare_line)
        l.addStretch()
        
        layoutExecutie.addWidget(metoda_label)
        layoutExecutie.addWidget(metoda_line)
        layoutExecutie.addWidget(executie_label)
        layoutExecutie.addWidget(executie_line)
        layoutExecutie.addStretch()
        
        Vbox.addLayout(hbox)
        Vbox.addLayout(layoutEroare)
        Vbox.addLayout(layoutExecutie)
        Vbox.addLayout(l)
        Vbox.addStretch()
        
        return exec_eroare_line,xn_line,eroare_line,metoda_line,executie_line,Vbox

class metode():
        def __init__(self):
            pass
        
        #---------METODA BISECTIEI----------------
        def bisectie(self,f,a,b,n,tol,tol2):
            x = Symbol('x')
            f = lambdify(x,f)
            t1 = perf_counter()
            x_val=[]
            x_val.append(b)
            count = 0
            while count < n:
                x = (a+b)/2
                x_val.append(x)
                if f(x)==0 or np.abs(b-a)/2<tol or np.abs(x-x_val[-2])<tol2:
                    break
                elif f(a)*f(x)<0:
                    b = x
                elif f(x)*f(b)<0:
                    a = x
                else: QMessageBox.critical(None, "Eroare", "Metoda bisectiei nu se poate aplica pe functia introdusa!")
                count += 1
            t2 = perf_counter()
            t_executie = str(round(t2-t1,4))
            
            
            t1 = perf_counter()
            er = fsolve(f,(a+b)/2)
            t2 = perf_counter()
            t_eroare = str(round(t2-t1,4))
            er = round(er[0],4)
            return t_executie,t_eroare,x,x_val,count,er
        
        #---------METODA COARDEI----------------
        def coarda(self, f, a, b, n, tol, tol2):
            t1 = perf_counter()
            x = Symbol('x')
            f2 = diff(f, x, 2)
            f = lambdify(x, f)
            f2 = lambdify(x, f2)
            r_ex = fsolve(f, (a + b) / 2)
            x_values = []
            y_values = []
            contor = 1
            try:
                if f(a) * f2(a) < 0:
                    x = a
                    punct_initial = a
                    while True:
                        x_prev = x
                        x = x - f(x) / (f(x) - f(b)) * (x - b)
                        x_values.append(x)
                        y_values.append(f(x))
                        contor += 1
                        if abs(r_ex - x) <= tol or contor > n or abs(x - x_prev) < tol2:
                            break
                else:
                    x = b
                    punct_initial = b
                    while True:
                        x_prev = x
                        x = x - f(x) / (f(x) - f(a)) * (x - a)
                        x_values.append(x)
                        y_values.append(f(x))
                        contor += 1
                        if abs(r_ex - x) <= tol or contor > n or abs(x - x_prev) < tol2:
                            break
            except Exception as e:
                    QMessageBox.critical(None, "Eroare", "Metoda coardei nu se poate aplica pe functia introdusa!")
            t2 = perf_counter()
            t_executie = str(round(t2-t1,4))
            t1 = perf_counter()
            fzero = fsolve(f,(a+b)/2)
            t2 = perf_counter()
            fzero = round(fzero[0],4)
            t_eroare = str(round(t2-t1,4))
            return t_executie,t_eroare,contor, x,fzero, x_values, y_values, punct_initial
            
        


class MainWindow(QMainWindow):
    
        
        
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.setWindowTitle('Proiect Calcul Numeric')     
        m = metode()
        #---------PLOTARE BISECTIE----------------
        def plotare_bisectie(f,a,b,radacina,x_val):
            x = Symbol('x')
            f = lambdify(x,f)
            t1=perf_counter()
            sc.axes.cla()
            x=np.linspace(a,b,100)
            sc.axes.plot(x,f(x),label=r"Function")
            sc.axes.axhline(y=0,color='black',linestyle='--')
            text=""
            n=len(x_val)
            for i in range(0,n):
                x_val[i] = round(x_val[i],6)
                if x_val[i]>radacina:
                    text+=str(x_val[i])
                    text+="\n"
            
            radacina=round(radacina,6)
            for x in x_val:
                if x > radacina:
                    sc.axes.plot([x],[0],marker='o',markersize=5,color='red')
            sc.axes.plot([radacina],[0],marker='o',markersize=10,color='blue',label=r'Radacina')
            sc.axes.legend()
            text_radacini.setText(text)
            sc.draw_idle()
            t2=perf_counter()
            executie_line.setText(str(round(t2-t1,5)))
            xn_line.setText(str(round(radacina,4)))
        
        #---------PLOTARE COARDA----------------
        def plotare_coarda(f,a,b,radacina,x_values, y_values, punct_initial):
            t1 = perf_counter()
            x = Symbol('x')
            f = lambdify(x,f)
            sc.axes.cla()
            x_plot = np.linspace(a, b, 1000)
            sc.axes.plot(x_plot,f(x_plot),'b-', label='Function')
            sc.axes.axhline(y=0,color='black',linestyle='--')
            for i in range(len(x_values)):
                sc.axes.plot([punct_initial, x_values[i]], [f(punct_initial), y_values[i]], 'r-', linewidth=0.5)
            text=""
            for i in x_values:
                text+=str(round(i,6))
                text+="\n"
            text_radacini.setText(text)
            sc.axes.scatter(x_values[-1], y_values[-1], color='r')
            sc.axes.scatter(x_values[0], y_values[0], color='g')
            sc.axes.set_title("Metoda coardei")
            sc.axes.set_xlabel("x")
            sc.axes.set_ylabel("y")
            sc.axes.legend()
            sc.draw_idle()
            t2 = perf_counter()
            executie_line.setText(str(round(t2-t1,5)))
            xn_line.setText(str(round(radacina,4)))
                 
        #---------BUTON PLOTARE----------------
        def but_plotare():
            
            plotare.setEnabled(False)
            f = f_line.text()
            a = int(a_line.text())
            b = int(b_line.text())
            n = int(n_line.text())
            tol = eval(e_line.text())
            tol2 = eval(tol_line.text())
            if bisectie.isChecked():
                t_executie,t_eroare,radacina,x_val,count,fzero = m.bisectie(f,a,b,n,tol,tol2)
                metoda_line.setText(t_executie)
                exec_eroare_line.setText(t_eroare)
                er = abs(round(radacina-fzero,8))
                eroare_line.setText(str(er))
                plotare_bisectie(f, a, b, radacina, x_val)
            
            if coarda.isChecked():
                t_executie,t_eroare,contor,fzero,radacina,x_values,y_values,punct_initial = m.coarda(f, a, b, n, tol, tol2)
                metoda_line.setText(t_executie)
                exec_eroare_line.setText(t_eroare)
                er = abs(round(radacina-fzero,8))
                eroare_line.setText(str(er))
                plotare_coarda(f, a, b, radacina, x_values, y_values, punct_initial)
        
        #---------VALIDARE FUNCTIE----------------
        def valid_func(f):
            try:
                expression = f
                x = Symbol('x')
                expr = parse_expr(expression)
                # if x in expr.free_symbols: AICI AM MODIFICAT DUPA INCARCARE
                if expr.free_symbols == {x}:
                    return True
                else:
                    raise ValueError
                    
            except Exception as e:
                return False
            
        #---------VALIDARE CRITERII STOP----------------
        def valid_crit_stop(expr):
            try:
                eval(expr)
                return True
            except Exception as e:
                return False
        
        def is_integer(n):
            if n.isdigit():
                return True
            elif n[0]=='-' and n[1:].isdigit():
                return True
            else:
                return False
            
        #---------BUTON VALIDARE----------------
        def but_validare():
            bool_list = []
            a = a_line.text()
            bool_a=is_integer(a)
            bool_list.append(bool_a)

            b = b_line.text()
            bool_b =is_integer(b)
            bool_list.append(bool_b)

            f = f_line.text()
            bool_f=valid_func(f)
            bool_list.append(bool_f)

            n = n_line.text()
            bool_n = is_integer(n)
            bool_list.append(bool_n)

            en = e_line.text()
            bool_en = valid_crit_stop(en)
            bool_list.append(bool_en)

            tol = tol_line.text()
            bool_tol = valid_crit_stop(tol)
            bool_list.append(bool_tol)
            
            bool_list.append(coarda.isChecked() or bisectie.isChecked())
            
            if not bool_a:
                QMessageBox.critical(None, "Eroare", "Valorile din campul a sunt invalide!")
            if not bool_b:
                QMessageBox.critical(None, "Eroare", "Valorile din campul b sunt invalide!")
            if not bool_f:
                QMessageBox.critical(None, "Eroare", "Functia f introdusa este invalida!")
            if not bool_n:
                QMessageBox.critical(None, "Eroare", "Valoarea introdusa pentru n este invalida!")
            if not bool_en:
                QMessageBox.critical(None, "Eroare", "Valoarea introdusa pentru E(n) este invalida!")
            if not bool_tol:
                QMessageBox.critical(None, "Eroare", "Valoarea introdusa pentru tol este invalida!")
            if not coarda.isChecked() and not bisectie.isChecked():
                QMessageBox.critical(None, "Eroare", "Selectati tipul de metoda de calcul!")
                
            if bool_list == ([True]*len(bool_list)):
                plotare.setEnabled(True)
                m = QMessageBox()
                m.setText("Datele introduse sunt valide")
                m.setWindowTitle("Valid!")
                m.exec()
            
        
        #---------ELEMENTE INTERFATA----------------
        toolbar=NavToolbar(sc, self)
        interfata=_interfata()
        e_line,tol_line,n_line,stop=interfata.valoriStop()
        
        
        layout=QGridLayout()
        layout_valori,a_line,b_line,f_line=interfata.valoriF()
        bisectie,coarda,layout_metode=interfata.metode()
        exec_eroare_line, xn_line,eroare_line,metoda_line,executie_line,layoutExecutie=interfata.rezultate()
        
        
        plotare=QPushButton("Plotare")
        plotare.setEnabled(False)
        validare=QPushButton("Validare")
        box=QHBoxLayout()
        box.addWidget(validare)
        box.addWidget(plotare)
        plotare.clicked.connect(but_plotare)
        validare.clicked.connect(but_validare)
        
        
        
        
        text_radacini = QTextEdit()
        text_radacini.setReadOnly(True)
        text_radacini.setFixedSize(200,200)
        
        layout.addWidget(text_radacini,1,1)
        layout.addWidget(toolbar, 0, 0)
        layout.addLayout(layout_valori, 1, 0)
        layout.addWidget(layout_metode, 0, 1)
        layout.addLayout(box, 3, 0)
        layout.addWidget(stop, 2, 0)    
        layout.addWidget(sc,2,2)
        layout.addLayout(layoutExecutie, 1, 2)


        
        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
        
        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()

