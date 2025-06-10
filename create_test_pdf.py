from fpdf import FPDF

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open("test_college_info.txt", "r") as file:
        for line in file:
            pdf.cell(200, 10, txt=line.strip(), ln=True)
    
    pdf.output("test_college_info.pdf")

if __name__ == "__main__":
    create_pdf() 