import numpy as np

# Define the data
data = np.array([(1, -2, -4), (0, 3, 0), (-4, 4, 2), (3, -3, 4), (-2, 0, -2), (-3, 0, -1), (0, 1, -3), (4, -4, 1), (-1, 2, 0), (2, -1, 3)])

# Calculate the correlation matrix
corr_matrix = np.corrcoef(data, rowvar=False)

# Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(corr_matrix)

# Sort eigenvalues and corresponding eigenvectors
sorted_indices = np.argsort(eigenvalues)[::-1]
sorted_eigenvalues = eigenvalues[sorted_indices]
sorted_eigenvectors = eigenvectors[:, sorted_indices]

# Select the 3 best factors
selected_eigenvalues = sorted_eigenvalues[:3]
selected_eigenvectors = sorted_eigenvectors[:, :3]

# Rotate the selected eigenvectors with varimax
def varimax_rotation(loadings, tolerance=1e-4, max_iter=500):
    loadings_rotated = loadings.copy()
    for _ in range(max_iter):
        loadings_rotated_prev = loadings_rotated.copy()
        
        # Calculate the rotation matrix
        factors = loadings_rotated @ loadings_rotated.T
        rotation_matrix = np.linalg.inv(factors) @ loadings_rotated.T @ np.diag(np.sum(factors, axis=0))
        
        # Apply the rotation matrix
        loadings_rotated = loadings @ rotation_matrix
        
        # Check convergence
        if np.allclose(loadings_rotated, loadings_rotated_prev, atol=tolerance):
            break
    
    return loadings_rotated

# Rotate the selected eigenvectors with varimax
rotated_loadings = varimax_rotation(selected_eigenvectors)

# Calculate factor loadings
unrotated_loadings = selected_eigenvectors * np.sqrt(selected_eigenvalues)
rotated_eigenvalues, rotated_eigenvectors = np.linalg.eig(np.corrcoef(rotated_loadings, rowvar=False))
rotated_loadings = rotated_eigenvectors * np.sqrt(rotated_eigenvalues)

# Print results
print("Eigenvalues:")
print(sorted_eigenvalues)
print("\nSelected Eigenvectors:")
print(selected_eigenvectors)
print("\nUnrotated Loadings:")
print(unrotated_loadings)
print("\nRotated Loadings:")
print(rotated_loadings)