from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Currency converter")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        # creation de layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")

        # Ajout des widgets sur le layout
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)


    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        # range of values
        self.spn_montant.setRange(1, 100000000)
        self.spn_montantConverti.setRange(1, 100000000)

        # default values
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)


    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)


    def setup_css(self):
        self.setStyleSheet("""
        background-color : rgb(44, 54, 57);
        color: white;
        border: none;
        """)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try:
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("Erreur de conversion")
        else:
            self.spn_montantConverti.setValue(resultat)


    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()



app = QtWidgets.QApplication([]) # debut app

win = App() # creation de la fênetre
win.show()

app.exec_() # fin app