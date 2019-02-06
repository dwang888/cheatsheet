from config import opt
import os
import torch as t
import models
from data.dataset import DogCat
from torch.utils.data import DataLoader
from torch.autograd import Variable
from torchnet import meter
from utils.visualize import Visualizer
from tqdm import tqdm
import sys
import os

def write_csv(results,file_name):
    import csv
    with open(file_name,'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id','label'])
        writer.writerows(results)
    
def train():
    # step1: configure model
    vis = Visualizer(opt.env)
    model = getattr(models, opt.model)()
    if opt.load_model_path and os.path.isfile(opt.load_model_path):
        model.load(opt.load_model_path)
    if opt.use_gpu: model.cuda()

    # step2: data
    train_data = DogCat(opt.train_data_root,train=True)
    # val_data = DogCat(opt.val_data_root,train=False)
    val_data = DogCat(opt.val_data_root, train=False)
    print('Size of training and val data:', len(train_data), len(val_data))

    train_dataloader = DataLoader(train_data,opt.batch_size,
                        shuffle=True,num_workers=opt.num_workers)
    val_dataloader = DataLoader(val_data,opt.batch_size,
                        shuffle=False,num_workers=opt.num_workers)
    print('Size of training and val loader:', len(train_dataloader.dataset), len(val_dataloader.dataset))
    # step3: criterion and optimizer
    criterion = t.nn.CrossEntropyLoss()
    lr = opt.lr
    optimizer = t.optim.Adam(model.parameters(),lr = lr,weight_decay = opt.weight_decay)
        
    # step4: meters
    loss_meter = meter.AverageValueMeter()
    confusion_matrix = meter.ConfusionMeter(2)
    previous_loss = 1e100

    # train
    for epoch in range(opt.max_epoch):
        
        loss_meter.reset()
        confusion_matrix.reset()

        for ii,(data,label) in tqdm(enumerate(train_dataloader),total=len(train_data)):

            # train model 
            input = Variable(data)
            target = Variable(label)
            if opt.use_gpu:
                input = input.cuda()
                target = target.cuda()

            optimizer.zero_grad()
            score = model(input)
            loss = criterion(score,target)
            loss.backward()
            optimizer.step()
            
            
            # meters update and visualize
            # print('printing: loss.data')
            # print(type(loss.data), loss.data)

            loss_data_cpu = loss.data.cpu().numpy()
            # print(type(loss_data_cpu), loss_data_cpu)
            # loss_meter.add(loss.data)
            loss_meter.add(loss_data_cpu)
            confusion_matrix.add(score.data, target.data)

            if ii%opt.print_freq==opt.print_freq-1:
                vis.plot('loss', loss_meter.value()[0])
                
                # # 进入debug模式
                # if os.path.exists(opt.debug_file):
                #     import ipdb;
                #     ipdb.set_trace()


        # model.save()

        # validate and visualize
        val_cm,val_accuracy, val_cm_value = val(model,val_dataloader)
        print(val_accuracy)
        print(val_cm_value)
        print(confusion_matrix.value())
        vis.plot('val_accuracy',val_accuracy)
        vis.log("epoch:{epoch},lr:{lr},loss:{loss},train_cm:{train_cm},val_cm:{val_cm}".format(
                    epoch = epoch,loss = loss_meter.value()[0],val_cm = str(val_cm.value()),train_cm=str(confusion_matrix.value()),lr=lr))
        
        # update learning rate
        if loss_meter.value()[0] > previous_loss:          
            lr = lr * opt.lr_decay
            # 第二种降低学习率的方法:不会有moment等信息的丢失
            for param_group in optimizer.param_groups:
                param_group['lr'] = lr
        

        previous_loss = loss_meter.value()[0]

def val(model,dataloader):
    '''
    计算模型在验证集上的准确率等信息
    '''
    model.eval()
    confusion_matrix = meter.ConfusionMeter(2)
    for ii, data in enumerate(dataloader):
        input, label = data
        val_input = Variable(input)
        val_label = Variable(label.type(t.LongTensor))
        if opt.use_gpu:
            val_input = val_input.cuda()
            val_label = val_label.cuda()
        score = model(val_input)
        confusion_matrix.add(score.data.squeeze(), label.type(t.LongTensor))

    model.train()
    cm_value = confusion_matrix.value()
    accuracy = 100. * (cm_value[0][0] + cm_value[1][1]) / (cm_value.sum())
    return confusion_matrix, accuracy, cm_value


if __name__=='__main__':
    train()