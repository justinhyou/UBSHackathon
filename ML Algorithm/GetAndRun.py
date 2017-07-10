# description:
# FFnet is a basic multilevel neural network class
# The number of layers is arbitrary.
# Each layer has a function, as specified using the class ActivationFunction.
# Each layer has its own learning rate.

import math
import random
from random import shuffle
import sklearn
import csv
import GetDataFromURL as get

#example:
#nnet = FFnet("cancer", [9, 5, 1], [logsig, logsig], [0.5, 0.2])

#Variable assignment: "nnet"
#Network name: "cancer"
#[9, 5, 1]: Nine nodes at input layer
#           Five nodes at middle layer
#           One node at output layer
#[logsig, logsig]: Logsig regression function between each layer
#[0.5, 0.2]: Learning rate for each weight within those layers
#            (i.e. 0.5 for learning rate)

# nnet.describe(False)
# Verbosity: output the descriptions

# nnet.train(cancerTrainingSamples, 2000, 100, False)
# Training Sample data set
# how many epochs to run through the data
# displayInterval: how often to display results from training
# Verbose: outputs information about the training at that epoch

# nnet.assessAll(cancerTestSamples)
# Validation testing data set

class FFnet:
    def __init__(nn, name, size, function, rate):
        """ Feedforward Neural Network                                    """
	""" nn is the 'self' reference, used in each method               """
        """ name is a string naming this network.                         """
        """ size is a list of the layer sizes:                            """
        """     The first element of size is understood as the number of  """
        """         inputs to the network.                                """
        """     The remaining elements of size are the number of neurons  """
        """         in each layer.                                        """
        """     Therefore the last element is the number of outputs       """
        """         of the network.                                       """
        """ function is a list of the activation functions in each layer. """
        """ deriv is a list of the corresponding function derivatives.    """
        """ rate is a list of the learning rate for each layer.           """

        nn.name = name
        nn.size = size
        nn.output = [[0 for i in range(s)] # output values for all layers,
                        for s in size]     # counting the input as layer 0

        nn.range1 = range(1, len(size))    # indices excluding the input layer
        nn.lastLayer = len(size)-1         # index of the last layer
        size1 = size[1:]                   # layer sizes excluding the input layer

        # dummy is used because the input layer does not have weights
        # but we want the indices to conform.
        dummy = [[]]
        nn.function = dummy + function
        nn.rate = dummy + rate

        # initialize weights and biases
        nn.weight = dummy + [[[randomWeight() for synapse in range(size[layer-1])]
                                              for neuron in range(size[layer])]
                                              for layer in nn.range1]

        nn.bias = dummy+[[randomWeight() for neuron in range(layer)]
                                         for layer in size1]

        nn.sensitivity = dummy + [[0 for neuron in range(layer)]
                                     for layer in size1]

        nn.act = dummy + [[0 for i in range(layer)]
                             for layer in size1]

    def describe(nn, noisy):
        """ describe prints a description of this network. """
        print "---------------------------------------------------------------"
        print "network", nn.name + ":"
        print "size =", nn.size
        print "function =", map(lambda x:x.name, nn.function[1:])
        print "learning rate =", nn.rate[1:]
        if noisy:
            print "weight =", roundall(nn.weight[1:], 3)
            print "bias =", roundall(nn.bias[1:], 3)

    def forward(nn, input):
        """ forward runs the network, given an input vector. """
        """ All act values and output values are saved.      """
        """ The output of the last layer is returned as a    """
        """ convenience for later testing.                   """

        nn.output[0] = input # set input layer

        # Iterate over all neurons in all layers.

        for layer in nn.range1:
            fun = nn.function[layer].fun
            for neuron in range(nn.size[layer]):
                # compute and save the activation
                nn.act[layer][neuron] = nn.bias[layer][neuron] \
                           + inner(nn.weight[layer][neuron], nn.output[layer-1])
                # compute the output
                nn.output[layer][neuron] = fun(nn.act[layer][neuron])

        return nn.output[-1]

    def backward(nn, desired):
        """ backward runs the backpropagation step, """
        """ computing and saving all sensitivities  """
        """ based on the desired output vector.     """

        # Iterate over all neurons in the last layer.
        # The sensitivites are based on the error and derivatives
        # evaluated at the activation values, which were saved during forward.

        deriv = nn.function[nn.lastLayer].deriv
        for neuron in range(nn.size[nn.lastLayer]):
            error = desired[neuron] - nn.output[nn.lastLayer][neuron]
            nn.sensitivity[nn.lastLayer][neuron] = \
                error*deriv(nn.act[nn.lastLayer][neuron], \
                            nn.output[nn.lastLayer][neuron])

        # Iterate backward over all layers except the last.
        # The sensitivities are computed from the sensitivities in the following
        # layer, weighted by the weight from a neuron in this layer to the one
        # in the following, times this neuron's derivative.

        for layer in range(nn.lastLayer-1, 0, -1):
            deriv = nn.function[layer].deriv
            # preNeuron is the neuron from which there is a connection
	    # postNeuron is the neuron to which there is a connection
            for preNeuron in range(nn.size[layer]):
                factor = deriv(nn.act[layer][preNeuron], nn.output[layer][preNeuron])
                sum = 0
                for postNeuron in range(nn.size[layer+1]):
                    sum += nn.weight[layer+1][postNeuron][preNeuron] \
                          *nn.sensitivity[layer+1][postNeuron]
                nn.sensitivity[layer][preNeuron] = sum*factor

    def update(nn):
        """ update updates all weights and biases based on the       """
        """ sensitivity values learning rate, and inputs to          """
        """ this layer, which are the outputs of the previous layer. """

        for layer in nn.range1:
            for neuron in range(nn.size[layer]):
                factor = nn.rate[layer]*nn.sensitivity[layer][neuron]
                nn.bias[layer][neuron] += factor
                for synapse in range(nn.size[layer-1]):
                    nn.weight[layer][neuron][synapse] \
                        += factor*nn.output[layer-1][synapse]

    def learn(nn, input, desired):
        """ learn learns by forward propagating input,  """
        """ back propagating error, then updating.      """
        """ It returns the output vector and the error. """

        nn.forward(input)
        nn.backward(desired)
        nn.update()
        output = nn.output[-1]
        error = subtract(desired, output)
        return [output, error]

    def assess(nn, sample, noisy):
        """ Assess the classification performance of a sample.             """
        """ returns 1 or 0 indicating correct or incorrect classification. """

        [input, desired] = sample
        nn.forward(input)
        output = nn.output[-1]
        error = subtract(desired, output)
        wrong = countWrong(error, 0.5)
        if noisy:
            print nn.name, "input =", input, \
                  "desired =", desired, \
                  "output =", roundall(output, 3), \
                  "error =", roundall(error, 3), \
                  "wrong =", wrong
        return wrong

    def train(nn, samples, epochs, displayInterval, noisy):
        """ Trains the network using the specified set of samples,   """
        """ for the specified number of epochs.                      """
        """ displayInterval indicates how often to display progress. """
        """ If using as a classifier, assumes the first component in """
        """ the output vector is the classification.                 """

        previousMSE = float("inf")
        for epoch in range(epochs):
            shuffle(samples)
            SSE = 0
            wrong = 0
            for [x, y] in samples:
                [output, error] = nn.learn(x, y)
                SSE += inner(error, error)/len(output)
                wrong += countWrong(error, 0.5)
            MSE = SSE/len(samples)
            wrongpc = 100.0*wrong/(len(samples)*len(output))
            # if wrong == 0:
            #     break   # stop if classification is correct
            if epoch%displayInterval == 0:
                direction = "decreasing" if MSE < previousMSE else "increasing"
                print nn.name, "epoch", epoch, "MSE =", round(MSE, 3), "wrong =", \
                    str(wrong) + " (" + str(round(wrongpc, 3)) + "%)", direction
            previousMSE = MSE

        if noisy:
            print nn.name, "final weight =", roundall(nn.weight[1:], 3)
            print nn.name, "final bias =", roundall(nn.bias[1:], 3)
        wrong = 0
        for sample in samples:
            wrong += nn.assess(sample, noisy)
        wrongpc = 100.0*wrong/(len(samples)*len(output))
        print nn.name, "final MSE =", round(MSE, 3), "final wrong =", \
                    str(wrong) + " (" + str(round(wrongpc, 3)) + "%)"

    def assessAll(nn, samples):
        """ Assess the network using the specified set of samples.   """
        """ Primarily used for testing an already-trained network.   """
        """ If using as a classifier, assumes the first component in """
        """ the output vector is the classification.                 """

        SSE = 0
        wrong = 0
        for [x, y] in samples:
            output = nn.forward(x)
            error = subtract(y, output)
            SSE += inner(error, error)/len(output)
            wrong += countWrong(error, 0.5)
        MSE = SSE/len(samples)
        wrongpc = 100.0*wrong/(len(samples)*len(output))
        print nn.name, "test MSE =", round(MSE, 3), "test wrong =", \
                    str(wrong) + " (" + str(round(wrongpc, 3)) + "%)"

