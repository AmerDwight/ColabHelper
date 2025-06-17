######### Python 檔案轉Base64
import base64
from tkinter import Tk, filedialog

def encode_file_to_base64(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        file_content = file.read()
    
    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    with open(output_file_path, 'w') as file:
        file.write(base64_encoded_content)

def main():
    # Initialize Tkinter root
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select the input file
    input_file_path = filedialog.askopenfilename(title="Select a file to encode")
    if not input_file_path:
        print("No file selected. Exiting.")
        return

    # Open file dialog to select the output file path
    output_file_path = filedialog.asksaveasfilename(
        title="Select the destination file", defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not output_file_path:
        print("No output file selected. Exiting.")
        return

    # Encode the file content and save to the output file
    encode_file_to_base64(input_file_path, output_file_path)
    print(f"File has been encoded and saved to {output_file_path}")

if __name__ == "__main__":
    main()

