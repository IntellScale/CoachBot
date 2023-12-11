from docx import Document
import os


def create_word_document(content, output_file_name):
    
    doc = Document()
    doc.add_paragraph(content)

    # Save the document
    doc.save(output_file_name)
    print(f'Document saved to: {output_file_name}')

def delete_document(file_path = 'output_report.docx'):
    try:
        os.remove(file_path)
        print(f'File {file_path} deleted successfully.')
    except OSError as e:
        print(f"Error deleting the file: {e}")

