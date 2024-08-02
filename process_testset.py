import os
import shutil
import sys
from preprocessing.preprocess import main as preprocess
from preprocessing.rearrange import main as rearrange
from training.test import main as tests

detector_config_map = {
    'xception': "./training/config/detector/xception.yaml",
    'ucf': "./training/config/detector/ucf.yaml",
    'capsule_net': "./training/config/detector/capsule_net.yaml",
}

detector_weights_map = {
    'xception': "./training/weights/xception_best.pth",
    'ucf': "./training/weights/ucf_best.pth",
    'capsule_net': "./training/weights/capsule_best.pth",
}


if __name__ == '__main__':
    folder_name = sys.argv[1]
    model = sys.argv[2]

    detector_config = detector_config_map[model]
    detector_weights = detector_weights_map[model]

    src_dir = os.path.join(os.getcwd(), f'../deepfakebench-frontend/uploads/{folder_name}')
    dest_dir = os.path.join(os.getcwd(), '../datasets/TestSet/fake')
    
    shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)

    os.chdir(os.path.join(os.getcwd(), './preprocessing'))
    preprocess()
    print("Stage 1: Frames and Landmarks Generated!")
    sys.stdout.flush()
    
    rearrange()
    print("Stage 2: JSON File Generated!")
    sys.stdout.flush()
    
    os.chdir(os.path.join(os.getcwd(), '../'))
    
    tests(["--detector_path", detector_config, "--test_dataset", "TestSet", "--weights_path", detector_weights])
    shutil.move(os.path.join(os.getcwd(), f'./results/{model}/TestSet_results.csv'), os.path.join(src_dir, 'frame.csv'))
    shutil.move(os.path.join(os.getcwd(), f'./results/{model}/TestSet_video_results.csv'), os.path.join(src_dir, 'video.csv'))
    print("Stage 3: Results Generated!")
    sys.stdout.flush()
