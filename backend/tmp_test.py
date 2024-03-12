import numpy as np
from factor_analyzer import FactorAnalyzer
from scipy.linalg import orthogonal_procrustes

X=[(1,-2, -4), (0,3,0), (-4,4,2), (3,-3, 4), (-2,0, -2), (-3,0,-1), (0,1,-3), (4,-4,1), (-1,2,0), (2,-1,3)]

X = np.array(X)
standardized_matrix = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# Step 4: Correlation Matrix
correlation_matrix = np.corrcoef(standardized_matrix, rowvar=False)

# Step 5: Eigenvalue Decomposition
eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)

# Sorting eigenvalues and corresponding eigenvectors
num_components = 3
sorted_indices = np.argsort(eigenvalues)[::-1]
sorted_eigenvalues = eigenvalues[sorted_indices]
sorted_eigenvectors = eigenvectors[:, sorted_indices[:num_components]]

# Select the number of principal components (adjust this based on your analysis)

# Selecting the top 'num_components' eigenvectors


# Calculate factor loadings
factor_loadings = sorted_eigenvectors * np.sqrt(sorted_eigenvalues[:num_components])

# give me principal components
principal_components = np.dot(standardized_matrix, sorted_eigenvectors)


# switch sign for each column if the value with the highest absolute value is negative
for i in range(num_components):
    if factor_loadings[np.argmax(np.abs(factor_loadings[:, i])), i] < 0:
        factor_loadings[:, i] = -factor_loadings[:, i]

# Create a factor loadings table
factor_loadings_table = np.column_stack((np.arange(1, X.shape[1] + 1), factor_loadings))


# Display factor loadings table
print('Correlation Matrix:')
print(correlation_matrix)

print("Factor Loadings:")
print(factor_loadings_table)


print("Eigenvalues:")
print(sorted_eigenvalues)

print("Explained Variance:")
explained_variance = sorted_eigenvalues / sum(sorted_eigenvalues)
print(explained_variance)

factor_scores = np.dot(standardized_matrix, sorted_eigenvectors)

# Display factor scores
print("Factor Scores:")
print(factor_scores)

q_sorts = np.argsort(-factor_scores, axis=0)

# Print Q sorts
print("Q Sorts:")
print(q_sorts)
# reversse the q_sorts
q_sorts = q_sorts[::-1].T
print("Q Sorts:")
print(q_sorts)

# works only for same number of 
from factor_analyzer import Rotator
rotator = Rotator(method='varimax')
rotated_factor_loadings = rotator.fit_transform(factor_loadings[:, :2])
print("Rotated Factor Loadings:")
print(rotated_factor_loadings)



















