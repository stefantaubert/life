#Executes the preprocessing
#Reading and Saving the Train Set

from data_reading import imageList_generator
import settings_main as settings

if __name__ == '__main__':
    imageList_generator.generate__train_image_list()
    #ImageToCSVConverter(1).create_datasets()
    #ImageToCSVConverter(2).create_datasets()
    #ImageToCSVConverter(32).create_datasets()