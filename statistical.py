from InquirerPy import inquirer
import statistics, time
import scipy.stats as stats
import numpy as np

class StatisticsCalculator:
    def get_dataset(self, prompt):
        while True:
            try:
                data = list(map(float, input(f"{prompt} (comma-separated): ").split(',')))
                if not data:
                    raise ValueError
                return data
            except ValueError:
                print("❌ Invalid input. Please enter comma-separated numbers.")

    def calculate_statistics(self):
        while True:
            choice = inquirer.select(
                message="📊 Select the statistical measure you want to calculate:",
                choices=[
                    "Mean", "Median", "Mode", "Standard Deviation", "Variance",
                    "Covariance & Correlation",
                    "Spearman Rank Correlation",
                    "Regression Analysis",
                    "❌ Exit"
                ],
            ).execute()

            if choice == "❌ Exit":
                break

            # For single-dataset stats
            if choice in ["Mean", "Median", "Mode", "Standard Deviation", "Variance"]:
                data = self.get_dataset("Enter numbers for Dataset 1")
                try:
                    if choice == "Mean":
                        result = statistics.mean(data)
                    elif choice == "Median":
                        result = statistics.median(data)
                    elif choice == "Mode":
                        result = statistics.mode(data)
                    elif choice == "Standard Deviation":
                        result = statistics.stdev(data)
                    elif choice == "Variance":
                        result = statistics.variance(data)
                    print(f"✅ {choice}: {result}")
                except Exception as e:
                    print(f"❌ Error calculating {choice}: {e}")

            # For two-dataset stats
            elif choice in ["Covariance & Correlation", "Spearman Rank Correlation", "Regression Analysis"]:
                data1 = self.get_dataset("Enter numbers for Dataset 1")
                data2 = self.get_dataset("Enter numbers for Dataset 2")
                try:
                    if len(data1) != len(data2):
                        raise ValueError("Datasets must be of equal length.")

                    if choice == "Covariance & Correlation":
                        cov = np.cov(data1, data2)[0][1]
                        corr = np.corrcoef(data1, data2)[0][1]
                        print(f"✅ Covariance: {cov}")
                        print(f"✅ Pearson Correlation: {corr}")

                    elif choice == "Spearman Rank Correlation":
                        spearman_corr, _ = stats.spearmanr(data1, data2)
                        print(f"✅ Spearman Rank Correlation: {spearman_corr}")

                    elif choice == "Regression Analysis":
                        slope, intercept, r_value, p_value, std_err = stats.linregress(data1, data2)
                        print(f"✅ Regression Line: Y = {slope:.2f}X + {intercept:.2f}")
                        print(f"   R-squared: {r_value**2:.4f}")
                        print(f"   P-value: {p_value:.4f}")
                        print(f"   Std. Error: {std_err:.4f}")
                except Exception as e:
                    print(f"❌ Error: {e}")
