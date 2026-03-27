from fpdf import FPDF
from datetime import datetime
import os

class MandeshReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'MANDESH SUITE - INTELLIGENCE REPORT', 0, 1, 'C')
        self.ln(5)

def generate_pdf(target_info, hunt_data):
    pdf = MandeshReport()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Target: {target_info}", 1, 1)
    pdf.ln(5)

    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, f"Latest Intelligence Findings:\n\n{hunt_data}")
    
    name = f"Report_{datetime.now().strftime('%H%M')}.pdf"
    pdf.output(name)
    print(f"[+] PDF Report Saved: {name}")

if __name__ == "__main__":
    # Pull data from hunt_results.txt if it exists
    data = "No data found."
    if os.path.exists("hunt_results.txt"):
        with open("hunt_results.txt", "r") as f:
            data = f.read()

    target = input("Enter Target Identifier (Name/Email): ")
    generate_pdf(target, data)
