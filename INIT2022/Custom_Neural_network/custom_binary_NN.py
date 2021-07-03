class mygb_NN:
    def __init__(self):
        self.intercept=1
        self.features=[]
        self.n_features=0
        self.coef=[]
        
        
    
    def fit(self,x,y,epochs,loss_thresold):
        self.features=x.columns
        self.n_features=len(self.features)
        self.coef=np.zeros(len(self.features))
        
        self.coef, self.intercept = self.gradient_descent(x, y,epochs, loss_thresold)
        
    
    def predict(self,x_test):
        
        weighted_sum=0
        for i in range(self.n_features):
            weighted_sum+=self.coef[i]*x_test[self.features[i]]
        weighted_sum+=+self.intercept
        return self.sigmoid_np(weighted_sum)
    
    def evaluate(self,x_test,y_test):
        accurate=0
        n=len(x_test[self.features[0]])
        predicted=self.predict(x_test)
        loss=round(self.log_loss(y_true=y_test,y_predicted=predicted),4)
        for i,pred in predicted.iteritems():
            if round(pred)==y_test[i]:
                accurate+=1
        accuracy=accurate/n
        print(f"evalution result -----> loss: {loss} - accuracy: {accuracy}")
        return accuracy

        
    
    def sigmoid_np(self,z):
            import numpy as np
            return 1/(1+np.exp(-z))
            
    def log_loss(self,y_true,y_predicted):
            epsilon=1e-15
            y_predicted_new=[max(i,epsilon) for i in y_predicted]
            y_predicted_new=[min(i,1-epsilon) for i in y_predicted_new]
            y_predicted_new=np.array(y_predicted_new)
            logloss=-np.mean(y_true*np.log(y_predicted_new)+(1-y_true)*np.log(1-y_predicted_new))
            return logloss     

    def gradient_descent(self,x,y_true,epochs,loss_thresold):
            w=self.coef
            bias=self.intercept
            rate=0.5
            n=len(x[self.features[0]])
            n_features=self.n_features
            
    
            for j in range(epochs):
                weighted_sum=0
                for i in range(n_features):
                    weighted_sum+=w[i]*x[self.features[i]]
                
                weighted_sum+=+bias
                y_predicted=self.sigmoid_np(weighted_sum)
                loss=self.log_loss(y_true=y_true,y_predicted=y_predicted)
                wd=1
                for i in range(n_features):
                    wd=(1/n)*np.dot(np.transpose(x[self.features[i]]),(y_predicted-y_true))
                    w[i]=w[i]-rate*wd
                    
                bias_d=np.mean(y_predicted-y_true)
                bias=bias-rate*bias_d
        
                print (f'Epoch:{j} -----> bias:{bias}, loss:{loss}')
                if loss<=loss_thresold:
                    break
        
            return w,bias
    
    
    