class ActivationFunction:
    """ ActivationFunction packages a function together with its derivative. """
    """ This prevents getting the wrong derivative for a given function.     """
    """ Because some derivatives are computable from the function's value,   """
    """ the derivative has two arguments: one for the argument and one for   """
    """ the value of the corresponding function. Typically only one is use.  """

    def __init__(af, name, fun, deriv):
        af.name = name
        af.fun = fun
        af.deriv = deriv

    def fun(af, x):
        return af.fun(x)

    def deriv(af, x, y):
        return af.deriv(x, y)

logsig = ActivationFunction("logsig",
                            lambda x: 1.0/(1.0 + math.exp(-x)),
                            lambda x,y: y*(1.0-y))

tansig = ActivationFunction("tansig",
                            lambda x: math.tanh(x),
                            lambda x,y: 1.0 - y*y)

purelin = ActivationFunction("purelin",
                             lambda x: x,
                             lambda x,y: 1)

def randomWeight():
    """ returns a random weight value between -0.5 and 0.5 """
    return random.random()-0.5

def inner(x, y):
    """ Returns the inner product of two equal-length vectors. """
    n = len(x)
    assert len(y) == n
    sum = 0
    for i in range(0, n):
        sum += x[i]*y[i]
    return sum

def subtract(x, y):
    """ Returns the first vector minus the second. """
    n = len(x)
    assert len(y) == n
    return map(lambda i: x[i]-y[i], range(0, n))

