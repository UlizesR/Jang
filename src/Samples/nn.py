class perceptron:
    def __init__(self, weights, bias, size):
        self.bias = bias
        self.weights = weights
        self.size = size
    
    def ReLU(self, inputSum):
        if (inputSum < 0):
            return 0
        return 1
    
    def SumInputs(self, inputArr):
        sum = self.bias
        for idx in range(self.size):
            sum += (self.weights[idx] * inputArr[idx])
        return sum
    
    def feedThrough(self, inputarr):
        out = self.SumInputs(inputarr)
        out = self.ReLU(out)
        return out
    
class HiddenLayer:
    def __init__(self, size, weights, biases):
        self.perceptrons = []
        self.size = size
        for i in [0,1]:
            self.perceptrons.append(perceptron(weights[i], biases[i], size))
    
    def feedThrough(self, inputArr):
        out = []
        temp = 0
        count = 0
        for pt in self.perceptrons:
            temp = pt.feedThrough(inputArr)
            out.append(temp)
            count += 1
        return out
    
output = perceptron([-1,1], -.5, 2)
hl = HiddenLayer(2, [[1,1],[1,1]], [-1.5, -.5])

hlOut = hl.feedThrough([0,0])
print(hlOut)
print(output.feedThrough(hlOut))
