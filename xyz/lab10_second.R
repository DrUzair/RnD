#install.packages("caret")
#install.packages('doParallel')
#install.ackages('kernlab')
library(class)
library(caret)
library(doParallel)
# Enable parallel processing.
cl <- makeCluster(detectCores())
registerDoParallel(cl)
#library(imager)

# a function to load the data
load_mnist <- function() {
  load_image_file <- function(filename) {
    ret = list()
    f = file(filename,'rb')
    # IDX format
    # magic number to be ignored
    readBin(f,'integer',n=1 # how many integers to read
            ,size=4, # number of bytes
            endian='big' # target system big or little 
            )
    ret$n = readBin(f,'integer',n=1,size=4,endian='big')
    # number of files
    print (ret$n)
    # number of rows in the image
    nrow = readBin(f,'integer',n=1,size=4,endian='big')
    a <- paste('nrow', nrow, sep='-')
    print (a)
    # number of cols in the image
    ncol = readBin(f,'integer',n=1,size=4,endian='big')
    b <- paste('ncol', ncol, sep='-')
    print (b)
    
    x = readBin(f,'integer',n=ret$n*nrow*ncol,size=1,signed=F)
    ret$x = matrix(x, ncol=nrow*ncol, byrow=T)
    y <- paste(nrow(ret$x), " rows", ncol(ret$x), " cols", sep=" ")
    print(y)
    close(f)
    ret
  }
  load_label_file <- function(filename) {
    f = file(filename,'rb')
    readBin(f,'integer',n=1,size=4,endian='big')
    n = readBin(f,'integer',n=1,size=4,endian='big')
    y = readBin(f,'integer',n=n,size=1,signed=F)
    close(f)
    y
  }
  
  train_mat <- load_image_file('/Users/iadmin/Downloads/train-images.idx3-ubyte')
  test_mat <- load_image_file('/Users/iadmin/Downloads/t10k-images.idx3-ubyte')
  
  train_mat$y <- load_label_file('/Users/iadmin/Downloads/train-labels.idx1-ubyte')
  test_mat$y <- load_label_file('/Users/iadmin/Downloads/t10k-labels.idx1-ubyte')  
  
  train <<- data.frame(y=train_mat$y, train_mat$x)
  train$y <<- as.factor(train$y)
  
  test <<- data.frame(y=test_mat$y, test_mat$x)
  test$y <<- as.factor(test$y)
  }

# a function to show the data
show_digit <- function(arr784, col=gray(12:1/12), ...) {
  image(matrix(arr784, nrow=28)[,28:1], col=col, ...)
}

#load the data
load_mnist()

# showing a few samples
show_digit(as.matrix(train[1,2:785]))
show_digit(as.matrix(train[5,2:785]))

# cut the 10k data into tr and ts sets
trainIndex = createDataPartition(test$y, p = 0.70, list=FALSE)
tr = test[trainIndex,]
ts = test[-trainIndex,]

# train knn and check the confusion matrix
knn_prediction <- knn(train = tr[,2:785], test = ts[,2:785], cl= tr$y, k = 11)
confusionMatrix(knn_prediction, ts$y)

# apply pca on data
pca_model = prcomp(tr[,2:785])
tr_pca = predict(pca_model, tr[,2:785])
ts_pca = predict(pca_model, ts[,2:785])

# reduce the dimensions to n_pca e.g. 50
n_pc = 50
tr_pca = tr_pca[,1:n_pc]
ts_pca = ts_pca[,1:n_pc]

# train knn on reduced data and check the confusion matrix 
knn_prediction_pca <- knn(train = tr_pca, test = ts_pca, cl= tr$y, k = 11)
confusionMatrix(knn_prediction_pca, ts$y)

