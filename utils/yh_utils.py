'''
yh_utils
  - dataset 생성 등에서 필요한 기본 utils

1.0.0.0
1.0.0.1 2022.01.13
  - move_files_to_folders() : *exts 파라미터 추가
  - collect_files_to_folder() : *exts 파라미터 추가

1.0.0.2 2022.02.14
  - read_json_list() : json에서 특정 key의 value만 추출할 때와 전체 추출할 때 모두 사용할 수 있게 수정

2022.04.06.
  - loadTextFile()
  - cleanGTfile() : gt.txt 파일에서 clean.txt 파일에 있는 특수기호들 바꿔주기

2022.04.08.
  - gtToCorpus() : gt.txt에서 정답만 추출해서 corpus로 변경

'''

from lib2to3.pytree import convert
import os
import random
from xml.etree.ElementTree import tostring
import pandas as pd
import numpy as np
import json
import glob
import shutil
import re
# import cv2
# import tensorflow as tf
# from pdf2image import convert_from_path
# from wand import image


'''파일 로드 관련'''
#파일 목록 가져오기
def get_file_list(dir, ext='.jpg', is_whole=False):

    if is_whole: #is_whole : dir 경로+파일명 리스트 반환
      file_names = glob.glob(dir + "\\*" + ext)

    else: #파일명만 반환
      file_names = [entry for entry in os.listdir(dir) if os.path.isfile(os.path.join(dir, entry)) and entry.endswith(ext)]

    return file_names


def getHierarchicalFilePaths(root, select_dir='/'):
    '''TRBA(naver clova) dataset.py hierarchical_dataset() 응용'''

    list_path = []
    for dirpath, dirnames, filenames in os.walk(root + '/'):
        if not dirnames: #가장 하위 폴더
            select_flag = False
            for selected in select_dir:
                if selected in dirpath: #현재 폴더에 selected(파일이 담긴 폴더)가 있을 때
                    select_flag = True

            if select_flag:
                paths = get_file_list(dirpath, ext='.txt', is_whole=True)
                list_path.extend(paths)

    return list_path


#csv 목록에서 df 가져오기
def df_list_from_csv(file_names, csv_dir="./"):
    df_list = []

    # print('img_name:', img_name)
    for file_name in file_names:
        data_ = csv_to_df(file_name, csv_dir)
        df_list.append(data_)

    return df_list

#csv 이름 + csv_dir에서 df 가져오기
def csv_to_df(file_name, csv_dir="./"):
    df_name = file_name if file_name.endswith('.csv') else file_name[0:file_name.find('.')] + '.csv'  # find(글자) 글자 인덱스

    # print(csv_dir)
    data_ = pd.read_csv(os.path.join(csv_dir, df_name), header=0, index_col=0, squeeze=True)
    # print(answer)

    # for key, value in answer.items():
    #     print(key)
    #     print(value)

    return data_


# json list 읽기
def read_json_list(file_dir, key=''):
  file_names = [entry for entry in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, entry)) and entry.endswith('.json')]
  # file_names = ["주민등록증_정인식_741103_19990930_1904_조도일반_skew_검정_GalaxyNote3_000213_AutoCrop.json", "주민등록증_정인식_741103_19990930_1904_조도일반_skew_검정_GalaxyNote3_000223_AutoCrop.json"]

  json_list = []

  for file in file_names:
    file_path = os.path.join(file_dir, file)
    if not os.path.isfile(file_path):
      raise FileNotFoundError(file_path)

    with open(file_path, "r", encoding="utf-8") as json_file:
      json_data = json.load(json_file)

    # print(json_data)
    if key != '': #list형 json이면 안됨.
      json_list.append(json_data[key])
      print(json_data[key])
    else :
      json_list.append(json_data)

  return file_names, json_list



def loadTextFile(path='make_focus/chars/list_focus_chars.txt'):
# txt file cant be uploaded...

    with open(path, 'r', encoding='utf-8') as f:
        text = f.readlines()

    list_text = [word.replace('\n', '') for word in text]

    return list_text



