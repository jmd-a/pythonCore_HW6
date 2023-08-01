import os
import sys
import shutil

image_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
document_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
audio_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
archive_extensions = ('ZIP', 'GZ', 'TAR')

categories = {
    'images': image_extensions,
    'video': video_extensions,
    'documents': document_extensions,
    'audio': audio_extensions,
    'archives': archive_extensions,
}

def normalize(filename):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G',
        'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K',
        'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ь': '', 'Ю': 'IU', 'Я': 'IA',
    }

    translit_name = ''
    for char in filename:
        translit_name += translit_dict.get(char, char)

    normalized_name = ''.join(c if c.isalnum() else '_' for c in translit_name)

    return normalized_name

def process_folder(folder_path):
    known_extensions = set()
    unknown_extensions = set()

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            process_folder(item_path)

        elif os.path.isfile(item_path):
            filename, file_extension = os.path.splitext(item)

            normalized_name = normalize(filename)
            new_filename = normalized_name + file_extension
            new_path = os.path.join(folder_path, new_filename)

            os.rename(item_path, new_path)

            moved = False
            for category, extensions in categories.items():
                if file_extension.upper()[1:] in extensions:
                    moved = True
                    target_folder = os.path.join(folder_path, category)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.move(new_path, os.path.join(target_folder, new_filename))
                    known_extensions.add(file_extension.upper())
                    break

            if not moved:
                unknown_extensions.add(file_extension.upper())

    return known_extensions, unknown_extensions

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python sort.py /path/to/folder")
    else:
        folder_path = sys.argv[1]
        known_ext, unknown_ext = process_folder(folder_path)