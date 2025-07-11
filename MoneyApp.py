import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget
)
from PyQt5.QtGui import QFont

class SangtongWallet(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.setWindowTitle("WalletBySangtong")
        self.setGeometry(500, 500, 557, 500)

        self.setStyleSheet("background-color: #121916; color: #DCDCDC")

        label_font = QFont("Segoe UI", 10, QFont.Bold)
        button_font = QFont("Segoe UI", 10)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(2)

        label_income = QLabel("Income : ")
        label_income.setFont(label_font)

        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("เขียนยอดเงิน")
        self.income_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        income_layout = QHBoxLayout()
        income_layout.addWidget(label_income)
        income_layout.addWidget(self.income_input)
        
        main_layout.addLayout(income_layout)

        label_outcome = QLabel("Outcome :")
        label_outcome.setFont(label_font)
        self.outcome_input = QLineEdit()
        self.outcome_input.setPlaceholderText("เขียนยอดเงิน")
        self.outcome_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        outcome_layout = QHBoxLayout()
        outcome_layout.addWidget(label_outcome)
        outcome_layout.addWidget(self.outcome_input)
        
        main_layout.addLayout(outcome_layout)

        label_percentage = QLabel("Passive Income Percent :")
        label_percentage.setFont(label_font)
        self.percentage_input = QLineEdit()
        self.percentage_input.setPlaceholderText("อัตรากำไร")
        self.percentage_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        percentage_layout = QHBoxLayout()
        percentage_layout.addWidget(label_percentage)
        percentage_layout.addWidget(self.percentage_input)

        main_layout.addLayout(percentage_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Month", "Total", "Income", "Outcome", "Passive"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #71a300;
                color: #FCF8E8;
                gridline-color: #000000;
            }
            QHeaderView::section {
                background-color: #558B2F;
                color: white;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #558B2F;
            }
        """)

        self.table.setRowCount(0)

        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("คำนวณ")

        green_btn_style ="""
            QPushButton {
                background-color: #44aa44;
                color: #e0e0e0;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: bold;
            }
        """

        self.start_button.setStyleSheet(green_btn_style)
        self.start_button.clicked.connect(self.calculate_total)

        main_layout.addWidget(self.start_button)

        self.setLayout(main_layout)

    def get_last_total(self):
        if not self.data:
            try:
                return int(self.table.item(0, 1).text())
            except:
                return 0
        return self.data[-1]["total"]
    
    def add_row_to_table(self, month, total, income, outcome, passive=0):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(month)))
        self.table.setItem(row, 1, QTableWidgetItem(str(total)))
        self.table.setItem(row, 2, QTableWidgetItem(str(income)))
        self.table.setItem(row, 3, QTableWidgetItem(str(outcome)))
        self.table.setItem(row, 4, QTableWidgetItem(str(passive)))

    def calculate_total(self):
        try:
            income = int(self.income_input.text() or 0)
            outcome = int(self.outcome_input.text() or 0)
            percent = float(self.percentage_input.text() or 0)

            last_total = self.get_last_total()
            passive = int((last_total * percent) / 100)
            new_total = last_total + income - outcome + passive
            month = len(self.data) + 1

            self.data.append ({
                "month": month,
                "total": new_total,
                "income": income,
                "outcome": outcome,
                "passive": passive,
            })

            self.add_row_to_table(month, new_total, income, outcome, passive)
            
            self.income_input.clear()
            self.outcome_input.clear()
            self.percentage_input.clear()
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้องนะ", "กรอกตัวเลขใหม่ให้ถูก")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SangtongWallet()
    window.show()
    sys.exit(app.exec_())
