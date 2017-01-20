# -*- coding: utf-8 -*-


class TrainType(object):
    # 车次类型
    trainTypeListAll = ['-g', '-d', '-t', '-k', '-z']
    def getTrainType(self, arguments):
        trainTypeListQuery = []
        for trainType in self.trainTypeListAll:
            trainTypeIsQuery = arguments[trainType]
            if (trainTypeIsQuery):
                trainTypeListQuery.append(trainType[1:].lower())
        return trainTypeListQuery