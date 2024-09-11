import streamlit as st
from io import StringIO
import qrcode
import xml.etree.ElementTree as ET

class LargerSquareModulesSvgDrawer(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, *args, **kwargs):
        self.border = border
        self.width = width
        self.box_size = box_size
        self._svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
        self._svg.set("width", f"{(width + border * 2) * box_size}mm")
        self._svg.set("height", f"{(width + border * 2) * box_size}mm")
        self._svg.set("viewBox", f"0 0 {(width + border * 2) * box_size} {(width + border * 2) * box_size}")
        super().__init__(border, width, box_size, *args, **kwargs)

    def drawrect(self, row, col):
        size = self.box_size
        x = (col + self.border) * size
        y = (row + self.border) * size
        radius = size / 8  
        gap = 0.05 * size  

        path_data = f"""
        M {x + gap + radius},{y + gap} 
        h {size - 2 * (gap + radius)} 
        a {radius},{radius} 0 0 1 {radius},{radius}
        v {size - 2 * (gap + radius)} 
        a {radius},{radius} 0 0 1 -{radius},{radius}
        h -{size - 2 * (gap + radius)} 
        a {radius},{radius} 0 0 1 -{radius},-{radius}
        v -{size - 2 * (gap + radius)} 
        a {radius},{radius} 0 0 1 {radius},-{radius}
        z
        """

        path_element = ET.Element("path", d=path_data.strip(), fill="black")
        self._svg.append(path_element)

    def save(self, stream, kind=None):
        tree = ET.ElementTree(self._svg)
        tree.write(stream, encoding="unicode")

class PreciseRoundedSvgDrawer(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, *args, **kwargs):
        self.border = border
        self.width = width
        self.box_size = box_size
        self._svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", version="1.1")
        self._svg.set("width", f"{(width + border * 2) * box_size}mm")
        self._svg.set("height", f"{(width + border * 2) * box_size}mm")
        self._svg.set("viewBox", f"0 0 {(width + border * 2) * box_size} {(width + border * 2) * box_size}")
        super().__init__(border, width, box_size, *args, **kwargs)

    def drawrect(self, row, col):
        size = self.box_size
        x = (col + self.border) * size
        y = (row + self.border) * size
        radius = size / 3 

        path_data = f"""
        M {x + radius},{y} 
        h {size - 2 * radius} 
        a {radius},{radius} 0 0 1 {radius},{radius}
        v {size - 2 * radius} 
        a {radius},{radius} 0 0 1 -{radius},{radius}
        h -{size - 2 * radius} 
        a {radius},{radius} 0 0 1 -{radius},-{radius}
        v -{size - 2 * radius} 
        a {radius},{radius} 0 0 1 {radius},-{radius}
        z
        """

        path_element = ET.Element("path", d=path_data.strip(), fill="black")
        self._svg.append(path_element)

    def save(self, stream, kind=None):
        tree = ET.ElementTree(self._svg)
        tree.write(stream, encoding="unicode")

def box(link, name):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,  
    box_size=40,
    border=2,
)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(image_factory=LargerSquareModulesSvgDrawer)

    larger_square_svg_path = f"{name}_box.svg"

    return img, larger_square_svg_path

def round(link, name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(image_factory=PreciseRoundedSvgDrawer)

    rounded_svg_path = f"{name}_round.svg"

    return img, rounded_svg_path

# Streamlit App
st.title("QR Code Generator")

# Input for the link and name
link = st.text_input("Enter the link for QR code:")
name = st.text_input("Enter a name for the QR code file:")

# Generate QR codes when the button is clicked
if st.button("Generate QR Codes"):
    if link and name:
        # Generate QR codes
        img_box, box_path = box(link, name)
        img_round, round_path = round(link, name)

        # Convert SVG data to a displayable format
        svg_box = StringIO()
        img_box.save(svg_box)
        svg_box.seek(0)
        svg_box_data = svg_box.getvalue()

        svg_round = StringIO()
        img_round.save(svg_round)
        svg_round.seek(0)
        svg_round_data = svg_round.getvalue()

        # Display QR codes using markdown with SVG data
        st.subheader("Larger Square Modules QR Code:")
        st.markdown(f'<img src="data:image/svg+xml;utf8,{svg_box_data}" width="1" />', unsafe_allow_html=True)

        st.subheader("Precise Rounded QR Code:")
        st.markdown(f'<img src="data:image/svg+xml;utf8,{svg_round_data}" width="300" />', unsafe_allow_html=True)

        # Buttons to save SVG files
        st.download_button(
            "Download Larger Square QR Code SVG",
            data=svg_box_data,
            file_name=box_path,
            mime="image/svg+xml",
        )

        st.download_button(
            "Download Precise Rounded QR Code SVG",
            data=svg_round_data,
            file_name=round_path,
            mime="image/svg+xml",
        )
    else:
        st.error("Please enter both the link and the name for the QR code.")
