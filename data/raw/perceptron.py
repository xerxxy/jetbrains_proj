import torch
import torch.nn as nn 
import torch.optim as optim
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from code.models.circle.circle_net import CircleNet2_1, CircleNet2_2_1


def generate_data(num_points = 10000, seed = 42):
    np.random.seed(seed)
    X = np.random.uniform(-1.5, 1.5, (num_points, 2))
    y = np.linalg.norm(X, axis = 1) <= 1
    y = y.astype(int)
    return X, y

def get_split(no_elements = 10000):
    X,y = generate_data(no_elements)
    print("This is y", sum(y))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state= 42)
    X_train = torch.tensor(X_train, dtype= torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)
    return X_train, y_train, X_test, y_test



def train(model, criterion, optimizer, X_train, y_train, num_epochs = 1000):

    for epoch in range(num_epochs):
        model.train()
        
        outputs = model(X_train)

        loss = criterion(outputs, y_train)
        
        optimizer.zero_grad()
        loss.backward()
        
        optimizer.step()

        # if (epoch + 1) % 100 == 0:
        #     print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
def print_parameters(model):
    for name, param in model.named_parameters():
        print(f"Parameter name: {name}")
        print(f"Parameter size: {param.size()}")
        print(f"Parameter values:\n{param}\n")   
           
def get_parameters_as_string(model):
    param_str = ""
    for name, param in model.named_parameters():
        param_str += f"{name}: {param.tolist()}; "
    return param_str

def plot_test_points_with_activations(X_test, test_outputs, y_test):
    X_test_np = X_test.numpy()  
    test_outputs_np = test_outputs.numpy().flatten()  # Model's predicted activations (output)
    y_test_np = y_test.numpy().flatten()  # Actual labels for test data

    plt.figure(figsize=(8, 6))

    # Plot the points, colored by the sigmoid output (model's predicted activation)
    plt.scatter(X_test_np[:, 0], X_test_np[:, 1], c=test_outputs_np, cmap='coolwarm', s=50, edgecolors='k')
    
    # Add color bar to show the activation values
    plt.colorbar(label='Activation (Sigmoid Output)')
    
    # Set plot labels and title
    plt.xlabel('X1 (Coordinate)')
    plt.ylabel('X2 (Coordinate)')
    plt.title('Test Points with Model Activations (Sigmoid Output)')
    
    # Show the plot
    plt.show()
    
def evaluate(model, X_test, y_test):

    model.eval()
    with torch.no_grad():

        test_outputs = model(X_test)
        
        test_predictions = (test_outputs >= 0.5).float()  # Convert probabilities to binary 0/1 predictions

        accuracy = (test_predictions.eq(y_test).sum() / float(y_test.shape[0])).item()
        plot_test_points_with_activations(X_test, test_outputs,y_test)
        return accuracy

 
