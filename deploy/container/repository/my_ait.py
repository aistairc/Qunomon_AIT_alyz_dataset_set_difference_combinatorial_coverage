#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# | 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# | 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
# | 3|create requirements and pip install|3|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit(second cell, you set use modules.)|
# | 4|import|2|you should write use import modules.<br>but bottom lines do not edit.|should edit(first cell, you import your moduel.)|
# | 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
# | 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
# | 7|initialize|1|this cell is initialize for ait progress.|no edit|
# | 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# | 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
# |10|entrypoint|1|Call the main function.|no edit|
# |11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
# |12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|
# 
# ## notebook template revision history
# 
# ### 1.0.1 2020/10/21
# 
# * add revision history
# * separate `create requirements and pip install` editable and noeditable
# * separate `import` editable and noeditable
# 
# ### 1.0.0 2020/10/12
# 
# * new cerarion

# In[1]:


#########################################
# area:flags set
# do not edit
#########################################

# Determine whether to start AIT or jupyter by startup argument
import sys
is_ait_launch = (len(sys.argv) == 2)


# In[2]:


#########################################
# area:ait-sdk install
# do not edit
#########################################
if not is_ait_launch:
    # get ait-sdk file name
    from glob import glob
    import os

    current_dir = get_ipython().run_line_magic('pwd', '')

    ait_sdk_path = "./ait_sdk-*-py3-none-any.whl"
    ait_sdk_list = glob(ait_sdk_path)
    ait_sdk_name = os.path.basename(ait_sdk_list[-1])

    # install ait-sdk
    get_ipython().system('pip install --upgrade pip')
    get_ipython().system('pip install -q --no-deps --force-reinstall ./$ait_sdk_name')


# In[3]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()


# In[4]:


#########################################
# area:create requirements and pip install
# should edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package('pandas', '2.2.3')


# In[5]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[6]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
from pathlib import Path
from os import path

import json
from itertools import combinations
import pandas as pd


# In[7]:


#########################################
# area:import
# do not edit
#########################################

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[8]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('alyz_dataset_set_difference_combinatorial_coverage')
    manifest_genenerator.set_ait_description('画像内のオブジェクトの属性（カテゴリ）と、画像ラベルの属性（例：天候や時間帯）の組み合わせに基づいて、訓練データとテストデータ間のSDCC(Set Difference Combinatorial Coverage)を測定する。データセット間のカバレッジの差異や偏りを把握することができる。\\n \\begin{align}SDCC_{t}(D_{train,t},D_{test,t})=\\frac{|D_{train,t} \\verb|\\| D_{test,t}|}{|D_{train,t}|}\\end{align} \\n\\begin{align}D_{train,t}\\end{align}:訓練データで観測されたt-wayの属性の組み合わせ\\n\\begin{align}D_{test,t}\\end{align}:テストデータで観測されたt-wayの属性の組み合わせ\\n\\begin{align}|D_{train,t} \\verb|\\| D_{test,t}|\\end{align}:訓練データには存在するが、テストデータには存在しないt-wayの属性の組み合わせ')
    manifest_genenerator.set_ait_source_repository('https://github.com/aistairc/Qunomon_AIT_alyz_dataset_set_difference_combinatorial_coverage')
    manifest_genenerator.set_ait_version('1.2')
    manifest_genenerator.add_ait_keywords('h5')
    manifest_genenerator.add_ait_keywords('dataset')
    manifest_genenerator.add_ait_keywords('object detect')
    manifest_genenerator.add_ait_keywords('Automatic Operation')
    manifest_genenerator.add_ait_keywords('combinatorial coverage')
    manifest_genenerator.add_ait_licenses('Apache License Version 2.0')
    manifest_genenerator.set_ait_quality('https://ait-hub.pj.aist.go.jp/ait-hub/api/0.0.1/qualityDimensions/機械学習品質マネジメントガイドライン第三版/B-1データセットの被覆性')
    
    #### Inventories
    ds_req = manifest_genenerator.format_ait_inventory_requirement(format_=['json'])
    
    manifest_genenerator.add_ait_inventories(name='label_dataset',
                                             type_='dataset',
                                             description="COCO形式の訓練データとテストデータのラベルデータ。imagesフィールドには、各画像のメタ情報（画像ラベルの属性。例：weather,timeofday,sceneなど）を記載し、annotationフィールドには物体ごとの情報（オブジェクトラベルの属性。例:catogory_id.bboxなど）を記載する。またimagesフィールドに各画像が訓練データかテストデータ化を識別するため、splitフィールド（trainまたはtest）を追加する。COCO形式のフォーマットはこちらを参考にしてください：https://qiita.com/kHz/items/8c06d0cb620f268f4b3e",
                                             requirement=ds_req)
    #### Parameters    
    manifest_genenerator.add_ait_parameters(name='target_image_attributes', 
                                            type_='str', 
                                            description='t-wayの組み合わせの計算に使用する、各画像に付随する画像ラベルの属性名を指定。指定した属性をもとにデータ間の違いを分析する。指定した属性が1つの場合は2-wayの組み合わせを使用し、指定した属性が複数の場合は3-wayの組み合わせを使用する。入力例：weather、timeofday,scene', 
                                            default_val='attributeA,attributeB')
    #### Measures
    manifest_genenerator.add_ait_measures(name='set_difference_combinatorial_coverage', 
                                          type_='float', 
                                          description='訓練データで観測された属性の組み合わせのうち、テストデータに存在しない割合。値が高いほどテストデータと訓練データの属性の組み合わせが異なる。', 
                                          structure='single',
                                          min='0',
                                          max='1')
    #### Resource
    manifest_genenerator.add_ait_resources(name='Train_Test_Attribute_Combinations_Table',
                                         type_='table', 
                                         description='訓練データとテストデータで観測された属性の組み合わせをまとめた表')
    
    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AIT実行ログ')
    
    manifest_path = manifest_genenerator.write()


