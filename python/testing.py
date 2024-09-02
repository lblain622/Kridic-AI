import numpy as np
import matplotlib.pyplot as plt

# Data
time = np.array([0, 1/60, 1/30, 1/20, 1/15, 1/12, 1/10, 7/60, 2/15, 3/20, 1/6,
                 11/60, 1/5, 13/60, 14/60, 1/4, 16/60, 17/60, 18/60, 19/60, 20/60])
position = np.array([0, 1.2, 2.9, 4.9, 6.9, 9.4, 12.1, 15.1, 18.3, 21.8, 25.4,
                     29.5, 33.3, 38.4, 38.4, 43.4, 53, 59.3, 65.4, 71.6, 78.1])

# Fit quadratic trend line
coefficients = np.polyfit(time, position, 2)
a, b, c = coefficients

# Generate the trend line
trend_line = np.poly1d(coefficients)

# Calculate residuals
residuals = position - trend_line(time)
residuals_std = np.std(residuals)

# Calculate uncertainties based on residuals
n = len(time)
p = 3  # Number of parameters (a, b, c)
uncertainty_coefficient = residuals_std / np.sqrt(n - p)

# Estimate uncertainties in coefficients
# Formula: uncertainty = residuals_std / sqrt(sum((x_i - x_mean)^2))
# Here, sum((x_i - x_mean)^2) is computed as part of the standard error calculation
x_mean = np.mean(time)
sum_squared_deviations = np.sum((time - x_mean) ** 2)
uncertainty_a = 2 * uncertainty_coefficient
uncertainty_b = uncertainty_coefficient / np.sqrt(sum_squared_deviations)
uncertainty_c = uncertainty_coefficient

# Calculate gravitational acceleration
gravitational_acceleration = 2 * a
uncertainty_gravitational_acceleration = 2 * uncertainty_a

print(f"Quadratic Trend Line: y = {a:.4f}t^2 + {b:.4f}t + {c:.4f}")
print(f"Gravitational Acceleration: {gravitational_acceleration:.2f} cm/s^2")
print(f"Uncertainty in Gravitational Acceleration: ±{uncertainty_gravitational_acceleration:.2f} cm/s^2")

# Plot the data and trend line
plt.figure(figsize=(10, 6))
plt.scatter(time, position, color='blue', label='Data')
plt.plot(time, trend_line(time), color='red', label=f'Trend Line: y = {a:.4f}t^2 + {b:.4f}t + {c:.4f}')
plt.xlabel('Time (s)')
plt.ylabel('Position (cm)')
plt.title('Quadratic Trend Line Fit')
plt.legend()
plt.grid(True)
plt.show()
