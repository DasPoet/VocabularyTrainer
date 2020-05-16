from threading import Thread

from fpdf import FPDF


class PDF(FPDF):
    """Class that changes the standard header of the FPDF class."""

    header_txt = "github.com/daspoet"

    def header(self):
        """Change the standard header so that it features the author of the project (Cedric Erkens)."""

        self.set_font("Arial", size=12)
        self.set_line_width(0.4)
        self.line(10, 15, 202, 15)
        self.cell(0, 0, txt=self.header_txt, align="R")
        self.ln(10)


def make_table(*, pdf_instance, content, center_content=True, show_border=True, spacing=1):
    """Add a table to a given pdf file and fill it with content."""

    row_width = int(pdf_instance.w / 2) - 15
    row_height = int(pdf_instance.font_size) + 1.25

    # maybe for future use (list the page every row is going to end up on along with that row
    # in order to allow efficient spacing so that as many words end up on one page as possible
    # (e.g. the first handmade table from in Excel))
    #
    # page_length = pdf_instance.h // pdf_instance.font_size
    # counter = Iterator(count(0))
    # words = list((next(counter), word.first_form, word.last_form) if (ind*row_height) % page_length == 0
    #              else (counter.current, word.first_form, word.last_form) for ind, word in enumerate(content))

    words = ((word.first_form, word.last_form) for word in content)

    for ind, row in enumerate(words):
        align = None
        if center_content:
            align = "C"

        # maybe for future use (see above)
        # pdf_instance.cell(row_width, row_height * spacing, txt=row[1], border=show_border, align=align)
        # pdf_instance.cell(row_width, row_height * spacing, txt=row[2], border=show_border, align=align)
        
        pdf_instance.cell(12, row_height*spacing, txt=str(ind+1), align="L")
        pdf_instance.cell(row_width, row_height*spacing, txt=row[0], border=show_border, align=align)
        pdf_instance.cell(row_width, row_height * spacing, txt=row[1], border=show_border, align=align)
        pdf_instance.ln(row_height * spacing)


def outsource_pdf_creation(*, path, content):
    """Create the pdf file using a separate thread."""

    if not path.endswith(".pdf"):
        path += ".pdf"

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    make_table(pdf_instance=pdf, content=content)

    try:
        pdf.output(path)
    except PermissionError:
        print("Permission error! Please close the pdf file")


def create_pdf(*, path, content):
    """Make a pdf file and save it to the currently chosen path."""

    Thread(target=lambda: outsource_pdf_creation(path=path, content=content)).start()