'''corpus 관련'''
def cleanGTfile(gt_path='gt.txt', clean_path='clean_chars.txt'):
    print('-- list of characters to clean texts')

    with open(clean_path, 'r', encoding='utf-8') as f:
        list_text_clean = f.readlines()

    with open(gt_path, 'r', encoding='utf-8') as f:
        list_gt = f.readlines()

    for text in list_text_clean:
        clean = text.replace('\n', '').split('\t')

        for line in list_gt:
            gt = line.replace('\n', '').split('\t')
            answer = gt[1]
            if clean[0] in gt[1]:
                answer = answer.replace(clean[0], clean[1])
                list_gt[list_gt.index(line)] = gt[0] + '\t' + answer #gt[0]+'\t'+gt[1]

    with open(gt_path, 'w', encoding='utf-8') as f:
        gt_text = "\n".join(list_gt)
        f.write(gt_text)

def gtToCorpus(gt_path='data/gt_total_0407.txt', save_path='data/total_0407.txt'):

  text = loadTextFile(gt_path)
  save = [line.split('\t')[1] for line in text] #정답만 저장

  with open(save_path, 'w', encoding='utf8') as f:
      save_txt = "\n".join(save)
      f.write(save_txt)

  return save


'''학습용 데이터셋 파일 폴더 경로 생성 관련'''
#파일 경로(디렉토리, 이름) 만들기
def make_file_path(save_name, base_dir="", mid_dir="", is_train=False):

    if is_train: file_dir = os.path.join(base_dir, 'train', mid_dir, 'input')
    else: file_dir = os.path.join(base_dir, 'test', mid_dir, 'input')

    # 폴더 자동 생성
    if not os.path.isdir(file_dir):
        print("[{}] 폴더 생성!".format(file_dir))
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, save_name)

    return file_dir, file_path


  #dataset path: input, answer, label 파일 경로 생성
def get_dataset_path(base_dir, mid_dir, save_name, is_train=False):

    if is_train: input_dir = os.path.join(base_dir, 'train', mid_dir, 'input')
    else: input_dir = os.path.join(base_dir, 'test', mid_dir, 'input')

    if is_train: answer_dir = os.path.join(base_dir, 'train', mid_dir, 'answer')
    else: answer_dir = os.path.join(base_dir, 'test', mid_dir, 'answer')

    if is_train: label_dir = os.path.join(base_dir, 'train', mid_dir, 'label')
    else: label_dir = os.path.join(base_dir, 'test', mid_dir, 'label')

    # 폴더 자동 생성
    if not os.path.isdir(input_dir):
        print("[{}] 폴더 생성!".format(input_dir))
        os.makedirs(input_dir)

    if not os.path.isdir(answer_dir):
        print("[{}] 폴더 생성!".format(answer_dir))
        os.makedirs(answer_dir)

    if not os.path.isdir(label_dir):
        print("[{}] 폴더 생성!".format(label_dir))
        os.makedirs(label_dir)

    input_path = os.path.join(input_dir, save_name)
    answer_path = os.path.join(answer_dir, save_name.replace('.jpg', '.csv'))
    label_path = os.path.join(label_dir, save_name.replace('.jpg', '.npy'))

    return input_path, answer_path, label_path


#dataset dir: input, answer, label 폴더 경로 생성
def get_dataset_path(base_dir, mid_dir, is_train=False):

    if is_train: input_dir = os.path.join(base_dir, 'train', mid_dir, 'input')
    else: input_dir = os.path.join(base_dir, 'test', mid_dir, 'input')

    if is_train: answer_dir = os.path.join(base_dir, 'train', mid_dir, 'answer')
    else: answer_dir = os.path.join(base_dir, 'test', mid_dir, 'answer')

    if is_train: label_dir = os.path.join(base_dir, 'train', mid_dir, 'label')
    else: label_dir = os.path.join(base_dir, 'test', mid_dir, 'label')

    # 폴더 자동 생성
    if not os.path.isdir(input_dir):
        print("[{}] 폴더 생성!".format(input_dir))
        os.makedirs(input_dir)

    if not os.path.isdir(answer_dir):
        print("[{}] 폴더 생성!".format(answer_dir))
        os.makedirs(answer_dir)

    if not os.path.isdir(label_dir):
        print("[{}] 폴더 생성!".format(label_dir))
        os.makedirs(label_dir)

    return input_dir, answer_dir, label_dir




