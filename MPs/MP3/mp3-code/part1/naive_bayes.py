import numpy as np


class NaiveBayes(object):
    def __init__(self, num_class, feature_dim, num_value):
        """Initialize a naive bayes model.

		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		    num_value(int): number of possible values for each pixel 
		"""

        self.num_value = num_value
        self.num_class = num_class
        self.feature_dim = feature_dim

        self.prior = np.zeros(num_class)
        self.likelihood = np.zeros((feature_dim, num_value, num_class))

    def train(self, train_set, train_label):
        """ Train naive bayes model (self.prior and self.likelihood) with training dataset.
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

        print("Training Now...")
        # this denotes the size of training set
        set_size = len(train_set)

        # preset the smoothing parameter
        k = 1
        V = self.num_value

        for img_index in range(set_size):
            img_label = train_label[img_index]
            self.prior[int(img_label)] += 1

            for f_index in range(self.feature_dim):
                p_val = train_set[img_index][f_index]

                self.likelihood[int(f_index)][int(p_val)][img_label] += 1

        # start smoothing
        self.likelihood += k
        self.likelihood = self.likelihood / (set_size + k * V)

        self.prior /= set_size
        print(self.prior)
        self.save_model("self_train_prior.npy", "self_train_likelihood.npy")

    def test(self, test_set, test_label):
        """ Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""

        print("Testing Now...")
        accuracy = 0
        pred_label = np.zeros((len(test_set)))

        for i in range(len(test_set)):
            # i denotes the test_img_index
            poss_set = np.zeros(self.num_class)

            for c_i in range(self.num_class):
                poss = np.log(self.prior[c_i])

                for f_i in range(self.feature_dim):
                    p_val = test_set[i][f_i]
                    poss += np.log(self.likelihood[f_i][int(p_val)][c_i])

                poss_set[c_i] = poss

            p_label = np.argmax(poss_set)
            pred_label[i] = p_label

        for i in range(len(test_label)):
            accuracy += (test_label[i] == pred_label[i])

        accuracy /= len(test_label)

        return accuracy, pred_label

    def save_model(self, prior, likelihood):
        """ Save the trained model parameters
        """

        np.save(prior, self.prior)
        np.save(likelihood, self.likelihood)

    def load_model(self, prior, likelihood):
        """ Load the trained model parameters
        """

        self.prior = np.load(prior)
        self.likelihood = np.load(likelihood)

    def intensity_feature_likelihoods(self, likelihood):
        """
	    Get the feature likelihoods for high intensity pixels for each of the classes,
	        by sum the probabilities of the top 128 intensities at each pixel location,
	        sum k<-128:255 P(F_i = k | c).
	        This helps generate visualization of trained likelihood images. 
	    
	    Args:
	        likelihood(numpy.ndarray): likelihood (in log) with a dimension of
	            (# of features/pixels per image, # of possible values per pixel, # of class)
	    Returns:
	        feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
	            (# of features/pixels per image, # of class)
	    """

        feature_likelihoods = np.zeros((likelihood.shape[0], likelihood.shape[2]))

        for f_i in range(self.feature_dim):
            for c_i in range(self.num_class):
                ct = 0
                for p_val in range(128, 256):
                    ct += self.likelihood[f_i][p_val][c_i]

                feature_likelihoods[f_i][c_i] = ct

        return feature_likelihoods