# In[9]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='label_dataset',
                                        value='data/bdd100K_train_test_coco.json')
    input_generator.set_ait_params("target_image_attributes", "weather,scene,timeofday")
    
    input_generator.write()


# In[10]:


#########################################
# area:initialize
# do not edit
#########################################

logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)

if is_ait_launch:
    # launch from AIT
    current_dir = path.dirname(path.abspath(__file__))
    path_helper = AITPathHelper(argv=sys.argv, ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)
else:
    # launch from jupyter notebook
    # ait.input.json make in input_dir
    input_dir = '/usr/local/qai/mnt/ip/job_args/1/1'
    current_dir = get_ipython().run_line_magic('pwd', '')
    path_helper = AITPathHelper(argv=['', input_dir], ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)

ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())

### do not edit cell


# In[11]:


#########################################
# area:functions
# should edit
#########################################
@log(logger)
def calculate_combinations(label_data,target_attributes_list):
    """
    訓練データのラベルデータにある画像ラベルの属性と画像内のオブジェクトの属性の組み合わせを測定する関数。
    テストデータのラベルデータにも同様に組み合わせを測定する。
    parameter:
        label_data:coco形式のラベルデータ
        target_attributes_list：指定された画像ラベルの属性のリスト
    return:
        train_combinations:訓練データで観測された属性の組み合わせ
        test_combinations:テストデータで観測された属性の組み合わせ
        all_combinations:訓練データまたはテストデータで観測された属性の組み合わせ
    """
    #訓練データとテストデータに分割
    train_data={img["id"]:img for img in label_data["images"] if img["split"]=="train"}
    test_data={img["id"]:img for img in label_data["images"] if img["split"]=="test"}
    #カテゴリ情報の取得
    category_id_name={c["id"]:c["name"] for c in label_data["categories"]}
    #訓練データ・テストデータの属性の組み合わせを記録する集合を用意
    train_combinations =set()
    test_combinations =set()
    
    for ann in label_data["annotations"]:
        #オブジェクトが含まれる画像のidを取得
        img_id = ann["image_id"]
        #オブジェクトのカテゴリidを取得
        category_id=ann["category_id"]
        #カテゴリidからオブジェクト名を取得
        category = category_id_name[category_id]
        #オブジェクトが含まれる画像が訓練データなのかテストデータなのかをチェック
        if img_id in train_data:
            img_attrs = train_data[img_id]#画像の情報を取得
            dataset = train_combinations
        elif img_id in test_data:
            img_attrs = test_data[img_id]#画像の情報を取得
            dataset = test_combinations
        else:
            continue
        #指定された属性が１つのときの処理
        if len(target_attributes_list)<2:
            attr=target_attributes_list[0]
            img_attr_values = img_attrs.get(attr)
            #(カテゴリ名,属性名,属性の値)の集合を作成し、訓練データの集合またはテストデータの集合に入れる
            dataset.add((category,attr,img_attr_values))
        #指定された属性が複数のときの処理
        else:
            #属性名をkey、属性の値をvalueとする辞書の作成
            img_attr_values = {attr:img_attrs.get(attr,"unused") for attr in target_attributes_list}
            #属性名から属性の組み合わせを計算し、リストに格納
            attribute_pairs=list(combinations(target_attributes_list,2))
            #属性名をkey、属性の値をvalueとする辞書から属性の組み合わせを使い属性の値を取得する
            for attr_pair in attribute_pairs:
                attr_value = (img_attr_values[attr_pair[0]],img_attr_values[attr_pair[1]])
                #(カテゴリ名,属性1の名前,属性1の値,属性2の名前,属性2の値)の集合を作成し、訓練データの集合またはテストデータの集合に入れる
                dataset.add((category,attr_pair[0],attr_value[0],attr_pair[1],attr_value[1]))
    #和集合より、観測したすべての組み合わせを保存
    all_combinations = train_combinations | test_combinations

    return train_combinations, test_combinations, all_combinations


