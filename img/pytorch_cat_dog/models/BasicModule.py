#coding:utf8
import torch as t
import time
from config import opt
import os
from pathlib import Path, PureWindowsPath

class BasicModule(t.nn.Module):
    '''
    封装了nn.Module,主要是提供了save和load两个方法
    '''

    def __init__(self):
        super(BasicModule,self).__init__()
        self.model_name=str(type(self))# 默认名字

    def load(self, path):
        '''
        可加载指定路径的模型
        '''
        self.load_state_dict(t.load(path))

    def save(self, name=None):
        '''
        保存模型，默认使用“模型名字+时间”作为文件名
        '''
        if name is None:
            file_name = self.model_name + "_" + time.strftime('%m%d_%H-%M-%S.pth')
            # path_model = os.path.join(opt.path_root, r"code/pytorch_cat_dog/checkpoints/", file_name)
            path_model = Path(opt.path_root) / Path("code/pytorch_cat_dog/checkpoints") / Path(file_name)
            # name = prefix + time.strftime('%m%d_%H-%M-%S.pth')
            path_model = PureWindowsPath(path_model)
            # print(type(path_model), path_model)
            path_model = str(path_model)
            # print(path_model)
            path_model = r"C:/backup/OneDrive/projects/cat_dog/code/pytorch_cat_dog/checkpoints/" + file_name
            # path_model = r"C:/backup/OneDrive/projects/cat_dog/code/pytorch_cat_dog/checkpoints/temp.pth"
        t.save(self.state_dict(), path_model)
        # t.save(self.state_dict(), )
        return name


class Flat(t.nn.Module):
    '''
    把输入reshape成（batch_size,dim_length）
    '''

    def __init__(self):
        super(Flat, self).__init__()
        #self.size = size

    def forward(self, x):
        return x.view(x.size(0), -1)
