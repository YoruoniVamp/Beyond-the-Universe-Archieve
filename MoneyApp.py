import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QDialog
)
from PyQt5.QtGui import QFont
from datetime import datetime

now = datetime.now()
current_date = now.strftime("%d-%m-%Y")

class SangtongWallet(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.wallet_info = []
        self.setWindowTitle("WalletBySangtong")
        self.setGeometry(500, 500, 557, 500)

        self.setStyleSheet("background-color: #121916; color: #DCDCDC")

        label_font = QFont("Segoe UI", 10, QFont.Bold)
        button_font = QFont("Segoe UI", 10)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(2)

        label_income = QLabel("Income : ")
        label_income.setFont(label_font)

        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("เขียนยอดเงิน")
        self.income_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        income_layout = QHBoxLayout()
        income_layout.addWidget(label_income)
        income_layout.addWidget(self.income_input)
        
        left_layout.addLayout(income_layout)

        label_outcome = QLabel("Outcome :")
        label_outcome.setFont(label_font)
        self.outcome_input = QLineEdit()
        self.outcome_input.setPlaceholderText("เขียนยอดเงิน")
        self.outcome_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        outcome_layout = QHBoxLayout()
        outcome_layout.addWidget(label_outcome)
        outcome_layout.addWidget(self.outcome_input)
        
        left_layout.addLayout(outcome_layout)

        label_percentage = QLabel("Passive Income Percent :")
        label_percentage.setFont(label_font)
        self.percentage_input = QLineEdit()
        self.percentage_input.setPlaceholderText("อัตรากำไร")
        self.percentage_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        percentage_layout = QHBoxLayout()
        percentage_layout.addWidget(label_percentage)
        percentage_layout.addWidget(self.percentage_input)

        left_layout.addLayout(percentage_layout)
        
        label_reason = QLabel("Reason :")
        label_reason.setFont(label_font)
        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("เหตุผล")
        self.reason_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")

        reason_layout = QHBoxLayout()
        reason_layout.addWidget(label_reason)
        reason_layout.addWidget(self.reason_input)

        right_layout = QVBoxLayout()
        right_layout.addLayout(reason_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setFixedSize(517,250)
        self.table.setHorizontalHeaderLabels(["Month", "Total", "Income", "Outcome", "Passive"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #5BB450;
                color: #FCF8E8;
                gridline-color: #000000;
            }
            QHeaderView::section {
                background-color: #175022;
                color: white;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #175022;
            }
        """)

        self.table.setRowCount(0)

        left_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("EndMonth")

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

        self.update_button = QPushButton("Income Update")
        self.update_button.setStyleSheet(green_btn_style)
        self.update_button.clicked.connect(self.update_income)

        self.outcome_button = QPushButton("Outcome Update")
        self.outcome_button.setStyleSheet(green_btn_style)
        self.outcome_button.clicked.connect(self.update_outcome)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.setStyleSheet(green_btn_style)
        self.clear_button.clicked.connect(self.clear)

        blue_btn_style = """
            QPushButton {
                background-color: #C3EEFA;
                color: #000000;
                border-radius 8px;
                padding: 8px 18px;
                font-weight: bold;
            }
        """

        self.fake_color_button = QPushButton("สีแอพ")
        self.fake_color_button.setStyleSheet(blue_btn_style)
        self.fake_color_button.clicked.connect(self.fake)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.outcome_button)
        left_layout.addLayout(button_layout)

        left_layout.addWidget(self.fake_color_button)

        right_layout.addWidget(self.clear_button)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ค้าหาจากวันที่, เดือน, หรือปี")
        self.search_input.setStyleSheet("background-color: #7EC636; color: #FFFFFF; border: 1px solid #44aa44; padding: 5px;")
        
        search_button = QPushButton("➤")
        search_button.setStyleSheet(green_btn_style)
        search_button.clicked.connect(self.search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        right_layout.addLayout(search_layout)

        self.load_data()
        for entry in self.data:
            self.add_row_to_table(
                entry.get("month", len(self.data)),
                entry.get("total", 0),
                entry.get("income", 0),
                entry.get("outcome", 0),
                entry.get("passive", 0),
            )

        main_layout.addLayout(left_layout, 2)

        self.right_table = QTableWidget()
        self.right_table.setColumnCount(3)
        self.right_table.setFixedSize(452, 380)
        self.right_table.setHorizontalHeaderLabels(["Income/Outcome", "Date", "Reason"])
        self.right_table.setColumnWidth(0, 120)
        self.right_table.setColumnWidth(1, 80)
        self.right_table.setColumnWidth(2, 250)
        self.right_table.setStyleSheet("""
            QTableWidget {
                background-color: #5BB450;
                color: #FCF8E8;
                gridline-color: #000000;
            }
            QHeaderView::section {
                background-color: #175022;
                color: white;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #175022;
            }
        """)

        right_layout.addWidget(self.right_table)

        main_layout.addLayout(right_layout, 1)
        
        self.setLayout(main_layout)

    def load_data(self):
        try:
            with open("Money.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = [{
                "month": 1,
                "income": 0,
                "outcome": 0,
                "passive": 0,
                "total": 0,
            }]
    
    def load_walletdata(self):
        try:    
            with open("walletInfo.json", "r", encoding="utf-8") as f:
                self.wallet_info = json.load(f)
        except FileNotFoundError:
            self.wallet_info = []
    
    def clear(self):
        reply = QMessageBox.question(
            self,
            "ยืนยันการลบ",
            "แน่ใจแล้วนะว่าจะลบประวัติ",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.right_table.setRowCount(0)
            self.table.setRowCount(0)

            self.wallet_info = []
            self.save_walletdata()

            self.data = [{
                "month": 1,
                "income": 0,
                "outcome": 0,
                "passive": 0,
                "total": 0,
            }]
            self.save_data()
            self.add_row_to_table(1, 0, 0, 0, 0)

            QMessageBox.information(self, "สำเร็จ", "ลบประวัติแล้ว")

    def get_last_total(self):
        if not self.data:
            try:
                return int(self.table.item(0, 1).text())
            except:
                return 0
        return self.data[-1]["total"]
    
    def get_last_income(self):
        if not self.data:
                return 0
        return self.data[-1]["income"]
    
    def get_last_outcome(self):
        if not self.data:
                return 0
        return self.data[-1]["outcome"]
    
    def add_row_to_table(self, month, total, income, outcome, passive=0):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(month)))
        self.table.setItem(row, 1, QTableWidgetItem(str(total)))
        self.table.setItem(row, 2, QTableWidgetItem(str(income)))
        self.table.setItem(row, 3, QTableWidgetItem(str(outcome)))
        self.table.setItem(row, 4, QTableWidgetItem(str(passive)))
    
    def update_outcome(self):
        try:
            outcome = int(self.outcome_input.text() or 0)
            reason = self.reason_input.text()
            if not self.data:
                QMessageBox.warning(self, "NoInfo", "Pls StartNewMonth")
                return
            last_entry = self.data[-1]
            last_entry["outcome"] += outcome
            last_entry["total"] = last_entry["total"] - outcome

            self.save_data()

            row = self.table.rowCount() - 1
            self.table.setItem(row, 1, QTableWidgetItem(str(last_entry["total"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(last_entry["outcome"])))

            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")

            new_row = self.right_table.rowCount()
            self.right_table.insertRow(new_row)
            self.right_table.setItem(new_row, 0, QTableWidgetItem(f"-{outcome}"))
            self.right_table.setItem(new_row, 1, QTableWidgetItem(date_str))
            self.right_table.setItem(new_row, 2, QTableWidgetItem(str(reason)))

            self.wallet_info.append({
                "type": "outcome",
                "amount": outcome,
                "date": date_str,
                "reason": reason
            })

            self.save_walletdata()

            self.outcome_input.clear()
            self.reason_input.clear()
        
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้อง", "กรอกข้อมูลให้ถูกต้อง")

    def update_income(self):
        try:
            income = int(self.income_input.text() or 0)
            reason = self.reason_input.text()

            if not self.data:
                QMessageBox.warning(self, "NoInfo", "Pls StartNewMonth")
                return
            
            last_entry = self.data[-1]
            last_entry["income"] += income
            last_entry["total"] = last_entry["total"] + income

            self.save_data()
            
            row = self.table.rowCount() - 1
            self.table.setItem(row, 1, QTableWidgetItem(str(last_entry["total"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(last_entry["income"])))

            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")

            new_row = self.right_table.rowCount()
            self.right_table.insertRow(new_row)
            self.right_table.setItem(new_row, 0, QTableWidgetItem(f"+{income}"))
            self.right_table.setItem(new_row, 1, QTableWidgetItem(date_str))
            self.right_table.setItem(new_row, 2, QTableWidgetItem(str(reason)))

            self.wallet_info.append({
                "type": "income",
                "amount": income,
                "date": date_str,
                "reason": reason
            })

            self.save_walletdata()
            
            self.income_input.clear()
            self.reason_input.clear()

        except ValueError:
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้อง", "กรอกข้อมูลให้ถูกต้อง")

    def calculate_total(self):
        try:
            income = int(self.income_input.text() or 0)
            outcome = int(self.outcome_input.text() or 0)
            percent = float(self.percentage_input.text() or 0)

            last_total = self.get_last_total()
            passive = int((last_total * percent) / 100)
            new_total = last_total + income - outcome + passive
            month = len(self.data) + 1

            new_entry = {
                "month" : month,
                "income": income,
                "outcome": outcome,
                "passive": passive,
                "total": new_total
            }

            self.data.append(new_entry)
            self.save_data()
            self.add_row_to_table(**new_entry)
            
            self.income_input.clear()
            self.outcome_input.clear()
            self.percentage_input.clear()
            
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลไม่ถูกต้องนะ", "กรอกตัวเลขใหม่ให้ถูก")
   
    def save_data(self):
        with open("Money.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def save_walletdata(self):
        with open("walletInfo.json", "w", encoding="utf-8") as f:
            json.dump(self.wallet_info, f, indent=2, ensure_ascii=False)
    
    def search(self):
        keyword = self.search_input.text().strip().lower()
        self.right_table.setRowCount(0)

        if not self.wallet_info:
            self.load_walletdata()

        for entry in self.wallet_info:
            if (
                keyword in entry["date"].lower()
                or keyword in entry["reason"].lower()
                or keyword in entry["type"].lower()
                or keyword in str(entry["amount"])
            ):
                new_row = self.right_table.rowCount()
                self.right_table.insertRow(new_row)

                symbol = "+" if entry["type"] == "income" else "-"
                self.right_table.setItem(new_row, 0, QTableWidgetItem(f"{symbol}{entry['amount']}"))
                self.right_table.setItem(new_row, 1, QTableWidgetItem(entry["date"]))
                self.right_table.setItem(new_row, 2, QTableWidgetItem(entry["reason"]))

    def fake(self):
        reply = QMessageBox.question(
            self,
            "บ้าป่าว",
            "คือคนทำชอบสีเขียวไง ไม่ให้เปลี่ยนเข้าใจป่าว",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            dialog = MemeDialog()
            dialog.exec_()

class MemeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ไม่เข้าใจอ๋อ")
        self.setFixedSize(250, 100)
        self.setStyleSheet("background-color: #121916; color: #DCDCDC")

        layout = QVBoxLayout()
        label = QLabel("เคเลย")
        label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(label)

        close_btn = QPushButton("โอเค")
        close_btn.setStyleSheet("background-color: #44aa44; color: #DCDCDC")
        close_btn.clicked.connect(self.exit_app)

        layout.addWidget(close_btn)
        self.setLayout(layout)

    def exit_app(self):
        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SangtongWallet()
    window.show()
    sys.exit(app.exec_())
