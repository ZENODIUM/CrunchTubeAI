from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=False)  # Disable automatic page breaks
        self.column_width = 90  # Width of each column
        self.left_margin = 10  # Starting x position for the left column
        self.right_margin = 110  # Starting x position for the right column
        self.current_column = 0  # Track the current column (0 = left, 1 = right)
        self.y_start = 30  # Starting y position for content

    def add_title(self, title):
        """Add a centered title to the page."""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(10)  # Add some vertical space after the title

    def switch_column(self):
        """Switch to the right column or add a new page if needed."""
        if self.current_column == 0:
            # Move to the right column
            self.set_xy(self.right_margin, self.y_start)
            self.current_column = 1
        else:
            # Add a new page and reset to the left column
            self.add_page()
            self.set_xy(self.left_margin, self.y_start)
            self.current_column = 0

    def add_section(self, title, content):
        """Add a section with a title and content."""
        # Check if we need to switch columns or add a new page before adding content
        if self.get_y() > 270:  # If content exceeds page height
            self.switch_column()

        # Set position based on current column
        if self.current_column == 0:
            x = self.left_margin
            y = max(self.get_y(), self.y_start)
        else:
            x = self.right_margin
            y = max(self.get_y(), self.y_start)

        # Draw a box for the title
        self.set_fill_color(80, 200, 120)  # Light gray color for title box
        self.rect(x, y, self.column_width, 10, 'F')

        # Add section title
        self.set_xy(x, y)
        self.set_font('Arial', 'B', 12)
        self.multi_cell(self.column_width, 10, title)

        # Adjust position for content after title
        y = self.get_y()

        # Calculate content box height dynamically
        # Dynamically calculate the height of the content box based on multi_cell rendering
        self.set_xy(x, y)
        self.set_font('Arial', '', 8)

        # Start recording the current Y position before adding the content
        start_y = self.get_y()
        self.multi_cell(self.column_width, 8, content)  # Render the content
        end_y = self.get_y()  # Get Y position after rendering

        # Calculate actual height of the rendered content
        content_height = end_y - start_y

        # Draw a box for the content using the calculated height
        self.set_fill_color(153, 255, 153)  # Lighter gray color for content box
        self.rect(x, y, self.column_width, content_height, 'F')

        # Reposition to add text again (since rect overwrites it)
        self.set_xy(x, start_y)
        self.multi_cell(self.column_width, 8, content)


def generate_pdf(content, title="Python Cheat Sheet", output_file="output.pdf"):
    """Generate a PDF with the given content."""
    pdf = PDF()
    pdf.add_page()
    pdf.add_title(title)
    
    # Add sections to the PDF
    for section_title, section_content in content:
        pdf.add_section(section_title, section_content)
    
    # Save the PDF
    pdf.output(output_file)

# Example usage
# sections = [
#     ('Variables', 'x = 5\ny = "Hello"\n'),
#     ('Data Types', 'int, float, str, list, tuple, dict, set, bool\n'),
#     ('Control Flow', 'if condition:\n    # do something\nelif condition:\n    # do something else\nelse:\n    # fallback\n'),
#     ('Loops', 'for i in range(5):\n    print(i)\nwhile condition:\n    # do something\n'),
#     ('Functions', 'def my_function(arg):\n    return arg * 2\n'),
# ]

# generate_pdf(sections, title="Cheat Sheet", output_file="pdfs/cheat_sheet.pdf")