def countWrong(L, tolerance):
    """ Returns the number of elements of L with an absolute """
    """ value above the specified tolerance. """
    return reduce(lambda x,y:x+y, \
                  map(lambda x:1 if abs(x)>tolerance else 0, L))

def roundall(item, n):
    """ Round a list, list of lists, etc. to n decimal places. """
    if type(item) is list:
        return map(lambda x:roundall(x, n), item)
    return round(item, n)

def csv_feed_training(feed):
    ubsTrainingSamples =  []
    with open(feed, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter= ' ', quotechar = '|')
        for row in spamreader:
            full_row = row[0].strip('\n').split(",")
            clean_row = []
            for i in range(len(full_row)-2):
                clean_row+=[float(full_row[i])]
            input_data = clean_row
#            summation = sum(input_data)
#            if (summation != 0):
#                input_data[:] = [x / summation for x in input_data]
            output_data = [float(full_row[-1])/10]
            ubsTrainingSamples = ubsTrainingSamples + [[input_data, output_data]]
    return ubsTrainingSamples

def csv_feed_testing(feed):
    ubsTrainingSamples =  []
    with open(feed, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter= ' ', quotechar = '|')
        for row in spamreader:
            full_row = row[0].strip('\n').split(",")
            clean_row = []
            for i in range(len(full_row)-1):
                clean_row+=[float(full_row[i])]
            input_data = clean_row
            ubsTrainingSamples = ubsTrainingSamples + [input_data]
    return ubsTrainingSamples

def rounding(num):
    beginningText = "This article "
    if (num<0.5):
        return beginningText + "does not reflect on this company's stocks positively.\n"
    elif (num>0.5):
        return beginningText + "reflects on this company's stocks positively.\n"
    else:
        return "error"

def returnedText(num):
    roundingText = rounding(num)
    otherText = "The AI predicts " + str(round(num*100, 2)) + "% confidence."

    if (roundingText=="error"):
        return "An error has occured."
    else:
        return roundingText + otherText
    justOneRandom = random.randrange(1, 10, 1)
    justOneRandomSample = trainingSet[justOneRandom]
    justOneRandomSampleInput = justOneRandomSample[0]


def ubs_hack(file):
    #UBS HACKATHON CONFIGURATIONS
    #layer_configuration = [50, 20, 5, 1]
    layer_configuration = [142, 70, 30, 8, 1]
    #function_series = [tansig, logsig, logsig]
    function_series = [tansig, logsig, logsig, logsig]
    #learning_rates = [0.2, 0.2, 0.1]
    learning_rates = [0.2, 0.2, 0.2, 0.1]
    describe = False
    trainingSet = csv_feed_training(file)
    epochs = 200
    visualizeFreq = 10
    verbose = False
    #validationSet = ubsValidationSamples
    validationSet = trainingSet

    nnet = FFnet("ubs_hack", layer_configuration, function_series, learning_rates)
    nnet.describe(describe)
    nnet.train(trainingSet, epochs, visualizeFreq, verbose)
    #nnet.assessAll(validationSet)

    justOneRandom = random.randrange(1, 10, 1)
    justOneRandomSample = trainingSet[justOneRandom]
    justOneRandomSampleInput = justOneRandomSample[0]

    results = []
    testingSet = csv_feed_testing('TEST.csv')
    print len(testingSet)
    for i in range(len(testingSet)):
        print testingSet[i]
        probability = nnet.forward(testingSet[i])
        results+=[probability[0]]
        print returnedText(probability[0])

    lengthOfQuery = len(testingSet)


    return lengthOfQuery, results
    #
    # probability = nnet.forward(justOneRandomSampleInput)
    # print returnedText(probability[0])

def main():
    get.main()
    numQueries, finalResult = ubs_hack('output.csv')
    in_file = open('TEST.csv', "rb")
    reader = csv.reader(in_file)
    out_file = open('OUT.csv', "wb")
    writer = csv.writer(out_file)

    # for i in range(numQueries):
    #     reader[i][143] = finalResult[i]
    #     writer.writerow(reader[i])

    # i = 0
    # for row in reader:
    #     print i, len(finalResult)
    #     row[143] = finalResult[i]
    #     writer.writerrow(row)
    #     i+=1

    i = 0
    for row in reader:
        row+=[finalResult[i]]
        writer.writerow(row)
        i+=1

    in_file.close()
    out_file.close()


main()