'''파일 이동 관련'''
#file을 특정 dir list에 나누어 넣기
def move_files_to_folders(source_dir, base_dir, dir_names, file_count=100, is_copy=False, *exts):

  file_list = []
  if exts:
    for ext in exts:
      file_list.extend(get_file_list(source_dir, ext, is_whole=True))
  else:
    file_list.extend(get_file_list(source_dir, "*", is_whole=True))

  if len(dir_names) == 0:
    count = len(file_list) // file_count
    if (len(file_list) % file_count) != 0:
      count += 1

    dir_names = []
    source_dir_name = os.path.basename(source_dir) #하단 directory name

    for i in range(count):
      dir_names.append(source_dir_name + "_" + str(i+1))

  #리스트 셔플
  # random.shuffle(file_list)

  for i in range(len(dir_names)):
    folder = os.path.join(base_dir, dir_names[i])
    if not os.path.isdir(folder):
        print("[{}] 폴더 생성!".format(folder))
        os.makedirs(folder)

    for j in range(file_count):
      if j+(file_count*i) > len(file_list) - 1:
        print("--" + folder + ": " + str(j+(file_count*i)%file_count) + "개")
        break

      if is_copy:
        file_path = file_list[j+(file_count*i)]
        shutil.copy(file_path, os.path.join(folder, os.path.basename(file_path)))
        #os.path.basename(path) : path에서 기본 이름만 반환
        # print(os.path.join(folder, os.path.basename(file_path)))
        # print(os.path.basename(file_path) + " : " + folder + "로 파일 복사 완료")

      else:
        shutil.move(file_list[j+(file_count*i)], folder)
        # print(os.path.basename(file_path) + " : " + folder + "로 파일 이동 완료")

    print(folder + ": 파일 복사 완료") if is_copy else print(folder + ": 파일 이동 완료")


#여러 폴더에 나눠져 있는 파일들 하나의 폴더로 합치기
def collect_files_to_folder(source_dirs, new_dir, is_copy=False, *exts):
  file_list = []

  #파일 리스트
  for path in source_dirs:
    if exts:
      for ext in exts:
        file_list.extend(get_file_list(path, ext, is_whole=True))
    else:
      file_list.extend(get_file_list(path, ".*", is_whole=True))

  if not os.path.isdir(new_dir):
      print("[{}] 폴더 생성!".format(new_dir))
      os.makedirs(new_dir)

  for path in file_list:

    count = 1
    save_name = os.path.basename(path)
    while(os.path.isfile(os.path.join(new_dir, save_name))):
      name, ext = os.path.splitext(save_name) #파일명과 확장자 분리

      save_name = name + "_" + str(count) + ext
      count += 1

    if is_copy:
      shutil.copy(path, os.path.join(new_dir, save_name))
      #os.path.basename(path) : path에서 기본 이름만 반환
      # print(new_dir + "로 파일 복사 완료")

    else:
      if save_name != os.path.basename(path):
        path_ = os.path.join(os.path.dirname(path), save_name)
        os.rename(path, path_)
        shutil.move(path_, new_dir)
      else:
        shutil.move(path, new_dir)

      # print(new_dir + "로 파일 이동 완료")

  print(new_dir + ": 파일 복사 완료") if is_copy else print(new_dir + ": 파일 이동 완료")

      # print(os.path.dirname(path))
      # print(save_name)



'''image 관련'''
#pdf to image(jpg)
def convertPDFtoimage(root_dir, save_dir):
  print("Convert PDF to Image")

  root_dir = "C:\\workspace\\0_범용인식기\\2022_범용인식_SGI서울보증\\AI OCR PoC 샘플이미지(주석제거)"
  save_dir = "D:\\Dataset\\data_범용인식기\\2022_SGI_서울보증보험\\20220118_poc_sample"
  pdf_list = get_file_list(root_dir, ext='.pdf', is_whole=True)

  for path in pdf_list :
    file_name = os.path.splitext(os.path.basename(path))[0]
    # print(file_name)
    # with(Image(filename=path, resolution=600)) as source:
    #   images = source.sequence
    # # break

    # for i, image in enumerate(images):
    #   Image(image).save(os.path.join(save_dir, file_name + str(i) + ".jpg"), "JPEG")


