import os


collection_location = "/Volumes/SSD"


collection_folder   = os.path.join( collection_location, "collection" )
wordlist_file       = os.path.join(collection_folder, "wordlist.txt")

def create_collection_folder():
    if os.path.exists(collection_folder) and os.path.isdir(collection_folder):
        print('Folder already exists')
    else:
        os.mkdir(collection_folder)
        with open(wordlist_file, "w") as file:
            file.write('')


def start_collection( word ):
    subdirs = dirs = [d for d in os.listdir(collection_folder) if os.path.isdir(os.path.join(collection_folder, d))]

    dir_name = 0

    if dirs:
        max_folder = max(dirs)
        print("Max folder number:", max_folder)
        dir_name = int(max_folder) + 1

    os.mkdir(os.path.join(collection_folder, str(dir_name)))

    with open(wordlist_file, 'a') as file:
        file.write(f"{word}, {dir_name}\n")

    sample_size = 60
    for _ in range(sample_size):
        pass


create_collection_folder()


word = input('Enter word to manually collect : ')
start_collection(word)