# In[12]:


@log(logger)
@measures(ait_output, 'set_difference_combinatorial_coverage')
def calculate_sdcc(train_combinations,test_combinations):
    """
    訓練データで観測された属性の組み合わせとテストデータで観測された属性の組み合わせからSDCCを計算する関数
    parameters:
        train_combinations:訓練データで観測された属性の組み合わせ
        test_combinations:テストデータで観測された属性の組み合わせ
    return:
        sdcc_value:訓練データで観測された属性の組み合わせのうち、テストデータに存在しない割合
    """
    if len(train_combinations)>0:
        sdcc_value = len(train_combinations - test_combinations)/len(train_combinations)
    #train_combinationsが0の時の処理
    else:
        sdcc_value=0
    return sdcc_value


# In[13]:


@log(logger)
@resources(ait_output, path_helper, 'Train_Test_Attribute_Combinations_Table',"Train_Test_Attribute_Combinations_Table.csv")
def output_csv(train_combinations, test_combinations, all_combinations,target_attributes_list,file_path: str=None):
    """
    訓練データとテストデータで観測された属性の組み合わせをまとめた表を出力する関数。
    parameters:
       train_combinations:訓練データで観測された属性の組み合わせ
        test_combinations:テストデータで観測された属性の組み合わせ
        all_combinations:訓練データまたはテストデータで観測された属性の組み合わせ        
        target_attributes_list：指定された画像ラベルの属性のリスト
     """
    csv_data=[]
    for comb in sorted(all_combinations):
        #指定された属性が複数のときの処理
        if len(target_attributes_list)>=2:
            category, attr_name1, attr_value1, attr_name2, attr_value2 =comb
            #訓練データで観測された場合は〇、観測されていない場合は全角スペース
            train_flag ="〇" if comb in train_combinations else "　"
            #テストデータで観測された場合は〇、観測されていない場合は全角スペース
            test_flag ="〇" if comb in test_combinations else "　"
            #属性名をkey、属性の値(初期値は全角スペース)をvalueとする辞書の作成
            all_attribute_values = {attr:"　" for attr in target_attributes_list}
            #属性の値を更新
            all_attribute_values[attr_name1] = attr_value1
            all_attribute_values[attr_name2] = attr_value2
            #カテゴリ名、属性の値、訓練データで観測されているかどうかの判定、テストデータで観測されているかどうかの判定を保存
            csv_data.append([category]+[all_attribute_values[attr] for attr in target_attributes_list]+[train_flag, test_flag])
        #指定された属性が１つのときの処理
        else:
            category, attr_name1, attr_value1 =comb
            #訓練データで観測された場合は〇、観測されていない場合は全角スペース
            train_flag ="〇" if comb in train_combinations else "　"
            #テストデータで観測された場合は〇、観測されていない場合は全角スペース
            test_flag ="〇" if comb in test_combinations else "　"
            #カテゴリ名、属性の値、訓練データで観測されているかどうかの判定、テストデータで観測されているかどうかの判定を保存
            csv_data.append([category, attr_value1, train_flag, test_flag])
    columns =["category"]+target_attributes_list+["Train","Test"]
    df = pd.DataFrame(csv_data,columns=columns)
    df.to_csv(file_path,index=False)
    print(df)
    return file_path


# In[14]:


@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> str:
    shutil.move(get_log_path(), file_path)


# In[15]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper, is_ait_launch)
def main() -> None:
    #指定された属性の読み込み
    target_attributes = ait_input.get_method_param_value('target_image_attributes')
    target_attributes_list = [attr.strip() for attr in target_attributes.strip().split(",")]
    #データセットの読み込み
    label_path = ait_input.get_inventory_path('label_dataset')
    with open(label_path,"r") as lf:
        label_data=json.load(lf)
    #属性の組み合わせを計算し、取得する
    train_combinations, test_combinations, all_combinations = calculate_combinations(label_data, target_attributes_list)
    #SDCCの計算と表示
    sdcc_value = calculate_sdcc(train_combinations,test_combinations)
    print(f"Set Difference Combinatorial Coverage Value:{sdcc_value}")
    #訓練データとテストデータで観測された属性の組み合わせをまとめた表を表示
    csv_data=output_csv(train_combinations, test_combinations, all_combinations,target_attributes_list)    
    move_log()


# In[16]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[17]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2025'


# In[18]:


#########################################
# area:prepare deproy
# do not edit
#########################################

if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    from ait_sdk.license.license_generator import LicenseGenerator
    
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_sdk_name, current_dir, requirements_path)
    
    # output License.txt
    license_generator = LicenseGenerator()
    license_generator.write('../top_dir/LICENSE.txt', ait_creation_year, ait_owner)

