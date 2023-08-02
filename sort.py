import os
import sys
import shutil

def normalize(name):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ь': '', 'Ю': 'IU', 'Я': 'IA'
    }
    
    result = []
    for char in name:
        if char.isalnum() or char.isspace() or char == '.':
            result.append(char)
        elif char in translit_dict:
            result.append(translit_dict[char])
        else:
            result.append('_')
    return ''.join(result)

def sort_files(folder_path):
    extensions = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'video': ('AVI', 'MP4', 'MOV', 'MKV'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }
    
    known_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split('.')[-1].upper()
            known = False
            
            for category, ext_list in extensions.items():
                if file_extension in ext_list:
                    target_folder = os.path.join(folder_path, category)
                    known_extensions.add(file_extension)
                    known = True
                    
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    target_path = os.path.join(target_folder, normalize(file))
                    source_path = os.path.join(root, file)
                    shutil.move(source_path, target_path)
                    break
            
            if not known:
                unknown_extensions.add(file_extension)
    
    return known_extensions, unknown_extensions

def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        known_extensions, unknown_extensions = sort_files(folder_path)
        remove_empty_folders(folder_path)