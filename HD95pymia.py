import pymia.evaluation.metric as metric
import pymia.evaluation.evaluator as eval_
import pymia.evaluation.writer as writer
import SimpleITK as sitk
import os
import pandas as pd
import numpy as np
import gatetools as gt
import itk
# path to the folders
folder1 = "ADMIREauto_contouring/TestSET/Test002/RTS_MANUAL_REF/"

folder2 = "ADMIREauto_contouring/TestSET/Test002/RTS_MIM_MV/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_CLB_70DL/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_ARTplan/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_ARTplan_corr/"
#folder2 = "ADMIREauto_contouring/TestSET/Test001/RTS_RF_CORR/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_STAPLE/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_PATCHFUSION/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_RF/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_MIM/"
#folder1 = "ADMIREauto_contouring/TestSET/Test015/RTS_Manual_CTVn/"
#folder2 = "ADMIREauto_contouring/TestSET/Test_019/RTS_ABAS_RandomForest/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_EKTDL/"
#folder2 = "ADMIREauto_contouring/TestSET/Test001/RTS_EKTDL/"
#folder2 = "ADMIREauto_contouring/TestSET/Test009/RTS_CLB_70DL_corr/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RT/"
#folder2 = "ADMIREauto_contouring/TestSET/Test018/RTS_MIM_OARs/"
#folder2 = "ADMIREauto_contouring/TestSET/Test001/RTS_CLB_DL63/"
#folder2 = "ADMIREauto_contouring/TestSET/Test013/RTS_CLB_84DL/"
#folder2 = "ADMIREauto_contouring/TestSET/Test015/RTS_MIM_CTVn2-4/"

# find the structs
structs = []

for f in os.listdir(folder1):
    if f.endswith('.mhd') and os.path.isfile(os.path.join(folder2, f)):
        structs.append(f)
print(structs)
print(len(structs))
#define metrics
distances = {}
metrics = [metric.DiceCoefficient(), metric.HausdorffDistance(percentile=100, metric='HDmax'),metric.HausdorffDistance(percentile=95, metric='HD95'),metric.HausdorffDistance(percentile=50, metric='HDmedian'),metric.VolumeSimilarity()]
for metric in metrics:
  distances[metric.metric] = []
#distances["vol1"] = []
#distances["vol2"] = []
for struct in structs:
  labels = {1: struct }
  evaluator = eval_.SegmentationEvaluator(metrics, labels)
  #open images and execute
  ground_truth = sitk.ReadImage(os.path.join(folder1, struct))
  prediction = sitk.ReadImage(os.path.join(folder2, struct))
  evaluator.evaluate(prediction, ground_truth, "T")
  # print results
  #writer.ConsoleWriter().write(evaluator.results)
  # save results
  for r in evaluator.results:
    distances[r.metric].append(r.value)

df = pd.DataFrame(data=np.transpose(np.array(list(distances.values()))), index = structs, columns=list(distances.keys()))
print(df)
