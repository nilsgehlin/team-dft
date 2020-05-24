import numpy as np
from scipy.stats import linregress

class Measurement(object):
    def __init__(self, segmentation, color, pixel_spacing):
        self.sagittalMeas = None
        self.coronalMeas = None
        self.axialMeas = None
        self.pixel_spacing = pixel_spacing
        self.segment_array = segmentation
        self.measure(segmentation)

        #determine if default red color is okay for this measurement
        self.color = [1,0,0]
        euc_diff = np.linalg.norm(np.array(color) - np.array(self.color))
        if euc_diff < 0.5:
            self.color = [0,1,0]


    def GetInfo(self, planeID):
        if planeID == 0: 
            info = self.sagittalMeas
            startPoint = np.append( info[0], info[2][0][0] ) 
            endPoint = np.append( info[0], info[2][0][1] )

        if planeID == 1: 
            info = self.coronalMeas
            startPoint = np.flip( np.insert(info[2][0][0], 1, info[0]),  0)
            endPoint = np.flip( np.insert(info[2][0][1], 1, info[0]), 0)

        if planeID == 2: 
            info = self.axialMeas
            startPoint = np.append( info[2][0][0], info[0] ) 
            endPoint = np.append( info[2][0][1], info[0] )

        info = dict(major = list(info[1])[0],
                    minor = list(info[1])[1],
                    startPoint = startPoint.tolist(),
                    endPoint = endPoint.tolist(),
                    color = self.color,
                    area = info[3],
                    volume = np.count_nonzero(self.segment_array) * self.pixel_spacing[0] * self.pixel_spacing[1] * self.pixel_spacing[2]
        )
        return info

    
    def measure(self, segmentation):
        segmentationOnesZeros = segmentation

        sliceIndS = 0
        sliceIndC = 0
        sliceIndA = 0
        sagittalMeas = [0, (0, 0), 0, 0]  # slice, majMinor len tuple, extent tuple, area
        coronalMeas = [0, (0, 0), 0, 0]
        axialMeas = [0, (0, 0), 0, 0]

        for sagittalArray in segmentationOnesZeros:
            majMinorMeas = self.measureOrth(sagittalArray)
            if majMinorMeas[0][0] > sagittalMeas[1][0]:
                sagittalMeas[0] = sliceIndS
                sagittalMeas[1] = majMinorMeas[0]
                sagittalMeas[2] = majMinorMeas[1]
                sagittalMeas[3] = np.count_nonzero(sagittalArray) * self.pixel_spacing[0] * self.pixel_spacing[2]
            sliceIndS += 1
        print(sagittalMeas)
        self.sagittalMeas = sagittalMeas
        # print("Sagittal max major length of " + str(sagittalMeas[0][0]) + " at slice " + str(sagittalMeas[0][1]))
        # print("Sagittal max minor length of " + str(sagittalMeas[1][0]) + " at slice " + str(sagittalMeas[1][1]))

        segmentationOnesZerosC = np.transpose(segmentationOnesZeros, (1, 2, 0))
        for coronalArray in segmentationOnesZerosC:
            majMinorMeas = self.measureOrth(coronalArray)
            if majMinorMeas[0][0] > coronalMeas[1][0]:
                coronalMeas[0] = sliceIndC
                coronalMeas[1] = majMinorMeas[0]
                coronalMeas[2] = majMinorMeas[1]
                coronalMeas[3] = np.count_nonzero(coronalArray) * self.pixel_spacing[1] * self.pixel_spacing[2]
            sliceIndC += 1
        print(coronalMeas)
        self.coronalMeas = coronalMeas

        segmentationOnesZerosA = np.transpose(segmentationOnesZeros, (2, 0, 1))
        for axialArray in segmentationOnesZerosA:
            majMinorMeas = self.measureOrth(axialArray)
            if majMinorMeas[0][0] > axialMeas[1][0]:
                axialMeas[0] = sliceIndA
                axialMeas[1] = majMinorMeas[0]
                axialMeas[2] = majMinorMeas[1]
                axialMeas[3] = np.count_nonzero(axialArray) * self.pixel_spacing[0] * self.pixel_spacing[1]
            sliceIndA += 1
        print(axialMeas)
        self.axialMeas = axialMeas


    
    def measureOrth(self, segArray):
        majDist = 0
        minorDist = None
        majExtent1 = None
        majExtent2 = None
        minorExtent1 = None
        minorExtent2 = None
        y, x = np.nonzero(segArray)
        if len(x) > 0:
            # find eigenvectors
            coords = np.vstack([x, y])

            cov = np.cov(coords)
            if not np.isnan(np.sum(cov)):
                evals, evecs = np.linalg.eig(cov)
                sort_indices = np.argsort(evals)[::-1]
                x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
                x_v2, y_v2 = evecs[:, sort_indices[1]]

                majDist, majExtent1, majExtent2 = self.measureMaxDist(x_v1, y_v1, x, y, segArray)
                minorDist, minorExtent1, minorExtent2 = self.measureMaxDist(x_v2, y_v2, x, y, segArray)

                # # plt.imshow(segArray)
                # # plt.imshow(majorArray.transpose())
                # # plt.plot(x, y, 'k.')
                # # plt.axis('equal')
                # # # plt.gca().invert_yaxis()  # Match the image system with origin at top left
                # # plt.show()

            else:
                print("np.cov() returns NaN")

        return [(majDist, minorDist), ((majExtent1, majExtent2), (minorExtent1, minorExtent2))]


    
    def measureMaxDist(self, ev_X, ev_Y, x, y, segArray):
        dist = 0
        max_x_index = None
        min_x_index = None
        k = 1000000  # arbitrary
        if ev_X > 0:
            slope, intercept, r_value, p_value, std_err = linregress(
                [ev_X * -k * 2 + np.mean(x), ev_X * k * 2 + np.mean(x)],
                [ev_Y * -k * 2 + np.mean(y), ev_Y * k * 2 + np.mean(y)])
            majMinorArray = np.fromfunction(lambda i, j: j == np.round(slope * i + intercept),
                                            (len(segArray[0]), len(segArray)), dtype=int)
        else:
            xIntercept = np.mean(x)
            majMinorArray = np.fromfunction(lambda i, j: i == np.round(xIntercept),
                                            (len(segArray[0]), len(segArray)), dtype=int)

        arrayOnesZeroes = majMinorArray.astype(np.int)
        extent = np.where(segArray & arrayOnesZeroes.transpose(), 1, 0)
        maxPoints = np.array(np.where(extent == 1)).transpose()

        if len(maxPoints) > 0:
            max_x_index = np.argmax(maxPoints[:, 1])
            min_x_index = np.argmin(maxPoints[:, 1])
            dist = np.linalg.norm(maxPoints[max_x_index] - maxPoints[min_x_index])

        return (dist, maxPoints[max_x_index], maxPoints[min_x_index])