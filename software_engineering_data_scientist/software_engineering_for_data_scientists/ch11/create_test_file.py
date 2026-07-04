import time

def create_file(dir_name: str):

    current_time = str(int(time.time()))
    path = "sample_file_" + current_time + ".txt"
    path = dir_name + "/" + path

    with open(path, "w+") as file_obj:
        file_obj.write("test")

create_file("C:/technical_documents/book_reviews/manning/software_engineering_data_scientist/software_engineering_for_data_scientists/ch11")