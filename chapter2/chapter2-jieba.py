# -*- coding: utf-8 -*-
import jieba as jb
import sys

seg_list=jb.cut("我从马上跳下来",cut_all=True)
print('Full mode','/'.join(seg_list))

seg_list=jb.cut("我从马上跳下来",cut_all=False)
print('Default mode:','/'.join(seg_list))

seg_list=jb.cut('Lucy硕士专业是计算机科学技术，后来读人工智能方向的博士')

print(','.join(seg_list))


import jieba.posseg as pseg
words=pseg.cut("我在学习知识表示与处理")
words2=pseg.cut('Lucy硕士专业是计算机科学技术，后来读人工智能方向的博士')

print("词性标注结果1")
for w in words:
    print(w.word,w.flag)

print("词性标注结果2")
for w in words2:
    print(w.word,w.flag)