def cleanCorpus(file_path, save_path):
  '''corpus clean'''
  list_text = loadTextFile(file_path)
  set_text = set(list_text)
  # print(len(list_text), '/', len(set_text))
  with open(save_path, 'w', encoding='utf8') as f:
    text_ = '\n'.join(set_text)
    f.write(text_)

def cleanGT(file_path, save_path, wrong_path):
  list_text = loadTextFile(file_path)
  list_wrong = loadTextFile(wrong_path)

  match_str = '|'.join(list_wrong)
  print(match_str)
  p = re.compile(match_str)

  result_str = []
  for text in list_text:
    if p.search(text):
      continue
    result_str.append(text)

  # print(result_str)

  set_text = set(result_str)
  print(len(list_text), '/', len(set_text))
  with open(save_path, 'w', encoding='utf8') as f:
    text_ = '\n'.join(set_text)
    f.write(text_)


if __name__ == "__main__":

  ''' 폴더 파일 분할, 모으기 '''
  # base_dir = "D:\\git_inzi\\yhpark\\Fulltext_Recognizer\\ExtractWord\\ExtractWord\\crops"
  # source_dir = "D:\\git_inzi\\yhpark\\Fulltext_Recognizer\\ExtractWord\\ExtractWord\\crops\\S22C-6e21110323140_2_2_2"

  # dir_names = [] #공백 리스트인 경우 자동으로 폴더명 생성해줌
  # for i in range(5):
  #   dir_name = "wooden_" + "{:05d}_".format(random.randint(0, 99999)) + "{:03d}".format(i)
  #   dir_names.append(dir_name)
  # dir_names = get_file_list(base_dir, '', True)
  # print(dir_names)
  # source_list = get_file_list(base_dir, "_540", True)
  # print("file_names_list : ")
  # print(file_list)
  # move_files_to_folders(source_dir, base_dir, dir_names, file_count=1500, is_copy=False)
    # dir_names = [] 전달 --> source_dir의 하단 폴더명_index로 폴더 자동 생성

  # source_dir = "D:\\Dataset\\data_범용인식기\\2021_우리카드\\우리카드_파산_법조치_우리카드_20220114_600DPI\\법조치"
  # source_list = get_file_list(source_dir, "_0", True)

  # new_dir = "D:\\Dataset\\data_범용인식기\\2021_우리카드\\우리카드_파산_법조치_우리카드_20220114_600DPI\\법조치\\0모음"
  # collect_files_to_folder(source_list, new_dir, True)

  ''' pdf to image '''

  # root_dir = "C:\\workspace\\0_범용인식기\\2022_범용인식_SGI서울보증\\AI OCR PoC 샘플이미지(주석제거)"
  # save_dir = "D:\\Dataset\\data_범용인식기\\2022_SGI_서울보증보험\\20220118_poc_sample"
  # convertPDFtoimage(root_dir, save_dir)


  '''gt to corpus'''
  # os.chdir("D:/git_etc/makeCorpus/make_corpus")
  # gtToCorpus(gt_path='data/gt/gt_gen_0412.txt', save_path='data/gt/gen_0412.txt')

  '''clean corpus'''
  file_path = 'D:\\git_etc\\makeCorpus\\make_corpus\\data\\full_word_20220406_TOTAL_old.txt'
  save_path = 'D:\\git_etc\\makeCorpus\\make_corpus\\corpus\\full_word_20220406_TOTAL_.txt'
  # cleanCorpus(file_path, save_path)

  wrong_path = 'D:\\git_etc\\makeCorpus\\make_corpus\\chars\\wrong_text.txt'
  cleanGT(file_path, save_path, wrong_path)