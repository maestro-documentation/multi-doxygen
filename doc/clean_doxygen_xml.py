import sys
import xml.etree.ElementTree as ET

def clean_doxygen_index(xml_path):
    """
    Parses a Doxygen index.xml file and removes any <compound> elements
    that have an empty <name> tag. This prevents Breathe from crashing on
    anonymous structs/enums.

    Args:
        xml_path (str): The full path to the index.xml file.
    """
    try:
        print(f"--- Cleaning Doxygen XML: {xml_path}")
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find all <compound> elements that are direct children of the root.
        # We build a list of nodes to remove first, because removing while iterating
        # is problematic.
        compounds_to_remove = []
        for compound in root.findall('compound'):
            name_element = compound.find('name')
            # Check if the name element exists and its text is None or empty.
            if name_element is not None and not name_element.text:
                refid = compound.get('refid', 'N/A')
                print(f"  - Found compound with empty name (refid: {refid}). Marking for removal.")
                compounds_to_remove.append(compound)

        if not compounds_to_remove:
            print("  - No empty-named compounds found. File is clean.")
            return

        # Now, remove the marked compounds from the root element.
        for compound in compounds_to_remove:
            root.remove(compound)

        # Overwrite the original index.xml file with the cleaned version.
        # We use 'wb' to preserve the original encoding (usually UTF-8).
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        print(f"--- Successfully cleaned and saved {xml_path}")

    except FileNotFoundError:
        print(f"  - WARNING: File not found: {xml_path}. Skipping.")
    except ET.ParseError as e:
        print(f"  - ERROR: Failed to parse XML file {xml_path}: {e}")
    except Exception as e:
        print(f"  - ERROR: An unexpected error occurred: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python clean_doxygen_xml.py <path_to_index.xml>")
        sys.exit(1)

    index_file = sys.argv[1]
    clean_doxygen_index(index_file)
